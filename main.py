from fastapi import FastAPI

# This creates your server application
app = FastAPI()

# This is your first endpoint
@app.get("/")
def read_root():
    return {"message": "Hello! My backend is working."}

# This is your second endpoint
@app.get("/data")
def get_data():
    return {"assignment": "BE-01", "status": "In Progress"}
