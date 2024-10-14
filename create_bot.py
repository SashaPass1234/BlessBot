from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

API_TOKEN = '6250216616:AAHFP2asefqoW5fu3dkHrFW9n4v4c5okKEk'
bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=storage)
