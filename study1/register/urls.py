# urls.py
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views as v

app_name = 'main'

urlpatterns = [
    path("home/", v.home, name="home"),
    path("pay/", v.Pay, name="pay"),
    path('help/', v.Help, name='help'),
    path('contact/', v.Contact, name='contact'),
    path('profile/', v.Profile, name='profile'),
    path('profile/update/', v.UpdateProfile, name='update-profile'),
    path('resgister/', v.Register, name='register'),
    path('booklist/', v.BookListView.as_view(), name='books'),
    path('booklist/search', v.BookSearchView.as_view(), name='book-search'),
    path('book/<int:pk>', v.BookDetailView.as_view(), name='book-detail'),
    path('shoppingcart/', v.ShoppingCart, name='shopping-cart'),
    path('shoppingcart/add/<int:pk>', v.AddToCart, name='add-to-cart'),
    path('shoppingcart/remove/<int:pk>', v.RemoveFromCart, name='remove-from-cart'),
    path('shoppingcart/checkout/', v.Checkout, name='checkout'),
]