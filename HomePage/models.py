from django.db import models
import uuid 
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
	product_id = models.CharField(max_length=50,default="")
	prod_name = models.CharField(max_length=50,default="")
	prod_desc = models.CharField(max_length=1000,default="")
	prod_price=models.FloatField(default=0)
	prod_category=models.CharField(max_length=100,default="")
	prod_image=models.ImageField(upload_to="images",default="")
	brand_name=models.CharField(max_length=100,default="")


	def __str__(self):
		return self.prod_name

class offer(models.Model):
	offer_id=models.CharField(max_length=50,default="")
	offer_name = models.CharField(max_length=50,default="")
	offer_desc=models.CharField(max_length=100,default="")
	offer_price=models.FloatField(default=0)
	offer_image=models.ImageField(upload_to="images",default="")

	def __str__(self):
		return self.offer_name

class bestseller(models.Model):
	bestseller_id=models.CharField(max_length=50,default="")
	bestseller_name = models.CharField(max_length=50,default="")
	bestseller_desc=models.TextField(default="")
	bestseller_price=models.FloatField(default=0)
	bestseller_image=models.ImageField(upload_to="images",default="")

	def __str__(self):
		return self.bestseller_name

class brand(models.Model):
	brand_name = models.CharField(max_length=50,default="")
	brand_image=models.ImageField(upload_to="images",default="")

	def __str__(self):
		return self.brand_name


class Contact(models.Model):
	name=models.CharField(max_length=50,default="")
	email=models.EmailField(max_length=100)
	phone_number = models.CharField(max_length=12) # validators should be a list
	Reason=models.TextField()

	def __str__(self):
		return self.name

class CheckoutOrder(models.Model):
	orderid = models.UUIDField(default = uuid.uuid4,editable = False)
	name=models.CharField(max_length=50,default="")
	email=models.EmailField(max_length=100,default="")
	address1=models.CharField(max_length=500,default="")
	address2=models.CharField(max_length=500,default="")
	city=models.CharField(max_length=50,default="")
	state=models.CharField(max_length=50,default="")
	zip_code=models.CharField(max_length=10,default="")
	total=models.CharField(max_length=50,default="")
	products=models.CharField(max_length=1000,default="")

	def __str__(self):
		return self.name


class OrderTracker(models.Model):
	orderid=models.UUIDField(default = uuid.uuid4,editable = False)
	status=models.CharField(max_length=100)


class VerifyEmail(models.Model):
	customer=models.ForeignKey(User,on_delete=models.CASCADE)
	token=models.UUIDField(default = uuid.uuid4,editable = False)
	is_verified=models.BooleanField(default=False)

class Blog(models.Model):
	title=models.CharField(max_length=100,default="")
	description=models.TextField()
	posted_on=models.DateTimeField(auto_now_add=True) 
	image=models.ImageField(upload_to="images")