class MtgaCollectionExporterMac < Formula
  include Language::Python::Virtualenv

  desc "Export MTG Arena card collection on macOS to txt, json, and Moxfield csv"
  homepage "https://github.com/jv-darkheartlabs/mtga-collection-exporter-mac"
  url "https://github.com/jv-darkheartlabs/mtga-collection-exporter-mac/archive/refs/heads/main.tar.gz"
  version "1.0.0-mac"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_create(libexec, "python3.12")
    system libexec/"bin/pip", "install", "-r", "requirements-mac.txt"
    libexec.install "mtg.py", "mtga_memory.py"
    (bin/"mtga-export").write <<~EOS
      #!/bin/bash
      exec "#{libexec}/bin/python" "#{libexec}/mtg.py" "$@"
    EOS
  end

  def caveats
    <<~EOS
      MTG Arena must be running with Collection/Decks open before export.

      If memory access fails, run:
        sudo mtga-export

      Update the formula sha256 after cutting a release tarball.
    EOS
  end

  test do
    system libexec/"bin/python", "-m", "compileall", libexec/"mtg.py", libexec/"mtga_memory.py"
  end
end
