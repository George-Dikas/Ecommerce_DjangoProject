from django.contrib.auth import views
from .forms import ForgotForm, ConfirmForm
from .models import Wishlist, Cart
from django.urls import reverse_lazy
from django.contrib import messages
import json
from django.core.paginator import Paginator

#All Verification and Purchase Email Imports 
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, EmailMultiAlternatives
from .tokens import account_activation_token
from django.contrib.auth import logout


def verifEmail(request, user, to_email):
    subject = 'Account Verification'
    message = render_to_string('products_app/user/verificationEmail.html',
    {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(subject, message, to=[to_email])

    if email.send():
        messages.success(request, 'Thank you for registering! Please check you email to verify your account.')
    
    else: 
        messages.error(request, f'Problem sending email to {to_email}, please check if you typed it correctly.')

def verifLink(request, uidb64, token): 
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.registered.is_verified = True
        user.registered.save()
        messages.success(request, 'Thank you for your account verification. Now you can sign into your account!') 

    else:
        messages.error(request, 'The verification link you followed has expired.') 
        
    logout(request)
    return redirect('signInUp')

class forgotPass(views.PasswordResetView):
    template_name = 'products_app/user/forgotPass/forgottenPassword.html'
    email_template_name = 'products_app/user/forgotPass/passwordResetEmail.html'
    form_class = ForgotForm
    success_url = reverse_lazy('passResetSent')

    def form_invalid(self, form):
        messages.warning(self.request, 'Something went wrong with email address. Please try again.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {}), 'cartNum': cartTotal(self.request), 
            'wishNum': wishlistTotal(self.request)}
        )
        return context

class passResetSent(views.PasswordResetDoneView): 
    template_name = 'products_app/user/forgotPass/passwordResetSent.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {}), 'cartNum': cartTotal(self.request), 
            'wishNum': wishlistTotal(self.request)}
        )
        return context

class passResetConfirm(views.PasswordResetConfirmView): 
    template_name = 'products_app/user/forgotPass/passwordResetConfirm.html'
    success_url = reverse_lazy('passResetComplete')
    form_class = ConfirmForm

    def form_invalid(self, form):
        messages.warning(self.request, 'Something went wrong while trying to change password. Please try again.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {}), 'cartNum': cartTotal(self.request), 
            'wishNum': wishlistTotal(self.request)}
        )
        return context

class passResetComplete(views.PasswordResetCompleteView): 
    template_name = 'products_app/user/forgotPass/passwordResetComplete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {}), 'cartNum': cartTotal(self.request), 
            'wishNum': wishlistTotal(self.request)}
    )
        return context

def cartTotal(request):
    if request.user.is_authenticated:
        return len(Cart.objects.filter(user=request.user))

    else:
        try:
            return len(json.loads(request.COOKIES['CookieCart']))

        except: return 0

def totals(amount_bef, cartbook_total, operation='-'):
    total_amount = 0

    if operation == '-':
        amount = amount_bef - cartbook_total

        if amount:
            total_amount = amount + 20

    else:
        amount = amount_bef + cartbook_total
        total_amount = amount + 20

    return (amount, total_amount)

def purchaseEmail(request, data):
    subject = 'Completed Purchase'
    html_content = render_to_string('products_app/user/purchaseEmail.html',
    {
        'firstname': data['order'].firstname,
        'lastname': data['order'].lastname,
        'email': data['order'].email,
        'phone': data['order'].phone,
        'address': data['order'].address,
        'city': data['order'].city,
        'zipcode': data['order'].zipcode,
        'transaction_id': data['order'].transaction_id,
        'cart_books': data['cart_books'],
        'total_amount': data['total_amount']
    })

    message = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, to=[data['order'].email])
    email.attach_alternative(html_content, 'text/html')
    email.send()
    
def wishlistTotal(request):
    num = 0

    if request.user.is_authenticated:
        num = len(Wishlist.objects.filter(user=request.user))
    
    return num

def pagination(request, list, num):
    paginator = Paginator(list, num)   
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)