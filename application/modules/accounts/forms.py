from __future__ import annotations

from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy import and_, func
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError

from application.modules.accounts.models import Account
from application.utils.form_filters import lowercase

username_length = Length(min=2, max=24)
name_length = Length(min=2, max=32)
password_length = Length(min=4, max=4)
email_length = Length(min=5, max=42)


class CreateOrEditAccountFormBase(FlaskForm):
    """Just the base - inherit this in create and edit"""

    name = StringField(
        "Name",
        validators=[DataRequired(), name_length],
        render_kw={
            "autofocus": "true",
            "spellcheck": "false",
            "autocorrect": "off",
        },
    )
    email = StringField(
        "Email",
        validators=[Email()],
        filters=[lowercase],
        render_kw={
            "spellcheck": "false",
            "autocorrect": "off",
            "autocapitalize": "off",
        },
        description="Your email address to be used for notifications and password resets.",
    )
    username = StringField(
        "Username",
        validators=[DataRequired(), username_length],
        filters=[lowercase],
        description="A unique username to you that you can remember. This is not displayed to others.",
        render_kw={
            "spellcheck": "false",
            "autocorrect": "off",
            "autocomplete": "off",
            "autocapitalize": "off",
        },
    )


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), username_length],
        description="Your unique username.",
        render_kw={
            "autofocus": "true",
            "spellcheck": "false",
            "autocorrect": "off",
            "autocapitalize": "off",
        },
    )
    password = PasswordField(
        "PIN",
        validators=[DataRequired(), password_length],
        render_kw={"inputmode": "numeric", "pattern": "[0-9]*"},
    )
    # remember = BooleanField("Remember Me", default=True)
    submit = SubmitField("Log In")

    # @staticmethod
    # def validate_username(_, username):
    #     if not Account.query.filter(func.lower(Account.username) == func.lower(username.data)).count():
    #         raise ValidationError("Doesn't exist.")


class CreateAccountForm(CreateOrEditAccountFormBase):
    password = PasswordField(
        "PIN",
        validators=[DataRequired(), password_length],
        description="A 4-digit PIN that you can easily remember",
        render_kw={"inputmode": "numeric", "pattern": "[0-9]*"},
    )
    confirm_password = PasswordField(
        "Confirm PIN",
        validators=[DataRequired(), password_length, EqualTo("password", "Your PINs must match.")],
        description="Type in your PIN again to confirm it's correct.",
        render_kw={"inputmode": "numeric", "pattern": "[0-9]*"},
    )
    submit = SubmitField("Create Account")

    @staticmethod
    def validate_username(_: CreateAccountForm, username: StringField) -> None:
        if Account.query.filter(func.lower(Account.username) == username.data).all():
            raise ValidationError("That username has already been taken.")

        # Forbidden usernames.
        if username.data in ["anon", "admin"]:
            raise ValidationError("That username is not allowed.")

    @staticmethod
    def validate_email(_: CreateAccountForm, email: StringField) -> None:
        if Account.query.filter(func.lower(Account.email) == email.data).all():
            raise ValidationError("That email has already been used.")


# if we allowed editing name, then CreateOrEditFormBase will be used, until then don't inherit
# class EditAccountForm(CreateOrEditFormBase):
class EditAccountForm(CreateOrEditAccountFormBase):
    password = PasswordField(
        "PIN",
        validators=[Optional(), password_length],
        render_kw={"inputmode": "numeric", "pattern": "[0-9]*"},
    )
    confirm_password = PasswordField(
        "Confirm PIN",
        validators=[EqualTo("password", "Your PINs must match.")],
        render_kw={"inputmode": "numeric", "pattern": "[0-9]*"},
    )
    submit = SubmitField("Save Changes")

    @staticmethod
    def validate_username(_: EditAccountForm, username: StringField) -> None:
        # Check if it already exists.
        if Account.query.filter(
            and_(
                func.lower(Account.username) == func.lower(username.data),  # Has same username, and...
                Account.account_id != current_user.account_id,  # has same account id.
            ),
        ).all():
            raise ValidationError("That username has already been taken.")

        # Forbidden usernames.
        if username.data in ["anon", "admin"]:
            raise ValidationError("That username is not allowed.")

    @staticmethod
    def validate_email(_: EditAccountForm, email: StringField) -> None:
        if Account.query.filter(
            and_(
                func.lower(Account.email) == func.lower(email.data),  # Has same email, and...
                Account.account_id != current_user.account_id,  # has same account id.
            ),
        ).all():
            raise ValidationError("That email has already been used.")
