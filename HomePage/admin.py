from django.contrib import admin
from . models import Product,offer,bestseller,brand,Contact,CheckoutOrder,OrderTracker,VerifyEmail,Blog
# Register your models here.
admin.site.register(Product)
admin.site.register(offer)
admin.site.register(bestseller)
admin.site.register(brand)
admin.site.register(Contact)
admin.site.register(CheckoutOrder)
admin.site.register(OrderTracker)
admin.site.register(VerifyEmail)
admin.site.register(Blog)