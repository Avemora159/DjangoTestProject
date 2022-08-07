from aiogram.contrib.fsm_storage.memory import MemoryStorage
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from sys import exit
from asgiref.sync import async_to_sync, sync_to_async
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiobot import services
import logging

users = {'bogdan': 1799244985, 'lovelas': 1836086969, 'threadx': 424035498}


class Form(StatesGroup):
    email = State()
    password = State()
    confirm_password = State()


class Command(BaseCommand):
    help = 'Start telegram-bot'

    def handle(self, *args, **options):
        bot_token = settings.TOKEN
        storage = MemoryStorage()
        if not bot_token:
            exit("Error: no token provided")

        bot = Bot(token=bot_token)
        dp = Dispatcher(bot, storage=storage)
        logging.basicConfig(level=logging.INFO)

        @dp.message_handler(commands=["cancel"], state='*')
        async def cancel(message: types.Message, state: FSMContext):
            await state.finish()
            await message.answer("<b>Canceled.</b>", parse_mode=types.ParseMode.HTML)

        @dp.message_handler(commands=["start", "edit"])
        async def start(message: types.Message):
            if message.from_user.id in users.values():
                if await services.check_user(message.from_user.id, message.from_user.username) \
                        and message.html_text != '/edit':
                    await message.answer('You are already registered, use /edit')
                else:
                    if message.html_text == '/edit':
                        await message.answer('<b>Begin edition</b>', parse_mode=types.ParseMode.HTML)
                    else:
                        await message.answer('<b>Begin registration</b>', parse_mode=types.ParseMode.HTML)
                    await Form.email.set()
                    await message.answer("Enter your email:")
            else:
                await message.answer('You are not in the dictionary...')

        @dp.message_handler(state=Form.email)
        async def process_email(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['email'] = message.text
            await Form.next()
            await message.answer('Password:')

        @dp.message_handler(state=Form.password)
        async def process_password(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['password'] = message.text
                await Form.next()
                await message.answer('Confirm password:')

        @dp.message_handler(state=Form.confirm_password)
        async def process_confirm(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                if data['password'] != message.text:
                    await Form.previous()
                    await message.answer('Bad confirmation, try again. Enter your password:')
                else:
                    user, is_created = await services.add_user(
                        user_id=message.from_user.id,
                        user_name=message.from_user.username,
                        user_email=data['email'],
                        user_password=data['password']
                    )
                    # if not User.objects.filter(user_name=message.from_user.username).aexists():
                    user, is_created = await User.objects.aupdate_or_create(
                        username=message.from_user.username,
                        email=data['email'],
                    )
                    await services.save_user(message.from_user.username, data['password'])
                    await state.finish()
                    if not is_created:
                        await message.answer('Update successful.')
                    else:
                        await message.answer('Registration successful.')

        executor.start_polling(dp, skip_updates=True)
