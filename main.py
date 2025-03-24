import uvicorn
from fastapi import FastAPI
from handlers import routes

app = FastAPI()

for route in routes:
    app.include_router(route)



# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)