from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import UserInfo, Book, BookInstance, Author, Professor, CreditCard, OrderItems, Order

# Register your models here.

admin.site.register(UserInfo)
admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Author)
admin.site.register(Professor)
admin.site.register(CreditCard)
admin.site.register(OrderItems)
admin.site.register(Order)