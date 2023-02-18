from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware #this is used to allow cross origin requests from the frontend to the backend so that the frontend can access the backend since frontend will have 3000 port and backend will have 8000 port
from model import Todo
from database import fetch_one_todo, fetch_all_todo, create_todo, update_todo, delete_todo

app =FastAPI()

origins=["http://localhost:5173","http://192.168.0.111:5173"] #this means that the frontend will be running on port 5173

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["ROOT"])
async def read_root():
    return {"message": "Welcome to this Gawdly App!"}

@app.get("/api/todo")
async def get_todo():
    response=await fetch_all_todo()
    return response

@app.get("api/todo/{title}" , response_model=Todo)
async def get_todo_by_title(title):
    response =await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404,f"There is no todo with title as '{title}'")
    

@app.post("/api/todo" , response_model=Todo)
async def create_todos(todo:Todo):
    response = await create_todo(todo.dict()) 
    if response:
        return response
    raise HTTPException(404, f"Todo with title '{todo.title}' already exists")
    

@app.put("/api/todo/{title}" , response_model=Todo)
async def update_todo_by_title(title:str, desc:str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404,f"There is no todo with the title as '{title}")
    

@app.delete("/api/todo/{title}")
async def delete_todo_by_title(title:str):
    response = await delete_todo(title)
    if response:
        return {"message": f"Todo with title '{title}' is deleted successfully"}
    raise HTTPException(404,f"There is no todo with the title as '{title}'")