from fastapi import APIRouter

from routes.users import UsersRouter


class RootRouter(APIRouter):
    def __init__(self):
        super().__init__()
        self.include_router(UsersRouter(), prefix="/api/v1")
