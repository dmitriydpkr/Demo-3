'''
GET


    payment /
            all
            id /
            contributor /
            amount / start / finish
            period / start_date / finish_date
            period / start_date /                            # default time now
            contragent /

            conract / id
            conract / id / start_date / finish_date
            conract / id / start_date /
            conract /


POST


    INSERT, UPDATE

        payment /
                id / contributor / amount / period / date / contragent / contrac

    DELETE

        payment /
                id /











 id = IntegerField(primary_key=True, null=False)
    contributor = CharField(max_length=50, null=False)
    amount = DoubleField(null=False)
    period = DateTimeField(default=datetime.now)
    date = DateTimeField(default=datetime.now(), null=False)
    contragent = ForeignKeyField(Contragent)
    contract = ForeignKeyField(Contract)





















'''