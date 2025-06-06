from decimal import Decimal

from flask_login import current_user

from application import LedgerItemTypeEnum, db, logger
from application.modules.accounts.models import Account
from application.modules.ledger.forms import CreateEditLedgerItemForm
from application.modules.ledger.models import LedgerItem
from application.modules.ledger.view_models import LedgerItemViewModel
from application.utils.sort_and_filter_params import SortAndFilterParams


def create_ledger_item(form: CreateEditLedgerItemForm) -> LedgerItem:
    logger.debug("Create new ledger item")
    ledger_item = LedgerItem()
    _set_ledger_item_from_form(form, ledger_item)
    ledger_item.account = current_user
    db.session.add(ledger_item)
    db.session.commit()
    return ledger_item


def get_ledger_items(sort_and_filter_params: SortAndFilterParams) -> list[LedgerItemViewModel]:
    """Get an ordered list of ledger items for the index page."""

    # Start building a query.
    query = LedgerItem.query.join(LedgerItem.account)

    # Sorting asc/desc.
    # if sort_and_filter_params.desc:
    #     order_by = desc(order_by)

    # Search query.
    if sort_and_filter_params.search:
        # todo - I think I am going to skip search for now, should create a github issue to deal with later.
        # Probably want to integrate with HTMX.
        query = query.filter(LedgerItem.description.ilike(sort_and_filter_params.search.strip()))

    # todo - eventually do pagination

    # Order by column.
    if sort_and_filter_params.order_by == "date":
        query = query.order_by(
            LedgerItem.ledger_item_date.desc() if sort_and_filter_params.desc else LedgerItem.ledger_item_date,
            LedgerItem.ledger_item_id.desc() if sort_and_filter_params.desc else LedgerItem.ledger_item_id,
        )
    if sort_and_filter_params.order_by == "amount":
        query = query.order_by(
            LedgerItem.amount.desc() if sort_and_filter_params.desc else LedgerItem.amount,
            LedgerItem.ledger_item_date.desc() if sort_and_filter_params.desc else LedgerItem.ledger_item_date,
        )
    if sort_and_filter_params.order_by == "user":
        query = query.order_by(
            Account.name.desc() if sort_and_filter_params.desc else Account.name,
            LedgerItem.ledger_item_date.desc() if sort_and_filter_params.desc else LedgerItem.ledger_item_date,
        )

    # Execute the SQL query.
    ledger_items_for_front_end = query.all()

    # Calculate the balance for each row and put into view model
    result: list[LedgerItemViewModel] = []
    all_ledger_items_in_order = LedgerItem.query.order_by(LedgerItem.ledger_item_date, LedgerItem.ledger_item_id).all()
    for current_ledger_item in ledger_items_for_front_end:
        # todo - this seems inefficient
        balance = 0
        for previous_item in all_ledger_items_in_order:
            balance += previous_item.amount
            if current_ledger_item.ledger_item_id == previous_item.ledger_item_id:
                break

        result.append(
            LedgerItemViewModel(
                current_ledger_item.ledger_item_id,
                current_ledger_item.ledger_item_type,
                current_ledger_item.ledger_item_date,
                current_ledger_item.amount,
                current_ledger_item.description,
                created_by_user=current_ledger_item.account.name,
                balance=Decimal(balance),
            ),
        )

    return result


def prefill_edit_ledger_item_form_values(form: CreateEditLedgerItemForm, ledger_item_id: int) -> None:
    ledger_item = LedgerItem.query.get_or_404(ledger_item_id)
    form.ledger_item_id.data = ledger_item.ledger_item_id
    form.ledger_item_type.data = ledger_item.ledger_item_type
    form.description.data = ledger_item.description
    form.ledger_item_date.data = ledger_item.ledger_item_date
    form.amount.data = ledger_item.amount


def _set_ledger_item_from_form(form: CreateEditLedgerItemForm, ledger_item: LedgerItem) -> None:
    ledger_item.ledger_item_type = form.ledger_item_type.data
    ledger_item.ledger_item_date = form.ledger_item_date.data
    ledger_item.description = form.description.data
    if form.ledger_item_type.data == LedgerItemTypeEnum.DEBIT:
        adjusted_amount = Decimal(float(form.amount.data) * -1.0)
        ledger_item.amount = adjusted_amount
    else:
        ledger_item.amount = Decimal(form.amount.data)


def delete_ledger_item(ledger_item_id: int) -> None:
    ledger_item = LedgerItem.query.get_or_404(ledger_item_id)
    logger.info(
        f"{current_user.username} ({current_user.account_id}) is deleting ledger item {ledger_item.ledger_item_id} /"
        f"\n{ledger_item.description}",
    )
    db.session.delete(ledger_item)
    db.session.commit()


def edit_ledger_item(form: CreateEditLedgerItemForm) -> None:
    logger.info(
        f"{current_user.username} ({current_user.account_id}) is editing ledger item {form.ledger_item_id.data}",
    )
    ledger_item = LedgerItem.query.get_or_404(form.ledger_item_id.data)
    _set_ledger_item_from_form(form, ledger_item)
    db.session.commit()
