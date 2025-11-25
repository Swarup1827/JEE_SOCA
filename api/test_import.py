import sys
import os

# Mimic the logic in api/index.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

print(f"Current dir: {current_dir}")
print(f"Parent dir: {parent_dir}")
print(f"Sys path: {sys.path}")

try:
    from backend.main import app
    print("Successfully imported app from backend.main")
except Exception as e:
    print(f"Failed to import: {e}")
    import traceback
    traceback.print_exc()
