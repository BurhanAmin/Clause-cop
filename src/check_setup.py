import sys 
import pymupdf

print("Python version:", sys.version.split()[0])
print("PyMuPDF version:", pymupdf.__version__)
print("Running inside venv:", sys.prefix != sys.base_prefix )