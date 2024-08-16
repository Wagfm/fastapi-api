from fastapi import FastAPI

from routes.root import RootRouter

app = FastAPI()
app.include_router(RootRouter())
