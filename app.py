# app.py - Dummy redirect file for Railway hardcoded command
# This tricks Railway into finding 'app' while running the real main.py

from main import app  # Import the FastAPI instance from your real main.py

# If you want to add any extra config or logging, do it here
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), workers=2)
