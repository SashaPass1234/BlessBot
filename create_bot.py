from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

API_TOKEN = 'YOUR_API_TOKEN' #TOKEN TELEGRAM BOTS
bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=storage)
