from django.views import View
from .utils import verifEmail, cartTotal, totals, purchaseEmail, wishlistTotal, pagination
from .forms import LoginForm, RegisterForm, ContactForm, UpdateForm, PasswordChangeForm, OrderForm
from .models import Registered, Category, Product, Wishlist, Cart, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, JsonResponse
import json
from decimal import Decimal
from random import randint


class signInUp(View):
    def get(self, request):
        cartNum = cartTotal(request)
        wishNum = wishlistTotal(request)
        loginForm = LoginForm()
        registerForm = RegisterForm()
        return render(request, 'products_app/user/signInUp.html', locals())

    def post(self, request):
        if 'signInSub' in request.POST:
            loginForm = LoginForm()
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
            if user is None:
                cartNum = cartTotal(request)
                wishNum = wishlistTotal(request)
                registerForm = RegisterForm()
                messages.error(request, 'Something went wrong when you sign in.')
                err_message = 'Username and password do not match. Note that both fields may be case-sensitive.'
                return render(request, 'products_app/user/signInUp.html', locals())
                
            else:
                if user.registered.is_verified == True:
                    login(request, user)
                    messages.success(request, f'Welcome {user.username}!')
                    return redirect('home')

                else:
                    cartNum = cartTotal(request)
                    wishNum = wishlistTotal(request)
                    registerForm = RegisterForm()
                    messages.error(request, 'Something went wrong when sign in.')
                    err_message = 'Your profile is not verified yet. Please check your email.'
                    return render(request, 'products_app/user/signInUp.html', locals())

        elif 'signUpSub' in request.POST:
            registerForm = RegisterForm(request.POST)

            if registerForm.is_valid(): 
                user = registerForm.save()
                reg_user = Registered(user=user).save()
                verifEmail(request, user, user.email)
                return redirect('signInUp')

            else:
                cartNum = cartTotal(request)
                wishNum = wishlistTotal(request)
                loginForm = LoginForm()
                messages.error(request, 'Something went wrong when sign up.')
                return render(request, 'products_app/user/signInUp.html', locals())

class profile(View):
    def get(self, request):
        cartNum = cartTotal(request)
        wishNum = wishlistTotal(request)
        user = request.user
        formUpdate = UpdateForm(instance=user)
        formPassword = PasswordChangeForm(user)
        return render(request, 'products_app/user/profile.html', locals())
        
    def post(self, request):
        if 'subProfile' in request.POST:
            user = User.objects.get(id=request.user.id)
            formUpdate = UpdateForm(request.POST, instance=request.user)
            
            if formUpdate.is_valid():
                temp_user = formUpdate.save(commit=False)
                
                if not( (temp_user.first_name == '' or temp_user.first_name == user.first_name) and
                        (temp_user.last_name == '' or temp_user.last_name == user.last_name) and
                        (temp_user.username == '' or temp_user.username == user.username) and 
                        (temp_user.email== '' or temp_user.email == user.email) ):

                    if(temp_user.first_name == ''):
                        temp_user.first_name=user.first_name

                    if(temp_user.last_name == ''):
                        temp_user.last_name=user.last_name

                    if(temp_user.username == ''):
                        temp_user.username=user.username

                    if(temp_user.email == ''):
                        temp_user.email=user.email
                    
                    temp_user.save()
                    messages.success(request, 'Your profile was updated succesfully!')
                    return redirect('profile')

                else:
                    messages.warning(request, "Your profile wasn't updated.")
                    return redirect('profile')

            else: 
                formPassword = PasswordChangeForm(user)
                messages.error(request, "The form is invalid. Your profile wasn't updated.")
                return render(request, 'products_app/user/profile.html', locals())
                
        elif 'subPassword' in request.POST:
            formPassword = PasswordChangeForm(request.user, request.POST)
            
            if formPassword.is_valid():
                formPassword.save()
                update_session_auth_hash(request, formPassword.user)
                messages.success(request, 'Your password was changed succesfully!')
                return redirect('profile')

            else: 
                formUpdate = UpdateForm(instance=request.user)
                messages.error(request, "The form is invalid. Password wasn't changed.")
                return render(request, 'products_app/user/profile.html', locals())

def delProfile(request):
    request.user.delete()
    messages.warning(request, 'Your account was deleted succesfully.')
    return redirect('home')

def logOut(request):
    logout(request)
    messages.warning(request, 'You have been successfully logged out.')
    return redirect ('home')

