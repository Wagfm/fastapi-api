from fastapi import APIRouter

from controllers.users import UsersController


class UsersRouter(APIRouter):
    def __init__(self):
        super().__init__(prefix="/users")
        self._controller = UsersController()
        self._setup_routes()

    def _setup_routes(self):
        self.post("/")(self._controller.create)
        self.get("/{id:str}")(self._controller.read_by_id)
