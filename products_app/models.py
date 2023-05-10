from django.db import models
from django.contrib.auth.models import User


class Registered(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.last_name
        
class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    description = models.TextField()
    image = models.ImageField(upload_to='product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.title

class Order(models.Model):
    SUBJECTS = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('On The Way', 'On The Way'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
    )

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    zipcode = models.IntegerField()
    transaction_id = models.CharField(max_length=6)
    status = models.CharField(max_length=10, choices=SUBJECTS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.transaction_id

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def total_cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.title

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.product.title
    
class Contact(models.Model):
    SUBJECTS = (
        ('', 'Please select a subject'),
        ('My Order', 'My Order'),
        ('Change my Order', 'Change my Order'),
        ('Order Cancellation', 'Order Cancellation'),
        ('Damaged Book', 'Damaged Book'),
        ('Incorrect Book', 'Incorrect Book'),
        ('Payment', 'Payment'),
        ('Other', 'Other'),
    )
    
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()
    subject =  models.CharField(max_length=18, choices=SUBJECTS)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
        