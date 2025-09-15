import ast
import os

def find_imports_in_file(filename):
    """
    Parse a single Python file and extract all the *top-level* imported module/package names.

    Args:
        filename (str): Path to the Python file to scan.

    Returns:
        Set[str]: The set of top-level module/package names imported in the file.
    
    Explanation:
        - Uses the 'ast' (Abstract Syntax Tree) standard library to robustly parse Python syntax.
        - Handles both forms of import statements:
            1. 'import X' and 'import X as Y': Direct imports.
            2. 'from X import Y' and 'from X.submodule import Z': Imports from submodules.
        - For 'import X', extracts 'X'.
        - For 'from X.submodule import Y', extracts just 'X' (the root package), because that's what you generally install via pip.
        - Returns a set so multiple instances don't cause duplicates.
    """
    with open(filename, 'r') as f:
        node = ast.parse(f.read(), filename=filename)
    modules = set()
    for item in ast.walk(node):
        # Handle: import X or import X as Y
        if isinstance(item, ast.Import):
            for n in item.names:
                # Only keep the root module/package
                modules.add(n.name.split('.')[0])
        # Handle: from X import Y, from X.submodule import Z, etc.
        elif isinstance(item, ast.ImportFrom):
            if item.module:
                # Only keep the root module/package
                modules.add(item.module.split('.')[0])
    return modules

def scan_all_py_files(src_dir):
    """
    Recursively scan a directory for all Python (.py) files and extract their top-level imports.

    Args:
        src_dir (str): Root directory to scan (e.g. ".", "src/", etc.).

    Returns:
        Set[str]: The union of all top-level imported module/package names across all files.

    Explanation:
        - Uses os.walk to traverse directories recursively.
        - Scans any file with a '.py' extension.
        - For each Python file, uses 'find_imports_in_file' to extract imports, aggregating all unique results.
    """
    all_imports = set()
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                fpath = os.path.join(root, file)
                # Union current file's imports into running set
                all_imports |= find_imports_in_file(fpath)
    return all_imports

def read_requirements(reqfile):
    """
    Parse a requirements.txt file to extract the set of listed package names (in lower case).

    Args:
        reqfile (str): Path to the requirements.txt file.

    Returns:
        Set[str]: Set of package names as they appear in requirements.txt, stripped of version pins.
    
    Explanation:
        - Ignores empty lines and comment lines.
        - Handles basic version specifiers like '==', '>=', '<=' by splitting on the first instance.
        - Converts all names to lowercase for case-insensitive matching.
        - Does not handle complex extras or VCS installs (those may need more logic).
    """
    pkgs = set()
    with open(reqfile, 'r') as f:
        for line in f:
            line = line.strip()
            # Ignore blank lines and comments
            if line and not line.startswith('#'):
                # Split on common version specifiers to get just the base package name
                base = line.split('==')[0].split('>=')[0].split('<=')[0]
                pkgs.add(base.lower())
    return pkgs

if __name__ == "__main__":
    # ---- Configuration ----
    source_dir = "."           # "." to scan current dir, or "./src", etc.
    reqfile = "requirements.txt"
    
    # ---- Step 1: Scan codebase imports ----
    imports = scan_all_py_files(source_dir)
    print("Imports found in codebase:", sorted(imports))

    # ---- Step 2: Scan requirements.txt ----
    reqs = read_requirements(reqfile)
    print("Packages in requirements.txt:", sorted(reqs))

    # ---- Step 3: Show discrepancies ----
    print("Possibly missing in requirements.txt (used in code, not listed):", sorted(imports - reqs))
    print("Possibly unused in codebase (listed, but not imported directly):", sorted(reqs - imports))

    # ---- Notes ----
    # - 'Possibly missing in requirements.txt' points to imports in the code not listed in requirements.txt:
    #   Likely needs to be added (unless from stdlib, or a subpackage of another package).
    # - 'Possibly unused in codebase' are listed dependencies you don't seem to use:
    #   Candidates for removal, but double-check for test/dev tools, CLI utils, or runtime dynamic imports.
    # - Some packages might not match their pip name (e.g., 'PIL' is 'pillow', 'sklearn' is 'scikit-learn').
    #   For these, a mapping or manual review is recommended.
    # - This script covers most static cases but can't handle truly dynamic imports (like importlib, etc).