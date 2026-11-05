"""Validation script run by GitHub Actions."""
import pathlib
import py_compile
import subprocess
import sys

failed = False

# 1. Syntax-check every Python file in the repo
for f in pathlib.Path(".").rglob("*.py"):
    if ".git" in f.parts:
        continue
    try:
        py_compile.compile(str(f), doraise=True)
        print(f"OK      {f}")
    except py_compile.PyCompileError as e:
        print(f"FAILED  {f}\n{e.msg}")
        failed = True

# 2. Make sure product.py runs without errors
result = subprocess.run([sys.executable, "product.py"], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(f"product.py exited with {result.returncode}\n{result.stderr}")
    failed = True

if failed:
    sys.exit(1)
print("All validations passed.")