def search(request):
    title = header = 'Search Results'
    cartNum = cartTotal(request)
    wishNum = wishlistTotal(request)
    phrase = request.GET.get ('search', '')
    books = Product.objects.filter(title__icontains=phrase)
    
    if books:
        page_obj = pagination(request, books, 8)

        if request.user.is_authenticated:
            wishlist_books = books.filter(wishlist__in=Wishlist.objects.filter(user=request.user))
            cart_books = books.filter(cart__in=Cart.objects.filter(user=request.user)) 

    else:
        message = f'Your phrase="{phrase}" did not return any results.'
  
    return render(request, 'products_app/books/search.html', locals())

def orders(request):
    cartNum = cartTotal(request)
    wishNum = wishlistTotal(request) 
    my_orders = Order.objects.filter(user=request.user)
    
    if my_orders:
        myOrdersDict = {}
        amount = 0
        page_obj = pagination(request, my_orders, 7)
        
        for order in my_orders:
            myOrdersDict[order] = {}
            myOrdersDict[order]['order_items'] = OrderItem.objects.filter(order=order)
            
            for orderItem in myOrdersDict[order]['order_items']: 
                amount += orderItem.total_cost

            myOrdersDict[order]['total_amount'] = amount + 20    
            amount = 0   
    
    return render(request, 'products_app/user/orders.html', locals())

