from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from .models import Product,offer,bestseller,brand,Contact,CheckoutOrder,OrderTracker,VerifyEmail,Blog
from django.contrib.auth.models import User
from django.core import serializers
import json,uuid
import ast
from PayTm import Checksum
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
# from django.contrib.sites.models import Site
# Create your views here.
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'

def Home(request):
	products=Product.objects.all();
	offers=offer.objects.all();
	bestsellers=bestseller.objects.all();
	brands=brand.objects.all();
	category=set()
	for i in products:
		category.add(i.prod_category)
	print(products)
	blogs=Blog.objects.all()
	return render(request,'Home.html',{"products":products,"offers":offers,"bestsellers":bestsellers,"brands":brands,"category":category,"blogs":blogs})

def MyContact(request):
	if request.method == "POST":
		name=request.POST['name']
		email=request.POST['email']
		phone=request.POST['phone']
		desc=request.POST['desc']
		contact= Contact(name=name,email=email,phone_number=phone,Reason=desc)
		contact.save()
		return redirect('/contact/')

	return render(request,'Contact.html')

def RE(request):
	return render(request,'RE.html')

def tc(request):
	return render(request,'tc.html')

def policy(request):
	return render(request,'policy.html')


def product(request,prod_id):
	product = Product.objects.filter(product_id=prod_id)
	return render(request,'productDetail.html',{"product":product[0]})


def About(request):
	return render(request,'About.html')

	
def Checkout(request):
	if request.user.is_authenticated:

		totalprice=0
		cartitems=request.session['prodid']

   
		if request.method == "POST":
			name=request.POST['checkoutname']
			address1=request.POST['address1']
			address2=request.POST['address2']
			city=request.POST['city']
			state=request.POST['state']
			zip_code=request.POST['zip_code']
			price=request.session['totalprice']
			prods_quant=request.session['prodid']
			orderid=uuid.uuid4() 
			print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
			print(orderid)

			checkout=CheckoutOrder(orderid=orderid,name=name,email=request.user.email,address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,total=price,products=prods_quant)

			checkout.save()
			ordertracker=OrderTracker(orderid=orderid,status="Under Processing")
			ordertracker.save()

            
			product_ids=[]
			for i,j in cartitems.items():
				product_ids.append(i)
			allprods=Product.objects.filter(product_id__in=product_ids)
			for i in allprods:
				totalprice+=i.prod_price * cartitems[i.product_id]
			request.session['totalprice']=totalprice

			param_dict = {

                'MID': 'WorldP64425807474247',
                'ORDER_ID': str(orderid),
                'TXN_AMOUNT': str(totalprice),
                'CUST_ID': request.user.email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',
				}
			param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
			return render(request, 'paytm.html', {'param_dict': param_dict})

			# return redirect('/checkout/')


		cartitems=request.session['prodid']
		print(len(cartitems.keys()))
		if len(cartitems.keys()) > 0:
			totalprice=0
			product_ids=[]
			for i,j in cartitems.items():
				product_ids.append(i)
			allprods=Product.objects.filter(product_id__in=product_ids)
			for i in allprods:
				totalprice+=i.prod_price * cartitems[i.product_id]
			request.session['totalprice']=totalprice

			return render(request,'Checkout.html',{"cartitems":allprods,"quantityid":cartitems,"totalprice":totalprice})



		else:
			print(request.session['prodid'])
			return HttpResponse("No items in the session cart")

		
	else:
		return HttpResponse("please Login First before checkout")

