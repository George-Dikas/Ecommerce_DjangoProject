from django.urls import path
from .views import *
from .utils import verifLink, forgotPass, passResetSent, passResetConfirm, passResetComplete
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Function-based views
    path('verification/<uidb64>/<token>', verifLink, name='verifLink'),
    path('profile/delete', delProfile, name='delProfile'),
    path('logout/', logOut, name='logOut'),
    path('searchResults', search, name='search'),
    path('orders/', orders, name='orders'),
    path('cancelation/<int:order_id>', cancelation, name='cancelation'),
    path('cart/', cart, name='cart'),
    path('addCart/<int:product_id>', addCart, name='addCart'),
    path('cart/removeCart/', removeCart, name='removeCart'),
    path('cart/minusQuantity', minusQuantity, name='minusQuantity'),
    path('cart/plusQuantity', plusQuantity, name='plusQuantity'),
    path('wishlist/', wishlist, name='wishlist'),
    path('addWishlist/<int:product_id>', addWishlist, name='addWishlist'),
    path('removeWishlist/<int:product_id>', removeWishlist, name='removeWishlist'),
    path('home/', home, name='home'),
    path('categories/<str:categoryTitle>', categoryBooks, name='categoryBooks'),
    path('aboutUs/', aboutUs, name='aboutUs'),
    
    # Class-based views
    path('singInUp/', signInUp.as_view(), name='signInUp'),
    path('singInUp/forgottenPassword/', forgotPass.as_view(), name='forgotPass'),
    path('singInUp/passwordResetSent/', passResetSent.as_view(), name='passResetSent'),
    path('singInUp/<uidb64>/<token>/', passResetConfirm.as_view(), name='passResetConfirm'),
    path('singInUp/PasswordResetComplete/', passResetComplete.as_view(), name='passResetComplete'),
    path('profile/', profile.as_view(), name='profile'),
    path('cart/checkout/', checkout.as_view(), name='checkout'),
    path('contactUs/', contactUs.as_view(), name='contactUs')

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
