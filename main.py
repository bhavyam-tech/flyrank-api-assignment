from fastapi import FastAPI
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url=os.getenv("DATABASE_URL")
conn=psycopg2.connect(db_url)

# This creates your server application
app = FastAPI()

# This is your first endpoint
@app.get("/")
def read_root():
    return {"message": "Hello! My backend is working."}

# This is your second endpoint
@app.get("/data")
def get_data():
    cur=conn.cursor()
    cur.execute("SELECT * FROM assignments WHERE assignment = 'BE-01';")
    result = cur.fetchone()

    return {"assignment": result[0], "status": result[1]}

# This is my Third endpoint
@app.get("/profile")
def get_profile():
    return{"message": "Hi, Welcome Bhavyam Rajguru!",
           "next line" :"Welcome to your Backend track of you internship"
           }