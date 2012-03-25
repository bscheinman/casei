from casei.fields import UUIDField
from django.contrib import admin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Market(models.Model):
    name = models.CharField(max_length=20, unique=True)
    game = models.ForeignKey('ncaacards.NcaaGame', blank=True, null=True)

    def __str__(self):
        return self.name


class Security(models.Model):
    market = models.ForeignKey(Market, related_name='securities')
    name = models.CharField(max_length=6)
    team = models.ForeignKey('ncaacards.GameTeam', blank=True, null=True)

    class Meta:
       unique_together = ('market', 'name')

    def __str__(self):
        return self.name

    def get_top_bids(self, count=5):
        return self.orders.filter(is_active=True, quantity_remaining__gt=0, is_buy=True).order_by('-price', 'last_modified')[:count]

    def get_top_asks(self, count=5):
        return self.orders.filter(is_active=True, quantity_remaining__gt=0, is_buy=False).order_by('price', 'last_modified')[:count]

    def get_bid(self):
        bids = self.get_top_bids(1)
        return bids[0].price if bids else 0.0

    def get_bid_order(self):
        bids = self.get_top_bids(1)
        return bids[0] if bids else Order(price=0.0)

    def get_ask(self):
        asks = self.get_top_asks(1)
        return asks[0].price if asks else 0.0

    def get_ask_order(self):
        asks = self.get_top_asks(1)
        return asks[0] if asks else Order(price=0.0)

    def get_last(self):
        execs = self.executions.order_by('-time')
        return execs[0].price if execs else 0.0

    def get_bbo(self):
        return (self.get_top_bids(5), self.get_top_asks(5))

    def get_bbo_table(self, depth=5):
        bids, asks = self.get_top_bids(depth), self.get_top_asks(depth)
        table = []
        for i in range(depth):
            bid = bids[i] if len(bids) > i else None
            ask = asks[i] if len(asks) > i else None
            if not bid and not ask:
                break
            table.append((bid, ask))
        return table



class Order(models.Model):
    order_id = UUIDField(auto=True, primary_key=True)
    placer = models.CharField(max_length=30) # This should be populated by the using application and is just for that application's use
    entry = models.ForeignKey('ncaacards.UserEntry', blank=True, null=True)
    security = models.ForeignKey(Security, related_name='orders')
    placed_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    quantity_remaining = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    is_buy = models.BooleanField()
    is_active = models.BooleanField(default=True)
    cancel_on_game = models.BooleanField(default=False)

    def __str__(self):
        return self.order_id

    def side_name(self):
        return 'Buy' if self.is_buy else 'Sell'


class Execution(models.Model):
    security = models.ForeignKey(Security, related_name='executions', editable=False)
    execution_id = UUIDField(auto=True, primary_key=True, editable=False)
    buy_order = models.ForeignKey(Order, related_name='buy_executions', editable=False)
    sell_order = models.ForeignKey(Order, related_name='sell_executions', editable=False)
    quantity = models.IntegerField(editable=False)
    price = models.DecimalField(decimal_places=2, max_digits=10, editable=False)
    time = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return '%s   %s x %s @ %s' % (self.time.strftime('%a %m/%d %H:%M'), self.security.name, self.quantity, self.price)


admin.site.register(Market)
admin.site.register(Security)
admin.site.register(Order)
admin.site.register(Execution)


def process_order(order):
    def execute_orders(existing_order):
        exec_quantity = min([order.quantity_remaining, existing_order.quantity_remaining])

        if order.is_buy:
            buy_order = order
            sell_order = existing_order
        else:
            buy_order = existing_order
            sell_order = order

        if buy_order.placer == sell_order.placer:
            buy_order.quantity_remaining -= exec_quantity
            buy_order.save()
            sell_order.quantity_remaining -= exec_quantity
            sell_order.save()
        else:
            execution = Execution.objects.create(security=order.security, buy_order=buy_order,\
                sell_order=sell_order, quantity=exec_quantity, price=existing_order.price)

    if order.is_buy:
        comparer = lambda x: x.price <= order.price
        order_generator = lambda: order.security.get_top_asks()
    else:
        comparer = lambda x: x.price >= order.price
        order_generator = lambda: order.security.get_top_bids()

    while True:
        matching_orders = order_generator()
        if not matching_orders:
            return
        for matching_order in matching_orders:
            if not comparer(matching_order):
                return
            execute_orders(matching_order)
            if order.quantity_remaining <= 0:
                return


@receiver(post_save, sender=Order, weak=False)
def on_new_order(sender, instance, created, **kwargs):
    if created:
        process_order(instance)


@receiver(post_save, sender=Execution, weak=False)
def record_execution(sender, instance, created, **kwargs):
    if created:
        instance.buy_order.quantity_remaining -= instance.quantity
        instance.buy_order.save()
        instance.sell_order.quantity_remaining -= instance.quantity
        instance.sell_order.save()
