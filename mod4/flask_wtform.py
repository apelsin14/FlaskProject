from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, Field
from wtforms.validators import InputRequired, Email, NumberRange, Optional, ValidationError

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    phone = IntegerField(validators=[InputRequired(), NumberRange(min=1000000000, max=9999999999)])
    name = StringField(validators=[InputRequired()])
    address = StringField(validators=[InputRequired()])
    index = IntegerField(validators=[InputRequired(), NumberRange(min=100000, max=999999)])
    comment = StringField(validators=[InputRequired()])


def number_length(min: int, max: int, message: Optional[str] = None):

    def _number_length(form: FlaskForm, field: Field):
        if len(str(field.data)) < min or len(str(field.data)) > max or field.data <= 0:
            raise ValidationError(massage=message)

    return _number_length


class NumberLength:
    def __init__(self, min: int, max: int, message: Optional = ''):
        self.min = min
        self.max = max
        self.massage = message

    def __call__(self, form: FlaskForm, field: Field):
        if len(str(field.data)) < self.min or len(str(field.data)) > self.max or field.data <= 0:
            raise ValidationError(message=self.massage)


number = IntegerField(validators=[InputRequired(), NumberLength()])


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        phone = form.phone.data
        name = form.name.data
        address = form.address.data
        index = form.index.data
        comment =  form.comment.data
        return f"Successfully registered user {email} with phone +7{phone}, name: {name}, address: {address}, index: {index}, comment: {comment}"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)

#endpoitn_registration