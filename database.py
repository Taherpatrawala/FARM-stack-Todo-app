import motor.motor_asyncio 
from model import Todo
 

client= motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/")
database=client.TodoApp #here TodoApp is the name of the database
collection= database.todo #here todo is the name of the collection and collection means table in mongodb

async def fetch_one_todo(title):
    document= await collection.find_one({"title":title})
    return document

async def fetch_all_todo():
    todos=[]
    cursor=collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos

async def create_todo(todo):
    document = todo
    result = await collection.insert_one(document)
    return document

async def update_todo(title,desc):
    await collection.update_one({"title":title},{"$set":{"description":desc}}) #$set is a mongodb operator which is used to update the value of a field
    document = await collection.find_one({"title":title})
    return document

async def delete_todo(title):
    await collection.delete_one({"title":title})
    return True #here we are returning true because we are not getting any response from mongodb after deleting the document and True means the document is deleted
