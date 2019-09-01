from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import UserInfo

# Register your models here.

class UserInfoAdmin(admin.ModelAdmin):
        list_display = [            
        "student_ID",
        "mailing_Address",
        "billing_Address",
        "credit_Card_Type",
        "credit_Card_Number",
        "expiration_Date",
    ]
'''
    def user_info(self, obj):
        return obj.student_ID
'''
'''
    def get_queryset(self, request):
        queryset = super(UserInfoAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-phone', 'user')
        return queryset

    user_info.short_description = 'Info'
'''
admin.site.register(UserInfo, UserInfoAdmin)
