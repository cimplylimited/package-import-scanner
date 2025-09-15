Absolutely! Here’s a comprehensive `README.md` for your Python Import/Requirements Auditor script. This covers: what it does, how it works, installation and usage, customization, limitations, licensing, and contributions. You can further tailor it for your organization or repo as needed.

---

````markdown
# Python Import/Requirements Auditor

A simple, static-analysis tool to help Python developers **compare** the set of packages _actually imported in their codebase_ with those _listed in `requirements.txt`_. This tool helps find unused requirements ("dependency bloat"), missing requirements, and maintain a clean, accurate project dependency list.

## ✨ Features

- **Scans all Python files** (recursively) in a directory for:
  - `import X`
  - `import X as Y`
  - `from X import Y`
  - `from X.submodule import Z`
- **Compares** discovered imports with package names in `requirements.txt`
- Outputs:
  - Packages **used by your code but missing from `requirements.txt`**
  - Packages **listed in `requirements.txt` but not imported anywhere**
- Easy to run, no third-party dependencies
- Educational: Aimed to be readable and well-commented for onboarding

## 🚀 Why Use This?

- Keep your `requirements.txt` accurate and minimal
- Improve reproducibility and CI/CD reliability
- Reduce security risk by removing unnecessary packages
- Onboard new contributors more easily

---

## 🛠️ Installation

No installation required – just clone this repo:

```bash
git clone https://github.com/cimplylimited/package-import-scanner.git
cd package-import-scanner
```

**Requirements:**

- Python 3.6 or higher

---

## 📦 Usage

```bash
python import_audit.py
```

By default, scans the current directory (`.`) and looks for `requirements.txt`.

**Optional:** To scan a specific folder (e.g., `src/`):

```python
# Edit these variables at the top of the script:
source_dir = "./src"
reqfile = "requirements.txt"
```

---

## 📝 Output

Example output:

```
Imports found in codebase: ['flask', 'requests', 'pytest']
Packages in requirements.txt: ['flask', 'requests']
Possibly missing in requirements.txt (used in code, not listed): ['pytest']
Possibly unused in codebase (listed, but not imported directly): []
```

---

## ⚠️ Limitations & Notes

- The script detects _imported module names_; it does **not always match the exact PyPI package name** (e.g., `PIL` is `pillow`, `sklearn` is `scikit-learn`). Manual review or a mapping file may be needed for these.
- It does **not detect dynamically imported modules** (via `__import__` or `importlib`).
- Won't account for development/test-only tools or non-Python dependencies.
- Does not handle requirements files with complex conditions, extras, or VCS sources.

---

## 🔬 How It Works

1. **AST Parsing:** Uses Python’s `ast` module to robustly extract imports from all `.py` files.
2. **Requirements Parsing:** Scans `requirements.txt` for declared package names, stripping any version specifications.
3. **Comparison:** Set operations reveal which packages are present in one list but not the other.

See well-documented code in [`import_audit.py`](./import_audit.py)!

---

## 🤝 Contributing

PRs and suggestions are welcome! Please:

- Keep code clean and well-commented
- Add or update relevant docstrings
- Ensure output clarity and accuracy

---

## 🪪 License

Licensed under the [MIT License](LICENSE).

---

## 🙋 FAQ

**Q:** Does this handle packages only used in tests?  
_A:_ No; it looks for imports in all scanned files. If you want to skip test files, adjust the script to exclude test directories.

**Q:** Can this update my `requirements.txt` automatically?  
_A:_ No (by design) – it alerts you, but you should review and edit requirements manually for best hygiene.

**Q:** Will this work with Poetry or Pipenv?  
_A:_ It currently only parses `requirements.txt`. For `pyproject.toml`/`Pipfile`, you can adapt the requirements parsing function.

---

## 📝 Credits

Developed by CIMPLY. Inspired by best Python packaging hygiene practices.

---

_Maintaining clean dependencies is the first step to secure, scalable Python projects._

```

---


```
````
