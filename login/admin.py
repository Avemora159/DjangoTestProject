from django.contrib import admin
from login.models import User
from login.forms import UserForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'user_name', 'user_email')
    form = UserForm
