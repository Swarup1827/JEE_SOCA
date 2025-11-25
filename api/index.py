import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.main import app
except Exception as e:
    # Fallback app to display error in browser
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse
    import traceback
    
    app = FastAPI()
    
    @app.get("/api/{path:path}")
    async def catch_all(path: str):
        error_msg = f"Server Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        return PlainTextResponse(error_msg, status_code=500)
