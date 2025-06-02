from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from application import LedgerItemTypeEnum


@dataclass
class LedgerItemViewModel:
    ledger_item_id: int
    ledger_item_type: LedgerItemTypeEnum
    ledger_item_date: date
    amount: Decimal
    description: str
    balance: Decimal
    created_by_user: str
