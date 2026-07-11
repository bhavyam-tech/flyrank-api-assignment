from fastapi import FastAPI

# Creating server application
app = FastAPI()

# First endpoint
@app.get("/")
def read_root():
    return {"message": "Hello! My backend is working."}

# Second endpoint
@app.get("/data")
def get_data():
    return {"assignment": "BE-01", "status": "In Progress"}
