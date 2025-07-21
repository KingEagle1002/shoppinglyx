from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


# Create your models here.
# customer model
STATES_Choice = (
    ('Abbottabad', 'Abbottabad'),
    ('Bahawalpur', 'Bahawalpur'),
    ('Bannu', 'Bannu'),
    ('Bhakkar', 'Bhakkar'),
    ('Bhaun', 'Bhaun'),
    ('Chakwal', 'Chakwal'),
    ('Chaman', 'Chaman'),
    ('Chiniot', 'Chiniot'),
    ('Dadu', 'Dadu'),
    ('Dera Ghazi Khan', 'Dera Ghazi Khan'),
    ('Dera Ismail Khan', 'Dera Ismail Khan'),
    ('Faisalabad', 'Faisalabad'),
    ('Gilgit', 'Gilgit'),
    ('Gujrat', 'Gujrat'),
    ('Gujranwala', 'Gujranwala'),
    ('Gwadar', 'Gwadar'),
    ('Hyderabad', 'Hyderabad'),
    ('Islamabad', 'Islamabad'),
    ('Jaranwala', 'Jaranwala'),
    ('Jhelum', 'Jhelum'),
    ('Karachi', 'Karachi'),
    ('Kasur', 'Kasur'),
    ('Killa Saifullah', 'Killa Saifullah'),
    ('Kohat', 'Kohat'),
    ('Lahore', 'Lahore'),
    ('Larkana', 'Larkana'),
    ('Mandi Bahauddin', 'Mandi Bahauddin'),
    ('Mardan', 'Mardan'),
    ('Mirpur', 'Mirpur'),
    ('Mirpur Khas', 'Mirpur Khas'),
    ('Multan', 'Multan'),
    ('Mianwali', 'Mianwali'),
    ('Muzaffarabad', 'Muzaffarabad'),
    ('Nawabshah', 'Nawabshah'),
    ('Nushki', 'Nushki'),
    ('Okara', 'Okara'),
    ('Peshawar', 'Peshawar'),
    ('Pishin', 'Pishin'),
    ('Quetta', 'Quetta'),
    ('Rahim Yar Khan', 'Rahim Yar Khan'),
    ('Rawalpindi', 'Rawalpindi'),
    ('Sahiwal', 'Sahiwal'),
    ('Sargodha', 'Sargodha'),
    ('Shikarpur', 'Shikarpur'),
    ('Sheikhupura', 'Sheikhupura'),
    ('Sialkot', 'Sialkot'),
    ('Skardu', 'Skardu'),
    ('Swat', 'Swat'),
    ('Toba Tek Singh', 'Toba Tek Singh'),
    ('Turbat', 'Turbat'),
    ('Zhob', 'Zhob'),
)

class Customer (models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    name     = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city     = models.CharField(max_length=50)
    zipcode  = models.IntegerField()
    state    = models.CharField(choices=STATES_Choice, max_length=50)

    def __str__(self):
        return str(self.id)


#  product model .
CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear')
)
class Product(models.Model):
    title            = models.CharField(max_length=100)
    selling_price    = models.FloatField()
    discounted_price = models.FloatField()
    description      = models.TextField()
    brand            = models.CharField(max_length=100)
    category         = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image    = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

# cart model
class Cart(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart({self.user.username}, {self.product.title})"

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATES_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

# order placed model
class OrderPlaced(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    customer     = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product      = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity     = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status       = models.CharField(choices=STATES_CHOICES, max_length=50, default='Pending')
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price    

    
               