def Tracker(request):
	if request.method=="POST":
		print("insdie Tracker++++++++++++++++++++++++++++++++++++++++",json.loads(request.body))
		data = json.loads(request.body)
		try:
			orderid=data['orderId']
		except Exception as e:
			print(e)
		orderemail=OrderTracker.objects.filter(orderid=orderid)
		orderdetail=CheckoutOrder.objects.filter(orderid=orderid)
		prodid=[]
		for i in orderdetail:
			data=ast.literal_eval(i.products)
			for i in data.keys():
				prodid.append(i)

		allprods=Product.objects.filter(product_id__in=prodid)
		prodname=[]
		for i in allprods:
			prodname.append(i.prod_name)






		if len(orderemail) > 0:
			mylist=[orderemail[0].status,orderdetail[0].total,prodname]
			return HttpResponse(json.dumps(mylist))
		else:
			return HttpResponse("Sorry We Unable To Find Your Order")
			



	return render(request,'tracker.html')


def ListviewInOrderid(request):
	orderedprod=CheckoutOrder.objects.filter(email=request.user.email)
	tmpJson = serializers.serialize("json",orderedprod)
	tmpObj = json.loads(tmpJson)
	print(tmpObj)

	return HttpResponse(json.dumps(tmpObj))

def handleSignup(request):
	if request.method=='POST':
		username=request.POST['username']
		fname=request.POST['fname']
		lname=request.POST['lname']
		email=request.POST['email']
		pass1=request.POST['pass1']
		pass2=request.POST['pass2']

		if len(username)<10 and len(username)>15:
		    messages.error(request,"username must be between 10-15 characters")
		    return redirect('/')

		if not username.isalnum():
		    messages.error(request,"username must contain only numbers and characters")
		    return redirect('/')

		if pass1 != pass2:
		    messages.error(request,"passwords not matches")
		    return redirect('/')


		#create user
		myuser=User.objects.create_user(username,email,pass1)
		myuser.first_name=fname
		myuser.last_name=lname
		myuser.save()
		token=uuid.uuid4()
		verifyemail=VerifyEmail(customer=myuser,token=token,is_verified=False)
		verifyemail.save()
		# if Site._meta.installed:
		# 	site = Site.objects.get_current()
		# else:
		# 	site = RequestSite(request)
		print("++++++++++++++++++")
		print(request.META['HTTP_HOST'] )
		subject = 'My Store Registration'
		message = 'Hello '+username+' Please Complete Your Registration By Clicking On The Link below \n\n\n\n\n\n'+request.scheme+':' +'//'+request.META['HTTP_HOST']+'/email/verify/'+str(token)
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [email,]
		res=send_mail( subject, message, email_from, recipient_list )
		if res==1:
			messages.success(request,"Account is created Please Verify your email Before Login"+str(token))
			return redirect('/')
		messages.error(request,"Some undefined error occur please try again")
		return redirect('/')

	else:
		return HttpResponse("404 - NOT FOUND")
def verifyemail(request,token):
	users=VerifyEmail.objects.filter(token=token).update(is_verified=True)
	# users[0]
	print("user saved ")
	return HttpResponse("save")
	# messages.success(request,"Email Verified Successfully")
	# return redirect('/')


def handleLogin(request):
	if request.method=='POST':
		loginusername=request.POST['loginusername']
		loginpassword=request.POST['loginpassword']

		user = authenticate(username=loginusername, password=loginpassword)
		if user is not None:
			myuser=VerifyEmail.objects.filter(customer=user).filter(is_verified=True)
		else:
			messages.error(request,"Invalid Credentials ")
			return redirect('/')

		if len(myuser) > 0:
			login(request,user)
			messages.success(request,"successfully logged In ")
			return redirect('/')
		else:
			messages.error(request,"Either You are not registered or not verified your Email")
			return redirect('/')

	return HttpResponse("404 - NOT FOUND")
    
def handleLogout(request):
    logout(request)
    messages.success(request,"You are successfully Logged Out")
    return redirect('/')

@csrf_exempt
def Sessionstore(request):
	if request.method == "POST":
		try:
			data = json.loads(request.body)
			print(data)
			if('Cart' in data):
				request.session['prodid'] = data['Cart']
			elif('Wish' in data):
				request.session['prodidwishlist'] = data['Wish']
			# del request.session['prodid']
			# print(request.session['prodid'])
			success="product successfully added to the cart"
			return HttpResponse(success)
		except Exception as e:
			print("error in data ______________________________________")
			success="Some error occur please try again"
			return HttpResponse(e)


