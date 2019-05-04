from marshmallow import Schema, fields, ValidationError, validates


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class PaymentSchema(Schema):
    id = fields.Integer(required=True, validate=must_not_be_blank)
    contributor = fields.String(validate=must_not_be_blank)
    amount = fields.Float(default=0)
    period = fields.LocalDateTime(validate=must_not_be_blank)
    date = fields.Integer(default=0)
    contragent_id = fields.Integer(required=True, validate=must_not_be_blank)
    contract_id = fields.Integer(required=True, validate=must_not_be_blank,
                                 error_meassages={'required': 'Contact ID is required.'})

    @validates('amount')
    def validate_amount(self, amount):
        if amount < 0:
            raise ValidationError("Only positive numbers")

    @validates('amount')
    def validate_amount(self, amount):
        if not int(amount):
            raise ValidationError("Amount have wrong format. Only integer numbers.")

    @validates('contributor')
    def validate_amount(self, contributor):
        if len(contributor) > 30:
            raise ValidationError("Too much symbols")

    class Meta:
        fields = ("id", "contributor", "amount", "contragent_id", "contract_id", "date")
        ordered = True


class ContragentSchema(Schema):
    id = fields.Integer(required=True, validate=must_not_be_blank)
    name = fields.Str(validate=must_not_be_blank)
    account = fields.Int()

    @validates('account')
    def validate_amount(self, account):
        if not int(account):
            raise ValidationError("Account have wrong format. Only integer numbers.")

