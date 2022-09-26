from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from .models import Product_series, Products
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .form import NewUserForm, formnew
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .email import sendmail
from .models import newuser, update_user_profile
import datetime


purchase_dict = {}
# dictionaries for products and qualitiies

recipt_list = {}
# dictionaries for recipt in email,final price and payment_method


def total_price():
    '''return float calucating the price base on unit price and qualitiy'''
    total_price = 0
    for product in purchase_dict.keys():
        price = Products.objects.values_list(
            'Price', flat=True).get(Name=product)
        # retrieving price from Products.model
        qualities = int(purchase_dict[product])
        # get the value from the dictionaries
        item_price = price*qualities
        total_price += item_price
    return total_price


def final_price(payment_method):
    '''return the statement of the final price after discount and the discount'''
    price = float(total_price())
    discount = '(summer discount)'
    # discount statement
    if price >= 300:
        price -= 20
        discount += '(supermarket discount)'
    price *= 0.9
    if payment_method == 'visa':
        price *= 0.9
        discount += '(visa discount)'
    return '$' + str(round(price, 2))+'\n' + discount


def delete(request):
    '''for deleting items in purchase list'''
    item = list(request.GET.keys())
    # must use list
    # get the required delete items'key by using 'get' request
    delete_item = item[0]
    # get the first item (only first) from the list

    for key in list(purchase_dict.keys()):
        # must use list
        if delete_item in key:
            del purchase_dict[key]
            # delete item if requested key in purchase dict
    return redirect('web:purchase')


def index(request):
    '''main page'''
    return render(request=request,
                  template_name="homepage.html",
                  context={"series": Product_series.objects.all})
    # get all the products


@csrf_exempt
def register_request(request):
    '''register page'''
    if request.method == "POST":
        # save password can only use post method
        form = NewUserForm(request.POST)

        # New user have new column 'email' have form model
        if form.is_valid():
            user = form.save()
            update_user_profile

            # save user data
            username = form.cleaned_data
            messages.success(request, f'You have created account:{username} ')
            login(request, user)
            return redirect("web:index")
        else:
            for msg in form.error_messages:
                messages.error(request, f"[msg]: {form.error_messages[msg]}")
    form = NewUserForm
    # render new user form
    return render(request=request,
                  template_name="register.html",
                  context={"form": form})


@csrf_exempt
def login_request(request):
    '''login page'''
    if request.method == 'POST':
      # passwaord only use post method
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
              # check if user correct in password and username
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('web:index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="login.html",
                  context={"form": form})


def meat_series(request):
    meat_ser = Products.objects.filter(series_title_id=2)
    # filter the Products with series 'meat'
    meat = [x for x in Products.objects.values_list('Name')]
    # return item lists  'name' of meat_series
    for item in meat:
        item = item[0]
        # eliminate comma
        try:
            if int(request.GET.get(item)) > 0:
                value = int(request.GET.get(item))
                if item not in purchase_dict.keys():
                    purchase_dict[item] = value
                    purchase_dict[item] = old_value+value

                else:
                    old_value = int(purchase_dict.get(item))
            else:
                messages.info(request, 'positive number expected')
        except:
            pass

    return render(request=request,
                  template_name="meat.html",
                  context={"meat_ser": meat_ser})


def fruit_series(request):
    '''fruit series page, returning the purchased items and qualities to the 
    purchase_list by the request  '''
    fruit_ser = Products.objects.filter(series_title_id=1)
    # filter fruit series from Products

    fruit = [x for x in Products.objects.values_list('Name')]
    # list for returning all the name in meat_series

    for item in fruit:
        item = item[0]
        # eliminate comma from list

        try:
            if int(request.GET.get(item)) > 0:
              # if have valid input number in card
                value = int(request.GET.get(item))
                # return the value of item from request from card

                if item not in purchase_dict.keys():
                    # for new addition purchased items
                    purchase_dict[item] = value

                else:
                    # for old item which is added already
                    old_value = int(purchase_dict.get(item))
                    # get the old item value and add to new input
                    purchase_dict[item] = old_value+value
            else:
                messages.info(request, 'positive number expected')

        except:
            pass

    return render(request=request,
                  template_name="fruit.html",
                  context={"fruit_ser": fruit_ser})


