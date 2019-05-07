from marshmallow import Schema, fields, ValidationError, validates, post_dump, post_load


def must_not_be_blank(value):
    if not value:
        raise ValidationError("Data not provided.")


class PaymentSchema(Schema):
    id = fields.UUID(required=True, validate=must_not_be_blank, nullable=False)
    contributor = fields.String(validate=must_not_be_blank)
    amount = fields.Float(default=0)
    date = fields.DateTime(default=0, validate=must_not_be_blank)
    period = fields.Integer(default=0, validate=must_not_be_blank)
    contract_id = fields.UUID(
        required=True,
        validate=must_not_be_blank,
        error_meassages={"required": "Contact ID is required."},
    )

    @validates("amount")
    def validate_amount(self, amount):
        if not float(amount):
            raise ValidationError("Amount have wrong format. Only whole numbers.")

    @validates("contributor")
    def validate_amount(self, contributor):
        if len(contributor) > 30:
            raise ValidationError("Too much symbols")

    @post_load
    def to_model(self, data):
        return data


row = {
    "id": "00643a49-be89-4c49-8376-6148482ac0bd",
    "contributor": "d9999999",
    "amount": 31.55,
    "date": "2019-05-04 05:34:05.287928-04",
    "period": 1557168899,
    "contract_id": "9d2b1d1c-b835-4f8d-9f0a-66d38eb602c0",
}

try:
    rows = PaymentSchema().load(row)
except ValidationError as error:
    print(error)
