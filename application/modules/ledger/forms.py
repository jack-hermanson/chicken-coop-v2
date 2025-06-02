from datetime import date

from flask_wtf import FlaskForm
from wtforms.fields import DateField, DecimalField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import AnyOf, DataRequired, Length, NumberRange, Optional
from wtforms.widgets.core import HiddenInput

from application import LedgerItemTypeEnum


class CreateEditLedgerItemForm(FlaskForm):
    # only for edit
    ledger_item_id = IntegerField(validators=[Optional()], widget=HiddenInput())

    ledger_item_type = SelectField(
        "Ledger Item Type",
        coerce=int,
        choices=[
            (0, "Select..."),
            (LedgerItemTypeEnum.DEBIT, "- Debit (Expense)"),
            (LedgerItemTypeEnum.CREDIT, "+ Credit (Income)"),
        ],
        validators=[
            AnyOf(
                [
                    LedgerItemTypeEnum.DEBIT,
                    LedgerItemTypeEnum.CREDIT,
                ],
            ),
            DataRequired(),
        ],
    )
    ledger_item_date = DateField("Ledger Item Date", validators=[DataRequired()], default=date.today)
    amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=0, max=10_000)])
    description = StringField("Description", validators=[DataRequired(), Length(min=3, max=255)])
    submit = SubmitField("Create" if ledger_item_id is None else "Save Changes")
