import uvicorn
from fastapi import FastAPI
from backend import routes

app=FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

app.include_router(routes.app)

if __name__=="__main__":
    uvicorn.run('main:app',port=5000)