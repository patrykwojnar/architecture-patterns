from dataclasses import dataclass
from typing import Optional
from datetime import date

"""
Use Case: To reduce information about out-of-stock products during purchases, 
orders will also be allocated in restock batches with details 
about the extended delivery time, which will result in higher sales 
and lower storage costs.
"""


@dataclass(frozen=True)
class OrderLine:
    orderID: str
    sku: str
    qty: int


class RestockBatch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference_code = ref
        self.sku = sku  # stock keeping unit
        self.available_quantity = qty
        self.eta = eta  # estimated time of arrival

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self.available_quantity -= line.qty

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
