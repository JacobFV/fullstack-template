from typing import Any, Optional
from app.api.deps import SessionDep, get_db, MaybeCurrentUserDep
from app.schema.proof_of_id_verification import (
    ModelBase,
    ModelCreate,
    ModelInDB,
    ModelRead,
    ModelUpdate,
)
from backend.app.schema.id import ID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session


def build_crud_endpoints(
    t_model_base: type[ModelBase],
    t_model_create: type[ModelCreate] = None,
    t_model_read: type[ModelRead] = None,
    t_model_update: type[ModelUpdate] = None,
    t_model_in_db: type[ModelInDB] = None,
    implement_create=True,
    implement_read=True,
    implement_update=True,
    implement_delete=True,
    router: APIRouter = None,
):
    if router is None:
        router = APIRouter()

    t_model_base.ModelCreate = t_model_create
    t_model_base.ModelUpdate = t_model_update
    t_model_base.ModelRead = t_model_read
    t_model_base.ModelInDB = t_model_in_db

    if implement_create and not t_model_create is not None:

        @router.post(
            "/",
            response_model=t_model_read,
            response_description=f"The created {t_model_base.__name__}",
            status_code=201,
            tags=[t_model_base.__name__],
            responses={
                201: {
                    "description": f"The created {t_model_base.__name__}",
                    "model": t_model_read,
                },
                401: {
                    "description": "Unauthorized",
                    "model": HTTPException,
                },
                403: {
                    "description": "Forbidden",
                    "model": HTTPException,
                },
            },
        )
        async def create_one(
            item: t_model_create, session: SessionDep, user: MaybeCurrentUserDep
        ):
            item_in_db = t_model_in_db.from_create(item, session=session, user=user)
            return item_in_db.to_read(user=user)

        @router.post(
            "/multiple",
            response_model=list[t_model_read],
            response_description=f"The created {t_model_base.__name__}s",
            status_code=201,
            tags=[t_model_base.__name__],
            responses={
                201: {
                    "description": f"The created {t_model_base.__name__}s",
                    "model": list[t_model_read],
                },
                401: {
                    "description": "Unauthorized",
                    "model": HTTPException,
                },
                403: {
                    "description": "Forbidden",
                    "model": HTTPException,
                },
            },
        )
        async def create_multiple(
            items: list[t_model_create],
            session: SessionDep,
            user: MaybeCurrentUserDep,
        ):
            return [
                t_model_in_db.from_create(item, session=session, user=user).to_read(
                    user=user
                )
                for item in items
            ]

    if implement_read and not t_model_read is not None:

        @router.get(
            "/{id}",
            response_model=t_model_read,
            response_description=f"The {t_model_base.__name__}",
            status_code=200,
            tags=[t_model_base.__name__],
            responses={
                200: {
                    "description": f"The {t_model_base.__name__}",
                    "model": t_model_read,
                },
                401: {
                    "description": "Unauthorized",
                    "model": HTTPException,
                },
                403: {
                    "description": "Forbidden",
                    "model": HTTPException,
                },
                404: {
                    "description": "Not found",
                    "model": HTTPException,
                },
            },
        )
        async def read_one(id: ID, session: SessionDep, user: MaybeCurrentUserDep):
            item_in_db = t_model_in_db.find_by_id(id, session=session)
            if not item_in_db:
                raise HTTPException(status_code=404, detail="Item not found")
            return item_in_db.to_read(user=user)

        @router.get(
            "/{id}/{field}",
            response_model=t_model_read,
            response_description=f"The {t_model_base.__name__}",
            status_code=200,
            tags=[t_model_base.__name__],
            responses={
                200: {
                    "description": f"The {t_model_base.__name__}",
                    "model": t_model_read,
                },
                401: {
                    "description": "Unauthorized",
                    "model": HTTPException,
                },
                403: {
                    "description": "Forbidden",
                    "model": HTTPException,
                },
                404: {
                    "description": "Not found",
                    "model": HTTPException,
                },
            },
        )
        async def read_one_field(
            id: ID, field: str, session: SessionDep, user: MaybeCurrentUserDep
        ):
            read_model = implement_read(id, session=session, user=user)
            if not hasattr(read_model, field):
                raise HTTPException(status_code=404, detail="Field not found")
            return getattr(read_model, field)

        @router.get(
            "/multiple",
            response_model=list[t_model_read],
            response_description=f"The {t_model_base.__name__}s",
            status_code=200,
            tags=[t_model_base.__name__],
            responses={
                200: {
                    "description": f"The {t_model_base.__name__}s",
                    "model": list[t_model_read],
                },
                401: {
                    "description": "Unauthorized",
                    "model": HTTPException,
                },
                403: {
                    "description": "Forbidden",
                    "model": HTTPException,
                },
                404: {
                    "description": "Not found",
                    "model": HTTPException,
                },
            },
        )
        async def read_multiple(
            ids: list[int], session: SessionDep, user: MaybeCurrentUserDep
        ):
            items_in_db = t_model_in_db.find_by_ids(ids, session=session)
            return [item.to_read(user=user) for item in items_in_db]

        @router.get(
            "/",
            response_model=list[t_model_read],
            response_description=f"The {t_model_base.__name__}s",
            status_code=200,
            tags=[t_model_base.__name__],
            responses={
                200: {
                    "description": f"The {t_model_base.__name__}s",
                    "model": list[t_model_read],
                },
                401: {
                    "description": "Unauthorized",
                    "model": HTTPException,
                },
                403: {
                    "description": "Forbidden",
                    "model": HTTPException,
                },
                404: {
                    "description": "Not found",
                    "model": HTTPException,
                },
            },
        )
        async def read_all(session: SessionDep, user: MaybeCurrentUserDep):
            all_items_in_db = t_model_in_db.find_all(session=session)
            return [item.to_read(user=user) for item in all_items_in_db]

    if implement_update and not t_model_update is not None:

        @router.put(
            "/{id}",
            response_model=t_model_read,
            response_description=f"Updated {t_model_base.__name__}",
            status_code=200,
            tags=[t_model_base.__name__],
            responses={
                200: {
                    "description": f"Updated {t_model_base.__name__}",
                    "model": t_model_read,
                },
                400: {
                    "description": "Bad Request",
                    "model": HTTPException,
                },
                401: {
                    "description": "Unauthorized",
                    "model": HTTPException,
                },
                403: {
                    "description": "Forbidden",
                    "model": HTTPException,
                },
                404: {
                    "description": "Not found",
                    "model": HTTPException,
                },
            },
        )
        async def update_one(
            id: ID,
            update_data: t_model_update,
            session: SessionDep,
            user: MaybeCurrentUserDep,
        ):
            item_in_db = t_model_in_db.find_by_id_or_raise(id, session)
            item_in_db.update_from(update_data, session, user)
            return item_in_db.to_read(user=user)

        @router.patch(
            "/{id}/{field_name}",
            response_model=t_model_read,
            response_description=f"Partially updated {t_model_base.__name__}",
            status_code=200,
            tags=[t_model_base.__name__],
            responses={
                200: {
                    "description": f"Partially updated {t_model_base.__name__}",
                    "model": t_model_read,
                },
                400: {
                    "description": "Bad Request",
                    "model": HTTPException,
                },
                401: {
                    "description": "Unauthorized",
                    "model": HTTPException,
                },
                403: {
                    "description": "Forbidden",
                    "model": HTTPException,
                },
                404: {
                    "description": "Not found",
                    "model": HTTPException,
                },
            },
        )
        async def update_one_field(
            id: ID,
            field_name: str,
            field_value: Any,
            session: SessionDep,
            user: MaybeCurrentUserDep,
        ):
            update_one(
                id,
                update_data={field_name: field_value},
                session=session,
                user=user,
            )

        @router.put(
            "/",
            response_model=list[t_model_read],
            response_description=f"Updated multiple {t_model_base.__name__}s",
            status_code=200,
            tags=[t_model_base.__name__],
            responses={
                200: {
                    "description": f"Updated multiple {t_model_base.__name__}s",
                    "model": list[t_model_read],
                },
                400: {
                    "description": "Bad Request",
                    "model": HTTPException,
                },
                401: {
                    "description": "Unauthorized",
                    "model": HTTPException,
                },
                403: {
                    "description": "Forbidden",
                    "model": HTTPException,
                },
                404: {
                    "description": "Not found",
                    "model": HTTPException,
                },
            },
        )
        async def update_multiple(
            ids: list[int],
            update_data: t_model_update,
            session: SessionDep,
            user: MaybeCurrentUserDep,
        ):
            items_in_db = t_model_in_db.find_by_ids(ids, session)
            for item in items_in_db:
                item.update_from(update_data, session, user)
            return [item.to_read(user=user) for item in items_in_db]

    if implement_delete:

        @router.delete(
            "/{id}",
            response_model=t_model_read,
            response_description=f"Deleted {t_model_base.__name__}",
            status_code=200,
            tags=[t_model_base.__name__],
            responses={
                200: {
                    "description": f"Deleted {t_model_base.__name__}",
                    "model": t_model_read,
                },
                400: {
                    "description": "Bad Request",
                    "model": HTTPException,
                },
                401: {
                    "description": "Unauthorized",
                    "model": HTTPException,
                },
                403: {
                    "description": "Forbidden",
                    "model": HTTPException,
                },
                404: {
                    "description": "Not found",
                    "model": HTTPException,
                },
            },
        )
        async def delete_one(id: ID, session: SessionDep, user: MaybeCurrentUserDep):
            item_in_db = t_model_in_db.find_by_id_or_raise(id, session)
            item_in_db.delete(session)
            return item_in_db.to_read(user=user)

        @router.delete(
            "/",
            response_model=list[t_model_read],
            response_description=f"Deleted multiple {t_model_base.__name__}s",
            status_code=200,
            tags=[t_model_base.__name__],
            responses={
                200: {
                    "description": f"Deleted multiple {t_model_base.__name__}s",
                    "model": list[t_model_read],
                },
                400: {
                    "description": "Bad Request",
                    "model": HTTPException,
                },
                401: {
                    "description": "Unauthorized",
                    "model": HTTPException,
                },
                403: {
                    "description": "Forbidden",
                    "model": HTTPException,
                },
                404: {
                    "description": "Not found",
                    "model": HTTPException,
                },
            },
        )
        async def delete_multiple(
            ids: list[int], session: SessionDep, user: MaybeCurrentUserDep
        ):
            items_in_db = t_model_in_db.find_by_ids(ids, session)
            for item in items_in_db:
                item.delete(session)
            return [item.to_read(user=user) for item in items_in_db]

    return router
