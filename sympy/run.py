import uvicorn
import os

APP_ENV = os.getenv("APP_ENV", "development")

if __name__ == "__main__":
    if APP_ENV == "development":
        print("Running in development mode.")
        uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True)
    else:
        print("Running in production mode.")
        uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=False)