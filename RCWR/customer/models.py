from django.db import models
from django.contrib.auth.models import User

class RiceItem(models.Model):
    name = models.CharField(max_length = 50, null = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True)
    quantity = models.IntegerField(blank = True)
    image = models.ImageField(upload_to = 'rice_images/', null = True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
    name = models.CharField(max_length = 100, null = True)
    email = models.CharField(max_length = 100, null = True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, blank = True, null = True)
    date_ordered = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default = False, null = True, blank = False)
    transaction_id = models.CharField(max_length = 100, null = True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderriceitems_set.all()
        total = sum([r.get_total for r in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderriceitems_set.all()
        total = sum([r.quantity for r in orderitems])
        return total

class OrderRiceItems(models.Model):
    rice = models.ForeignKey(RiceItem, on_delete = models.SET_NULL, blank = True, null = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, blank = True, null = True)
    quantity = models.IntegerField(default = 0, blank = True, null = True)
    date_added = models.DateTimeField(auto_now_add = True)

#individual rice item total
    @property
    def get_total(self):
        total = self.rice.price * self.quantity
        return total

class OrderDetails(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, blank = True, null = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, blank = True, null = True)
    rice_ordered = models.ManyToManyField(OrderRiceItems, blank = True, related_name='orders')
    total_payment = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True)
    address = models.CharField(max_length = 200, null = True)
    ContactNum = models.CharField(max_length = 11, null = True, blank = True)
    shippingMeth = models.CharField(max_length = 15, null = True)

    shippingStat = (
        ('Preparing', 'Preparing'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Ready for Pick Up', 'YReady for Pick Up'),
        ('Picked Up', 'Picked Up')
    )
    shippingStatus = models.CharField(max_length = 50, blank = True, choices = shippingStat) #Ready for pickup, picked up, on the way, delivered
    
    orderStat = (
        ('Accepted', 'Accepted'),
        ('Denied', 'Denied'),
    )
    
    orderStatus = models.CharField(max_length = 50, blank = True, choices = orderStat) #Accepted or denied
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.address    

class LendingStat(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, blank = True, null = True)
    ContactNum = models.CharField(max_length = 11, null = True, blank = True)
    total_payment = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True)
    amount_paid = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null = True)
    balance = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True) #updates everytime amount_paid is being updated
    status = models.CharField(max_length = 10, blank = True)
    date_added = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.customer.name

