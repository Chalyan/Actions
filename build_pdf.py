import subprocess
import sys
from pathlib import Path
from datetime import datetime
import shutil

TEX_FILE = "main.tex"      # Your main TeX file
BASE = Path(TEX_FILE).stem
PDF_FILE = f"{BASE}.pdf"

def run(cmd):
    print(">>", " ".join(cmd))
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print("\n❌ Command failed:", " ".join(cmd))
        sys.exit(result.returncode)

def clean_aux():
    exts = [
        ".aux", ".log", ".toc", ".out", ".bbl", ".blg",
        ".fls", ".fdb_latexmk", ".synctex.gz", ".nav",
        ".snm", ".vrb", ".lof", ".lot"
    ]
    for ext in exts:
        f = Path(BASE + ext)
        if f.exists():
            f.unlink()
            print(f"Deleted {f}")

def main():
    if not Path(TEX_FILE).exists():
        print(f"❌ Error: TeX file '{TEX_FILE}' not found")
        sys.exit(1)

    print("🔧 Running first pdflatex pass...")
    run(["pdflatex", "-interaction=nonstopmode", TEX_FILE])

    # Check for bibliography (BASE.bib)
    bib_exists = Path(f"{BASE}.bib").exists()
    if bib_exists:
        print("📚 Bibliography detected — running bibtex...")
        run(["bibtex", BASE])

        print("🔧 Running second pdflatex pass...")
        run(["pdflatex", "-interaction=nonstopmode", TEX_FILE])

        print("🔧 Running final pdflatex pass...")
        run(["pdflatex", "-interaction=nonstopmode", TEX_FILE])

    # Confirm PDF exists
    pdf_path = Path(PDF_FILE)
    if not pdf_path.exists():
        print("❌ PDF was not generated.")
        sys.exit(1)

    # Rename output PDF
    today = datetime.today().strftime("%Y-%m-%d")
    new_name = f"{today} Thermal drag.pdf"
    shutil.move(PDF_FILE, new_name)
    print(f"✔ PDF renamed to '{new_name}'")

    clean_aux()
    print("🎉 Build completed successfully!")

if __name__ == "__main__":
    main()
