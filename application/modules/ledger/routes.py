from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.typing import ResponseReturnValue

from application import ClearanceEnum, CrudEnum
from application.modules.accounts.requires_clearance import requires_clearance
from application.modules.ledger.forms import CreateEditLedgerItemForm
from application.modules.ledger.services import (
    create_ledger_item,
    delete_ledger_item,
    edit_ledger_item,
    get_ledger_items,
    prefill_edit_ledger_item_form_values,
)
from application.utils.sort_and_filter_params import SortAndFilterParams

ledger = Blueprint("ledger", __name__, url_prefix="/ledger")


@ledger.route("/")
@requires_clearance(ClearanceEnum.NORMAL)
def index() -> ResponseReturnValue:
    sort_and_filter_params = SortAndFilterParams()
    ledger_items = get_ledger_items(sort_and_filter_params)
    return render_template(
        "ledger/index.html",
        ledger_items=ledger_items,
        sort_and_filter_params=sort_and_filter_params,
    )


@ledger.route("/create", methods=["GET", "POST"])
@requires_clearance(ClearanceEnum.ADMIN)
def create() -> ResponseReturnValue:
    form = CreateEditLedgerItemForm()
    if form.validate_on_submit():
        create_ledger_item(form)
        # possible enhancement for later - save and add another?
        flash("Ledger item created successfully.", "success")
        return redirect(url_for("ledger.index"))

    return render_template("ledger/create_edit.html", mode=CrudEnum.CREATE, form=form)


@ledger.route("/edit/<int:ledger_item_id>", methods=["GET", "POST"])
@requires_clearance(ClearanceEnum.ADMIN)
def edit(ledger_item_id: int) -> ResponseReturnValue:
    form = CreateEditLedgerItemForm()
    if form.validate_on_submit():
        edit_ledger_item(form)
        flash("Ledger item edited successfully.", "success")
        return redirect(url_for("ledger.index"))
    if request.method == "GET":
        prefill_edit_ledger_item_form_values(form, ledger_item_id)
    return render_template("ledger/create_edit.html", mode=CrudEnum.UPDATE, form=form)


@ledger.route("/delete/<int:ledger_item_id>", methods=["POST"])
@requires_clearance(ClearanceEnum.ADMIN)
def delete(ledger_item_id: int) -> ResponseReturnValue:
    # theoretically I should be using a form and validating CSRF token, shouldn't really be necessary here
    delete_ledger_item(ledger_item_id)
    flash("Ledger item deleted successfully.", "success")
    return redirect(url_for("ledger.index"))
