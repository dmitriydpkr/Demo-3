from marshmallow import Schema, fields, ValidationError, validates, post_dump, post_load


def must_not_be_blank(value):
    if not value:
        raise ValidationError("Data not provided.")


class PaymentSchema(Schema):
    id = fields.UUID(required=True, validate=must_not_be_blank, nullable=False)
    contributor = fields.String(validate=must_not_be_blank)
    amount = fields.Float(default=0)
    date = fields.LocalDateTime(validate=must_not_be_blank)
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
    def validate_contributor(self, contributor):
        if len(contributor) > 30:
            raise ValidationError("Too much symbols")

    @post_load
    def to_model(self, data):
        return data


row = {
    "id": "d90667f8-7fa8-42c5-b47e-e6a0b8e03fed",
    "contributor": "d9999999",
    "amount": 28.55,
    "date": "2019-05-04 05:34:05.287928-04",
    "contract_id": "00643a49-be89-4c49-8378-6148482ac0bd",
}

try:
    rows = PaymentSchema().load(row)
except ValidationError as error:
    print(error)
