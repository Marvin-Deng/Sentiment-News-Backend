"""
Module for ticker table.
"""

from tortoise.models import Model
from tortoise.fields import IntField, CharField, FloatField


class TickerModel(Model):
    id = IntField(pk=True, generated=True)
    market_date = CharField(max_length=100)
    ticker = CharField(max_length=25, null=True)
    open_price = FloatField(null=True)
    high_price = FloatField(null=True)
    low_price = FloatField(null=True)
    close_price = FloatField(null=True)
    volume = IntField(null=True)
    adj_open = FloatField(null=True)
    adj_high = FloatField(null=True)
    adj_low = FloatField(null=True)
    adj_close = FloatField(null=True)
    adj_volume = IntField(null=True)
    div_cash = FloatField(null=True)
    split_factor = FloatField(null=True)

    class Meta:
        table = "ticker_model"
