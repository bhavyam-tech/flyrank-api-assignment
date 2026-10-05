from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

# ----- Database Setup -----
DB_FILE = "tasks.db"

def get_conn():
    """Opens a new connection to tasks.db for each request."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Makes results dict-like (e.g. row["title"])
    return conn

def init_db():
    """Creates the tasks table and seeds 3 example tasks on first run."""
    conn = get_conn()
    cursor = conn.cursor()
    
    # Create table if it doesn't exist yet
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT    NOT NULL,
            done  BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    
    # Only insert examples if the table is completely empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    if count == 0:
        example_tasks = [
            ("Buy groceries", 0),
            ("Read a book",   0),
            ("Complete assignment", 0),
        ]
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            example_tasks
        )
    
    conn.commit()
    conn.close()

# Run database setup when the app starts
init_db()

# ----- FastAPI App -----
app = FastAPI()

# Model for request body when creating/updating a task
class TaskIn(BaseModel):
    title: str
    done: bool = False   # defaults to False (not done)

# ----- Endpoints -----

@app.get("/")
def root():
    return {"message": "Hello! My backend is working."}

@app.get("/profile")
def get_profile():
    return {
        "message": "Hi, Welcome Bhavyam Rajguru!",
        "next_line": "Welcome to your Backend track of your internship"
    }

# Stage 1 — Read all tasks
@app.get("/tasks")
def get_all_tasks():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    # Convert each row to a plain dict
    return [dict(row) for row in rows]

# Stage 1 — Read one task by id
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return dict(row)

# Stage 2 — Create a new task
@app.post("/tasks", status_code=201)
def create_task(task: TaskIn):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, int(task.done))
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "title": task.title, "done": task.done}

# Stage 3 — Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskIn):
    conn = get_conn()
    cursor = conn.cursor()
    # First check the task exists
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (task.title, int(task.done), task_id)
    )
    conn.commit()
    conn.close()
    return {"id": task_id, "title": task.title, "done": task.done}

# Stage 3 — Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_conn()
    cursor = conn.cursor()
    # First check the task exists
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"message": f"Task {task_id} deleted successfully"}