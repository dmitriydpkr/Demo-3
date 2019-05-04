from marshmallow import Schema, fields


class ContragentSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    account = fields.Int()


class PaymentSchema(Schema):
    id = fields.Integer()
    contributor = fields.String()
    amount = fields.Float()
    period = fields.LocalDateTime()
    date = fields.Integer()
    contragent_id = fields.Integer()
    contract_id = fields.Integer()


contragent_schema = ContragentSchema()
contragents_schema = ContragentSchema(many=True)
payment_schema = ContragentSchema()
payments_schema = PaymentSchema(many=True)