def cancelation(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'Canceled'
    order.save()
    
    messages.warning(request, f'Your order with number "{order.transaction_id}" was canceled.')
    return redirect('orders')

def cart(request):
    cartNum = cartTotal(request)
    wishNum = wishlistTotal(request) 
    amount = shipping = total_amount = 0

    if request.user.is_authenticated:
        cart_books = Cart.objects.filter(user=request.user)

        for i in cart_books:
            amount += i.total_cost

    else: 
        try:
            cart = json.loads(request.COOKIES['CookieCart'])
            cart_books =[]
            
            for i in cart:
                book = Product.objects.get(id=i)

                cart_book = {
                    'product': book,
                    'id': i,
                    'quantity': cart[i]['quantity'],
                    'total_cost': book.price * cart[i]['quantity']
                }
                cart_books.append(cart_book)
                amount += book.price * cart[i]['quantity']

            title_dict = json.loads(request.COOKIES['CookieTitle']) 
            title = title_dict['title']

            response = redirect('cart')
            response.delete_cookie('CookieTitle')
            messages.success(request, f'"{title}" was added to your Cart!') 
            return response
        
        except: pass

    if amount:
        shipping = 20
        total_amount = amount + shipping
            
    return render(request, 'products_app/user/cart.html', locals())

def addCart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_book = Cart(user=request.user, product=product)
    cart_book.save()

    messages.success(request, f'"{product.title}" was added to your Cart!')

    url_path = request.META.get('HTTP_REFERER')
    next_to_last = url_path.split("/")[-2]
    
    if next_to_last == 'categories':
        return redirect(url_path)

    return redirect('cart')

def removeCart(request):
    if request.method == 'GET':
        cartbook_id = request.GET['cartbook_id']
        amount_bef = Decimal(request.GET['amount_bef'])
        
        if request.user.is_authenticated:
            cartbook = Cart.objects.get(id=cartbook_id)
            mytuple = totals(amount_bef, cartbook.total_cost)
            message = f'"{cartbook.product.title}" was removed from your cart!'
            cartbook.delete()
            data = {'cartnum':cartTotal(request), 'amount':mytuple[0], 'total_amount':mytuple[1], 'message':message}

        else:
            qty = int(request.GET['quantity'])
            cartbook = Product.objects.get(id=cartbook_id)
            mytuple = totals(amount_bef, cartbook.price*qty)
            message = f'"{cartbook.title}" was removed from your cart!'
            data = {'cartnum':cartTotal(request)-1, 'amount':mytuple[0], 'total_amount':mytuple[1], 'message': message, 'user':'anonymous'}

        return JsonResponse(data)

def minusQuantity(request):
    if request.method == 'GET':
        data = {}
        cartbook_id = request.GET['cartbook_id']
        amount_bef = Decimal(request.GET['amount_bef'])
        
        if request.user.is_authenticated:
            cartbook = Cart.objects.get(id=cartbook_id)
            
            if cartbook.quantity >1:
                cartbook.quantity -=1
                cartbook.save()
                mytuple = totals(amount_bef, cartbook.product.price, '-')
                data = {'quantity':cartbook.quantity, 'total_cost':cartbook.total_cost, 'amount':mytuple[0], 'total_amount':mytuple[1]}
            
        else:
            cart = json.loads(request.COOKIES['CookieCart'])
            
            if cart[cartbook_id]['quantity'] > 1:
                quantity = cart[cartbook_id]['quantity'] - 1
                total_cost = Product.objects.get(id=cartbook_id).price * quantity
                mytuple = totals(amount_bef, Product.objects.get(id=cartbook_id).price, '-')    
                data = {'quantity':quantity, 'total_cost':total_cost, 'amount':mytuple[0], 'total_amount':mytuple[1], 'user':'anonymous'}

        return JsonResponse(data)      

def plusQuantity(request):
    if request.method == 'GET':
        cartbook_id = request.GET['cartbook_id']
        amount_bef = Decimal(request.GET['amount_bef'])

        if request.user.is_authenticated:
            cartbook = Cart.objects.get(id=cartbook_id)
            cartbook.quantity +=1
            cartbook.save()
            mytuple = totals(amount_bef, cartbook.product.price, '+')
            data = {'quantity':cartbook.quantity, 'total_cost':cartbook.total_cost, 'amount':mytuple[0], 'total_amount':mytuple[1]}

        else:
            cart = json.loads(request.COOKIES['CookieCart'])
            quantity = cart[cartbook_id]['quantity'] + 1
            total_cost = Product.objects.get(id=cartbook_id).price * quantity
            mytuple = totals(amount_bef, Product.objects.get(id=cartbook_id).price, '+')
            data = {'quantity':quantity, 'total_cost':total_cost, 'amount':mytuple[0], 'total_amount':mytuple[1],'user':'anonymous'}

        return JsonResponse(data)

class checkout(View):
    def get(self, request):
        if (request.META.get('HTTP_REFERER')):
            cartNum = cartTotal(request)
            wishNum = wishlistTotal(request)
            amount = 0
            
            if request.user.is_authenticated:
                initial_dict = {'firstname':request.user.first_name, 'lastname':request.user.last_name, 'email':request.user.email}
                form = OrderForm(initial=initial_dict)
                form.fields['firstname'].widget.attrs['readonly'] = True
                form.fields['lastname'].widget.attrs['readonly'] = True
                form.fields['email'].widget.attrs['readonly'] = True

                form.fields['firstname'].widget.attrs['autofocus'] = False
                form.fields['phone'].widget.attrs['autofocus'] = True
                
                cart_books = Cart.objects.filter(user=request.user)
                
                for i in cart_books:
                    amount += i.total_cost
            
            else:
                form = OrderForm()
                cart = json.loads(request.COOKIES['CookieCart'])
                cart_books =[]
                
                for i in cart:
                    book = Product.objects.get(id=i)

                    cart_book = {
                        'product': book,
                        'quantity': cart[i]['quantity'],
                        'total_cost': book.price * cart[i]['quantity']
                    }
                    cart_books.append(cart_book)
                    amount += book.price * cart[i]['quantity']
                
            total_amount = amount + 20
            return render(request, 'products_app/user/checkout.html', locals())

        else:
            return HttpResponseNotFound('<h1>404 - Page not found</h1>')
            
    def post(self, request):
        form = OrderForm(request.POST)
        data={}
        amount = 0
        
        if form.is_valid():
            order = form.save(commit=False)

            while True:
                trans_id = randint(1000, 99999)
                trans_id = '#' + str(trans_id)

                if not Order.objects.filter(transaction_id=trans_id):
                    break

            order.transaction_id = trans_id
            messages.success(request, 'Your order has been placed! You will receive an email for further information.')

            if request.user.is_authenticated:
                order.user = request.user
                order.save()
                cart_books = Cart.objects.filter(user=request.user)  

                for cart_book in cart_books:
                    amount += cart_book.total_cost
                    OrderItem(order=order, product=cart_book.product, quantity=cart_book.quantity).save()
        
                data['order'] = order
                data['cart_books'] = cart_books 
                data['total_amount'] = amount + 20  
                purchaseEmail(request, data)
                cart_books.delete()
                return redirect('home')

            else:
                order.save()
                cart = json.loads(request.COOKIES['CookieCart'])
                cart_books =[]
                
                for i in cart:
                    book = Product.objects.get(id=i)

                    cart_book = {
                        'product': book,
                        'quantity': cart[i]['quantity'],
                        'total_cost': book.price * cart[i]['quantity']
                    }
                    cart_books.append(cart_book)
                    amount += book.price * cart[i]['quantity']

                data['order'] = order
                data['cart_books'] = cart_books   
                data['total_amount'] = amount + 20
                purchaseEmail(request, data)
                response = redirect('home')
                response.delete_cookie('CookieCart')
                return response

        else:
            messages.error(request, 'Your email is invalid, please try again.')
            return redirect('checkout')

def wishlist(request):
    if request.user.is_authenticated:
        cartNum = cartTotal(request)
        wishNum = wishlistTotal(request)
        wishlist_books = Wishlist.objects.filter(user=request.user)

        if wishlist_books:
            page_obj = pagination(request, wishlist_books, 6)
            
        else:    
            message = 'Your wishlist is empty.'

        return render(request, 'products_app/user/wishlist.html', locals())

    else:
        messages.warning(request, 'You must be logged in to see your wishlist.')
        return redirect('signInUp')

def addWishlist(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        Wishlist(user=request.user, product=product).save()
        messages.success(request, f'"{product.title}" was added to your whishlist!')
    
        url_path = request.META.get('HTTP_REFERER')
        next_to_last = url_path.split("/")[-2]
        
        if next_to_last == 'categories':
            return redirect(url_path)
        
        return redirect('wishlist')

    else:
        messages.warning(request, 'You must be logged in to add books to wishlist.')
        return redirect('signInUp')

def removeWishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    Wishlist.objects.get(user=request.user, product=product).delete()
    messages.warning(request, f'"{product.title}" was removed from your whishlist!')
    return redirect('wishlist')

def home(request):
    categories = Category.objects.all()
    cartNum = cartTotal(request)
    wishNum = wishlistTotal(request)
    return render(request, 'products_app/books/home.html', locals())

def categoryBooks(request, categoryTitle):
    category = Category.objects.filter(title=categoryTitle)
        
    if not category:
        return HttpResponseNotFound('<h1>404 - Page not found</h1>')

    if categoryTitle == 'C_C++':
        title = header = 'C/C++ Books'
        
    elif categoryTitle == 'HTML_CSS_JavaScript':
        title = header = 'HTML/CSS/JavaScript Books'

    elif categoryTitle == 'C_Sharp':
        title = header = 'C# Books'

    else:
        title = header = f'{categoryTitle} Books'

    cartNum = cartTotal(request)
    wishNum = wishlistTotal(request)
    books = Product.objects.filter(category__title=categoryTitle)

    if books:
        page_obj = pagination(request, books, 8)

        if request.user.is_authenticated:
            wishlist_books = books.filter(wishlist__in=Wishlist.objects.filter(user=request.user))
            cart_books = books.filter(cart__in=Cart.objects.filter(user=request.user))  

        else:  
            try: 
                title_dict = json.loads(request.COOKIES['CookieTitle']) 
                title = title_dict['title']

                response = redirect(request.META.get('HTTP_REFERER'))
                response.delete_cookie('CookieTitle')
                messages.success(request, f'"{title}" was added to your Cart!') 
                return response 

            except: pass

    else: 
        message = "This category hasn't any book yet."
    
    return render(request, 'products_app/books/categoryBooks.html', locals())

class contactUs(View):
    def get(self, request):
        cartNum = cartTotal(request)
        wishNum = wishlistTotal(request)

        if request.user.is_authenticated:
            initial_dict = {'firstname': request.user.first_name, 'lastname': request.user.last_name, 'email': request.user.email}
            form = ContactForm(initial=initial_dict)
            form.fields['firstname'].widget.attrs['readonly'] = True
            form.fields['lastname'].widget.attrs['readonly'] = True
            form.fields['email'].widget.attrs['readonly'] = True

            form.fields['firstname'].widget.attrs['autofocus'] = False
            form.fields['phone'].widget.attrs['autofocus'] = True
            
        else:
            form = ContactForm()

        return render(request, 'products_app/user/contactUs.html', locals())

    def post(self, request): 
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your message was sent successfully! We will get back you soon.')
            return redirect('contactUs')

        else:
            messages.error(request, 'Your email is invalid, please try again.')
            return redirect('contactUs')
    
def aboutUs(request):
    cartNum = cartTotal(request)
    wishNum = wishlistTotal(request)
    return render(request, 'products_app/user/aboutUs.html', locals())
