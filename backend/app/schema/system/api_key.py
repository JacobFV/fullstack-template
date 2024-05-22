from datetime import datetime
from app.schema.crud_base import CRUDBase
from app.schema.system.billing import Money
from app.schema.user.developer import DeveloperBase


class APIKeyBase(CRUDBase):

    created_at: datetime
    expires_at: datetime
    owner: DeveloperBase
    scopes: list[str]
    uses: list[APIKeyUse]
    spend_limit: Money[int].T


class APIKeyUseBase(BaseModel):
    pass


# WIP
