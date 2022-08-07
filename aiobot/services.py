from typing import Tuple
from login.models import User
import django.contrib.auth.models
from asgiref.sync import sync_to_async


async def check_user(user_id: int, user_name: str):
    return await User.objects.filter(user_id=user_id, user_name=user_name).aexists()


@sync_to_async
def save_user(username, password):
    username = username
    print (username)
    user = django.contrib.auth.models.User.objects.get(username=str(username))
    user.set_password(password)
    user.save()


async def add_user(user_id: int, user_name: str, user_email: str, user_password: str) -> Tuple[User, bool]:
    return await User.objects.aupdate_or_create(
        user_id=user_id, user_name=user_name, defaults={'user_email': user_email, 'user_password': user_password},
    )


async def edit_user(user_id: int, user_email: str, user_password: str):
    user = await User.objects.aget(user_id)
    user.user_email = user_email
    user.user_password = user_password
    user.save()
