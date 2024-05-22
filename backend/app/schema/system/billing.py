from typing import ClassVar, Generic, TypeVar
from attrs import define

T = TypeVar("T")


@define
class Money(Generic[T]):
    T: ClassVar[type] = int
    currency: str = "USD cents"
    amount: T


# class Invoice(BaseModel):
#     pass