def logout_request(request):
    '''logout the system'''
    logout(request)
    messages.info(request, "Logged out successfully!")
    purchase_dict.clear()
    # clear the purchase_list
    return redirect("web:index")


def purchase(request):
    '''purchase page'''
    purchase_list = [x + ' : ' + str(purchase_dict[x])
                     for x in purchase_dict.keys()]
    return render(request=request,
                  template_name='purchase.html',
                  context={'purchase_dict': purchase_list, 'total_price': total_price, 'final_price': final_price})


def payment(request):
    '''payment page, return recipt list'''
    recipt_list.clear()
    # clear the recipt_list

    if purchase_dict == {}:
        # prevent customers proceed the payment when they dont items and return them to purrchase page
        messages.info(request, "You havent buy things")
        return redirect('web:purchase')

    if not request.user.is_authenticated:
        # login before payment, return login page
        messages.info(request, 'Please log in to resume the purchase!')
        return redirect('web:login')

    payment_method = request.GET.get('payment')
    # get the payment method

    recipt_list['payment_method'] = payment_method

    if request.GET.get('payment'):
        if payment_method == '':
            messages.info(request, "the email column should not leave blank")
            return redirect('web:payment')

    fin_price = final_price(payment_method)
    # calucate final price
    recipt_list['fin_price'] = fin_price
    mail = request.GET.get('email')
    # get the email from request
    if mail == 'yes':
        email = True
    else:
        email = False
    recipt_list['email'] = email

    bran = request.GET.get('branch')
    if bran == 'Yuen Long':
        branch = 'Yuen long Branch\n(filty estate G/f,ktn road, Yuen Long)'
    elif bran == 'Kwun Tong':
        branch = 'Kwun Tong Branch\n(sdf estate ,lksjdf road,Kwun Tong)'
    else:
        branch = 'Causeway Bay Branch\n( gfhf estate,dfkgjld road , Causeway Bay )'
    recipt_list['branch'] = branch

    purchase_list = [x + ':' + str(purchase_dict[x])
                     for x in purchase_dict.keys()]
    return render(request=request,
                  template_name='payment.html',
                  context={'purchase_dict': purchase_list, 'total_price': total_price, 'final_price': fin_price, 'branch': branch, 'payment_method': payment_method})


def recipt(request):
    purchase_list = [x + ':' + str(purchase_dict[x])
                     for x in purchase_dict.keys()]
    payment_method = recipt_list.get('payment_method')

    messages.info(request, "Purchase successful!")

    fin_price = recipt_list['fin_price']

    email = recipt_list.get('email')

    username = request.user.username
    user_email = request.user.email

    branch = recipt_list.get('branch')

    history = newuser.objects.get(user__username='alex')
    buytime = datetime.datetime.now()

    history.purchase_history = f' {buytime} : {purchase_dict}'
    history.save()

    if email == True:
        # sending email
        email = sendmail(user_email, purchase_dict,
                         payment_method, fin_price, branch, take_day)

    take_day = datetime.datetime.now() + datetime.timedelta(days=3)
    return render(request=request,
                  template_name='recipt.html',
                  context={'purchase_dict': purchase_list, 'payment_method': payment_method,
                           'email': email, 'final_price': fin_price,
                           'username': username,
                           'branch': branch,
                           'buytime': buytime,
                           'take_day': take_day
                           })


def aboutus(request):
    '''aboutus page'''
    return render(request=request,
                  template_name='aboutus.html')


def discount(request):
    '''discount page'''
    return render(request=request,
                  template_name='discount.html')


def info(request):
    if request.user.newuser.purchase_history:
        purchase_history = request.user.newuser.purchase_history
    username = request.user.username
    password = request.user.password
    email = request.user.email
    return render(request=request, template_name='info.html', context={'purchase_history': purchase_history,
                                                                       'username': username,
                                                                       'password': password,
                                                                       'email': email})
