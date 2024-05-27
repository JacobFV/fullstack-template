from typing import ClassVar, Generic, TypeVar
from attrs import define

T = TypeVar("T")


@define
class Money(Generic[T]):
    T: ClassVar[type] = int
    amount: T
    currency: str = "USD cents"

# class Invoice(BaseModel):
#     pass
