from casei.fields import UUIDField
from django.contrib import admin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Market(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Security(models.Model):
    market = models.ForeignKey(Market, related_name='securities')
    name = models.CharField(max_length=6)

    class Meta:
       unique_together = ('market', 'name')

    def __str__(self):
        return self.name

    def get_top_bids(self, count=5):
        return self.orders.filter(is_active=True, quantity_remaining__gt=0, is_buy=True).order_by('-price')[count:]

    def get_top_asks(self, count=5):
        return self.orders.filter(is_active=True, quantity_remaining__gt=0, is_buy=False).order_by('price')[count:]

    def get_bid(self):
        bids = self.get_top_bids(1)
        return bids[0].price if bids else 0.0

    def get_ask(self):
        asks = self.get_top_asks(1)
        return asks[0].price if asks else 0.0

    def get_last(self):
        execs = self.executions.order_by('-time')
        return execs[0].price if execs else 0.0

    def get_bbo(self):
        return (get_top_bids(5), get_top_asks(5))



class Order(models.Model):
    order_id = UUIDField(auto=True, primary_key=True)
    placer = models.CharField(max_length=30) # This should be populated by the using application and is just for that application's use
    security = models.ForeignKey(Security, related_name='orders')
    placed_time = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    quantity_remaining = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    is_buy = models.BooleanField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id


class Execution(models.Model):
    security = models.ForeignKey(Security, related_name='executions')
    execution_id = UUIDField(auto=True, primary_key=True)
    buy_order = models.ForeignKey(Order, related_name='buy_executions')
    sell_order = models.ForeignKey(Order, related_name='sell_executions')
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.execution_id


admin.site.register(Market)
admin.site.register(Security)
admin.site.register(Order)
admin.site.register(Execution)
