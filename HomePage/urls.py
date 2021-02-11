from django.urls import path
from . import views
urlpatterns = [
    path('',views.Home),
    path('contact/',views.MyContact),
    path("product/<prod_id>", views.product),
    path('about/',views.About),
    path('checkout/',views.Checkout),
    path('tracker/',views.Tracker),
    path('sessionstore/',views.Sessionstore),
    path('myproducts/',views.ProdInCart),
    path('mywishlist/',views.Wishlist),
    path('RE/',views.RE),
    path('tc/',views.tc),
    path('policy/',views.policy),
    path('listview/',views.ListviewInOrderid),
    path("signup/", views.handleSignup, name="handleSignup"),
    path("login/", views.handleLogin, name="handleLogin"),
    path("logout/", views.handleLogout, name="handleLogout"),
    path("email/verify/<token>",views.verifyemail),
    path('blog/<blog_id>',views.ShowBlogs),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path('bestseller/<int:myid>',views.ShowBestsellers),
    path('products/<brand_name>/',views.BrandProducts),
    path('products/offer/<prodid>',views.OfferProd)

]