def ProdInCart(request):
	#prodids is a dictionary of prodid:quantity pair
	prodid_quant=request.session['prodid']
	print(prodid_quant)
	print(type(prodid_quant))
	prod_id=[]
	prod_quant=[]
	for i,j in prodid_quant.items():
		prod_id.append(i) 
		prod_quant.append(j)
	if len(prod_id) < 1:
		return HttpResponse("NO product added to the cart")
	# print(type(prod_id))
	allprods=Product.objects.filter(product_id__in=prod_id)
	allprods2=bestseller.objects.filter(bestseller_id__in=prod_id)
	allprods3=offer.objects.filter(offer_id__in=prod_id)
	# context = {"products":allprods,"prodid_quant":prodid_quant}
	# context2 = {"products":allprods2,"prodid_quant":prodid_quant}

	if len(allprods) and len(allprods2) and len(allprods3) > 0:
		return render(request,'myproducts.html',{"products":allprods,"products2":allprods2,"products3":allprods3, "prodid_quant":prodid_quant})
	elif len(allprods2) > 0:
		return render(request,'myproducts.html',{"products2":allprods2,"prodid_quant":prodid_quant})
	elif len(allprods3) > 0:
		return render(request,'myproducts.html',{"products":allprods3,"prodid_quant":prodid_quant})
	else:
		return render(request,'myproducts.html',{"products":allprods,"prodid_quant":prodid_quant})
	




def Wishlist(request):
	try:
		wishlist=request.session['prodidwishlist']
		print(wishlist,"-----------------------------------------")
		keys=wishlist.keys();
		allprods=Product.objects.filter(product_id__in=keys)
		allprods2=bestseller.objects.filter(bestseller_id__in=keys)
		allprods3=offer.objects.filter(offer_id__in=prod_id)
		print(allprods2)
		# print(request.session.keys())
	except Exception as e:
		# print(request.session['prodid'])
		return HttpResponse("no Wishlist item")
	if len(allprods) and len(allprods2) and len(allprods3) > 0:
		return render(request,'wishlist.html',{"wishlist":allprods,"wishlist2":allprods2,"wishlist3":allprods3})
	elif len(allprods2) > 0:
		return render(request,'wishlist.html',{"wishlist2":allprods2})
	elif len(allprods3) > 0:
		return render(request,'wishlist.html',{"wishlist":allprods3})
	else:
		return render(request,'wishlist.html',{"wishlist":allprods})
	

def ShowBlogs(request,blog_id):
	print(type(blog_id))
	blog=Blog.objects.filter(id=blog_id)
	print(blog)
	return render(request,'blog.html',{"blog":blog[0]})

def ShowBestsellers(request,myid):
	bestsellers=bestseller.objects.filter(id=myid)
	print(bestsellers)
	return render(request,'bestseller.html',{"bestseller":bestsellers[0]})


def BrandProducts(request,brand_name):
	brands=Product.objects.filter(brand_name=brand_name)
	return render(request,'brandedprods.html',{"brands":brands})


# def BestWishlist(request):
# 	try:
# 		wishlist=request.session['prodidwishlist']
# 		keys=wishlist.keys();
# 		allprods=bestseller.objects.filter(bestseller_id__in=keys)
# 		# print(request.session.keys())
# 	except Exception as e:
# 		# print(request.session['prodid'])
# 		return HttpResponse("no Wishlist item")
# 	return render(request,'bestwishlist.html',{"wishlist":allprods})


def OfferProd(request,prodid):
	offers=offer.objects.filter(id=prodid)
	print(offers,"||||||||||||||||||||||||||||||||||||||||||||||||")
	if len(offers) > 0:
		return render(request,'offerpage.html',{"offer":offers[0]})
	else:
		return HttpResponse("Products Not Found with this id")


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})