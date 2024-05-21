from typing import Optional
from app.schema import CRUDBase, CRUDCreate, CRUDInDB, CRUDRead, CRUDUpdate
from fastapi import APIRouter


def register_crud_endpoints(
    router: APIRouter,
    model_base: type[CRUDBase],
    model_create: type[CRUDCreate] = CRUDCreate,
    model_read: type[CRUDRead] = CRUDRead,
    model_update: type[CRUDUpdate] = CRUDUpdate,
    model_in_db: type[CRUDInDB] = CRUDInDB,
    create=True,
    read=True,
    update=True,
    delete=True,
):
    if create:

        @router.post("/")
        async def create(item: model_create):
            pass

    if read:

        @router.get("/{id}")
        async def read(id: UUID):
            pass

    if update:

        @router.put("/{id}")
        async def update(id: UUID, item: model_update):
            pass

    if delete:

        @router.delete("/{id}")
        async def delete(id: UUID):
            pass
