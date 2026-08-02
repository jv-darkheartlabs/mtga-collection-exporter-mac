"""Cross-platform memory access for MTGA collection scanning."""

from __future__ import annotations

import ctypes
import ctypes.util
import os
import sys
from typing import Callable, Iterator, List, Optional, Protocol, Tuple

LogFn = Callable[[str], None]

Region = Tuple[int, int, int]
MAX_REGIONS = 200_000


class MemoryProcess(Protocol):
    process_id: int

    def read_bytes(self, address: int, size: int) -> bytes: ...

    def pattern_scan_all(
        self,
        pattern: bytes,
        return_multiple: bool = False,
        log: Optional[LogFn] = None,
    ) -> List[int]: ...


def get_process_name() -> str:
    return "MTGA.exe" if sys.platform == "win32" else "MTGA"


def connect_to_mtga() -> MemoryProcess:
    if sys.platform == "darwin":
        if os.geteuid() != 0:
            print(
                "\n[macOS] Memory access usually requires elevated privileges.\n"
                "If connection fails, rerun with: sudo python3 mtg.py\n"
            )
        return _MacMemoryProcess(get_process_name())

    if sys.platform == "win32":
        import pymem

        pm = pymem.Pymem(get_process_name())
        return _WindowsMemoryProcess(pm)

    raise RuntimeError(f"Unsupported platform: {sys.platform}")


class _WindowsMemoryProcess:
    def __init__(self, pm) -> None:
        self._pm = pm

    @property
    def process_id(self) -> int:
        return self._pm.process_id

    def read_bytes(self, address: int, size: int) -> bytes:
        return self._pm.read_bytes(address, size)

    def pattern_scan_all(
        self,
        pattern: bytes,
        return_multiple: bool = False,
        log: Optional[LogFn] = None,
    ) -> List[int]:
        result = self._pm.pattern_scan_all(pattern, return_multiple=return_multiple)
        if not result:
            return []
        if isinstance(result, list):
            return result
        return [result]


class _MacMemoryProcess:
    CHUNK_SIZE = 4 * 1024 * 1024
    PAGE_SIZE = 4096

    def __init__(self, process_name: str) -> None:
        import pymem as mac_pymem
        import pymem.process as mac_process

        self._pm = mac_pymem.Pymem(process_name)
        self._mac_process = mac_process
        self._libproc = ctypes.CDLL(ctypes.util.find_library("libproc"))
        from pymem.resources import vmtypes as vt

        self._vt = vt

    @property
    def process_id(self) -> int:
        return self._pm.pid

    def read_bytes(self, address: int, size: int) -> bytes:
        buffer = ctypes.create_string_buffer(size)
        read_size = self._mac_process.read(
            self._pm.task, ctypes.c_uint64(address), buffer, size
        )
        if read_size <= 0:
            raise OSError(f"mach_vm_read failed at 0x{address:x}")
        return buffer.raw[:read_size]

    def pattern_scan_all(
        self,
        pattern: bytes,
        return_multiple: bool = False,
        log: Optional[LogFn] = None,
    ) -> List[int]:
        if log:
            log("Starting memory region walk...")

        matches: List[int] = []
        scanned_regions = 0
        readable_regions = 0

        for region_index, (region_start, region_size, protection) in enumerate(
            self._iter_regions(log=log), start=1
        ):
            scanned_regions = region_index
            if not (protection & self._vt.VM_PROT_READ):
                continue
            if not (protection & self._vt.VM_PROT_WRITE):
                continue
            if region_size <= 0:
                continue

            readable_regions += 1
            if log and (readable_regions == 1 or readable_regions % 10 == 0):
                log(
                    f"Scanning heap region {readable_regions} "
                    f"(addr 0x{region_start:x}, size {region_size // (1024 * 1024)} MB)..."
                )

            offset = 0
            while offset < region_size:
                read_size = min(self.CHUNK_SIZE, region_size - offset)
                try:
                    data = self.read_bytes(region_start + offset, read_size)
                except OSError:
                    break

                search_at = 0
                while True:
                    idx = data.find(pattern, search_at)
                    if idx == -1:
                        break
                    matches.append(region_start + offset + idx)
                    if log:
                        log(f"Pattern match at 0x{region_start + offset + idx:x}")
                    if not return_multiple:
                        return matches
                    search_at = idx + 1

                if offset + read_size >= region_size:
                    break
                offset += read_size - len(pattern) + 1

        if log:
            log(
                f"Scan complete: {len(matches)} match(es) across "
                f"{readable_regions} writable region(s), {scanned_regions} total region(s)"
            )
        return matches

    def _iter_regions(self, log: Optional[LogFn] = None) -> Iterator[Region]:
        vt = self._vt
        addr = ctypes.c_uint64(0)
        size = ctypes.c_uint64(0)
        count = ctypes.c_uint32(vt.VM_REGION_BASIC_INFO_COUNT_64)
        info = vt.VmRegionBasicInfo64()
        obj_name = ctypes.c_uint32()

        for _ in range(MAX_REGIONS):
            count.value = vt.VM_REGION_BASIC_INFO_COUNT_64
            kern = ctypes.c_int(
                self._libproc.mach_vm_region(
                    self._pm.task,
                    ctypes.byref(addr),
                    ctypes.byref(size),
                    vt.VM_REGION_BASIC_INFO_64,
                    ctypes.byref(info),
                    ctypes.byref(count),
                    ctypes.byref(obj_name),
                )
            )
            if kern.value != 0:
                break

            region_start = addr.value
            region_size = size.value
            yield region_start, region_size, info.protection

            if region_size == 0:
                addr.value += self.PAGE_SIZE
            else:
                addr.value += region_size

        else:
            if log:
                log(f"[Warn] Region walk hit safety limit ({MAX_REGIONS}).")
