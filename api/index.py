from fastapi import FastAPI
import os
import sys

app = FastAPI()

@app.get("/api/{path:path}")
async def debug_env(path: str):
    try:
        # List files in current directory and parent directory
        cwd = os.getcwd()
        files_in_cwd = os.listdir(cwd)
        
        parent = os.path.dirname(cwd)
        files_in_parent = os.listdir(parent) if os.path.exists(parent) else "Parent not accessible"
        
        # Try importing backend
        import_status = "Not attempted"
        try:
            sys.path.append(os.path.join(cwd)) # Add root to path
            from backend.main import app as backend_app
            import_status = "Success"
        except Exception as e:
            import_status = f"Failed: {str(e)}"

        return {
            "status": "Debug Mode",
            "cwd": cwd,
            "files_in_cwd": files_in_cwd,
            "parent_dir": parent,
            "files_in_parent": files_in_parent,
            "sys_path": sys.path,
            "import_backend_status": import_status
        }
    except Exception as e:
        return {"error": str(e)}
