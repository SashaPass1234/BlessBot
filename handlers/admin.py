from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.all_kb import kb_admin

ID3 = False
product_id = 0


############################################################# ADMIN #############################################################

async def autor_admin(message: types.Message):
	user = message.from_user
	admin_teg = user.username
	try:
		for ret4 in sqlite_db.cur.execute('SELECT admin_id FROM admins').fetchall():
			if ret4[0] == admin_teg:
				global ID3
				ID3 = True
				await message.answer('Вы успешно авторизовались как админ!', reply_markup=kb_admin)
	except:
		await message.answer('Ошибка базы данных!!!')

class FSMAdmin1(StatesGroup):
	admin_id = State()

async def cm_start1(message: types.Message):
	# if ID3 == True:
		await FSMAdmin1.admin_id.set()
		await message.reply('Загрузи ид админа')

async def load_admin_id(message: types.Message, state: FSMContext):
	# if ID3 == True:
		async with state.proxy() as data:
			data['admin_id'] = message.text

		await message.reply("Вы успешно добавили админа!")
		await state.finish()

		admins = data['admin_id']
		try:
			sqlite_db.cur.execute('INSERT INTO admins (admin_id) VALUES (?)', (admins, ))
			sqlite_db.base.commit()
		except:
			await message.answer('Ошибка базы данных!!!')

async def sql_read(message):
	try:
		for ret3 in sqlite_db.cur.execute('SELECT admin_id FROM admins').fetchall():
			await bot.send_message(message.from_user.id, f'Админ: {ret3[0]}')
	except:
		await message.answer('Ошибка базы данных!!!')


############################################################# crossovki #############################################################

class FSMAdmin(StatesGroup):
	photo1 = State()
	photo2 = State()
	name = State()
	quantity = State()
	size = State()
	ids = State()
	
async def cm_start(message: types.Message):
	if ID3 == True:
		await FSMAdmin.photo1.set()
		await message.reply('Загрузи фото сайзтега')

async def load_photo(message: types.Message, state: FSMContext):
	if ID3 == True:
		async with state.proxy() as data:
			data['photo1'] = message.photo[0].file_id
		await FSMAdmin.next()
		await message.reply("Теперь загрузи фото бирки")

async def load_photo2(message: types.Message, state: FSMContext):
	if ID3 == True:
		async with state.proxy() as data:
			data['photo2'] = message.photo[0].file_id
		await FSMAdmin.next()
		await message.reply("Теперь введи название")

async def load_name(message: types.Message, state: FSMContext):
	if ID3 == True:
		async with state.proxy() as data:
			data['name'] = message.text
		await FSMAdmin.next()
		await message.reply("Теперь введи количество пар")

async def load_quantity(message: types.Message, state: FSMContext):
	if ID3 == True:
		async with state.proxy() as data:
			data['quantity'] = message.text
		await FSMAdmin.next()
		await message.reply("Теперь введи размер")

async def load_size(message: types.Message, state: FSMContext):
	if ID3 == True:
		async with state.proxy() as data:
			data['size'] = message.text
		
		await message.reply("Вы успешно добавили новый продукт!")
		await state.finish()

		global product_id
		product_id += 1

		photo1 = data['photo1']
		photo2 = data['photo2']
		name = data['name']
		size = data['size']
		quantity = data['quantity']

		try:
			sqlite_db.cur.execute('INSERT INTO crossovki (img, img2, name, size, ids, quantity) VALUES (?, ?, ?, ?, ?, ?)', (photo1, photo2, name, size, product_id, quantity))
			sqlite_db.base.commit()
		except:
			await message.answer('Ошибка базы данных!!!')


############################################################# DEL CROSSOVKI #############################################################


class FSMAdmin2(StatesGroup):
	message_delete = State()

async def delete(message: types.Message):
	if ID3 == True:
		await FSMAdmin2.message_delete.set()
		await message.reply('Айдишник для поиска')

async def delete_write(message: types.Message, state: FSMContext):
	if ID3 == True:
		async with state.proxy() as data:
			data['message_delete'] = message.text

		await state.finish()

		textttt = data['message_delete']
		try:
			sqlite_db.cur.execute('SELECT img, img2, name, size, ids, quantity FROM crossovki WHERE ids = ?', (textttt,))
			result = sqlite_db.cur.fetchmany(7)

			if result:
				for value in result:
					keyboard_delete = InlineKeyboardMarkup()
					keyboard_delete.add(InlineKeyboardButton("Удалить продукт", callback_data=f"delete_{value[4]}"))
					keyboard_delete.add(InlineKeyboardButton("Изменить название", callback_data=f"names_{value[4]}"))
					keyboard_delete.add(InlineKeyboardButton("Изменить размер", callback_data=f"sizes_{value[4]}"))
					keyboard_delete.add(InlineKeyboardButton("Изменить количество", callback_data=f"update_{value[4]}"))

					await bot.send_photo(message.from_user.id, value[0])
					await bot.send_photo(message.from_user.id, value[1], f'Название: {value[2]}\nРазмер: {value[3]}\nАйди: {value[4]}\nКоличество пар: {value[5]}', reply_markup=keyboard_delete)
			else:
				response = f'Нет указанного айдишника в базе данных.'
				await message.answer(response)
		except:
			await message.answer('Ошибка базы данных!!!')
############################################################# SELL CROSSOVKI #############################################################

class FSMAdmin3(StatesGroup):
	message_sell = State()

async def sell_products(message: types.Message):
	user = message.from_user
	global user_teg
	user_teg = user.username
	await FSMAdmin3.message_sell.set()
	await message.reply('Айдишник для поиска')

async def sell_write(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['message_sell'] = message.text

	await state.finish()

	textttt = data['message_sell']
	try:
		sqlite_db.cur.execute('SELECT img, img2, name, size, ids, quantity FROM crossovki WHERE ids = ?', (textttt,))
		result = sqlite_db.cur.fetchmany(6)

		if result:
			for value in result:
				keyboard_sell = InlineKeyboardMarkup()
				keyboard_sell.add(InlineKeyboardButton("ЗАБРОНИРОВАТЬ", callback_data=f"sell_{value[4]}"))

				await bot.send_photo(message.from_user.id, value[0])
				await bot.send_photo(message.from_user.id, value[1], f'Название: {value[2]}\nРазмер: {value[3]}\nАйди: {value[4]}\nКоличество пар: {value[5]}', reply_markup=keyboard_sell)
		else:
			response = f'Нет указанного айдишника в базе данных.'
			await message.answer(response)

	except:
		await message.answer('Ошибка базы данных!!!')

############################################################# SETCOUNT CROSSOVKI #############################################################


class SetCount(StatesGroup):
	waiting1 = State()
	waiting2 = State()
	waiting3 = State()
	waiting4 = State()
	waiting5 = State()
	waiting6 = State()
	waiting7 = State()
	waiting8 = State()
	waiting9 = State()
	waiting10 = State()
	waiting11 = State()
		
@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
	# if ID3 == True:
	data = callback_query.data.split('_')

	global set_ids
	set_ids = data[1]
	
	if data[0] == "delete":
		try:
			sqlite_db.cur.execute("DELETE FROM crossovki WHERE ids=?", (data[1],))
			sqlite_db.base.commit()
		except:
			await bot.send_message(callback_query.message.chat.id, "Ошибка базы данных!!!")

		await bot.send_message(callback_query.message.chat.id, "Продукт удалён из базы данных!")

	elif data[0] == "update":
		await bot.send_message(callback_query.message.chat.id, "Введи новое количество пар:")
		await SetCount.waiting1.set()

	elif data[0] == "names":
		await bot.send_message(callback_query.message.chat.id, "Введи новое название пары:")
		await SetCount.waiting2.set()

	elif data[0] == "sizes":
		await bot.send_message(callback_query.message.chat.id, "Введи новый размер пары:")
		await SetCount.waiting3.set()


############################################################# SELL CROSSOVKI #############################################################


	elif data[0] == "sell":
		try:
			sqlite_db.cur.execute('SELECT img, img2, name, size, ids, quantity FROM crossovki WHERE ids = ?', (data[1],))
			global result4
			result4 = sqlite_db.cur.fetchmany(6)
			if result4:
				for value in result4:
					global quantity2
					quantity2 = int(value[5])

					await bot.send_message(callback_query.message.chat.id, "Введи количество пар которые вы хотите забронировать:")
					await SetCount.waiting4.set()
			else:
				response = f'Продукт с этим айдишником имеет бронь!❌'
				await bot.send_message(callback_query.message.chat.id, response)
		except:
			await bot.send_message(callback_query.message.chat.id, "Продукт удалён из базы данных!")

@dp.message_handler(state=SetCount.waiting4)
async def update_size(message: types.Message, state):
	global set_ids
	global quantity
	quantity = int(message.text)
	global user_teg
	global quantity2
	quantity2 -=quantity

	try:
		sqlite_db.cur.execute("UPDATE crossovki SET quantity=? WHERE ids=?", (quantity2, set_ids))
		sqlite_db.base.commit()
	except:
		await message.answer("Продукт удалён из базы данных!")

	await state.finish()
	await bot.send_message(message.chat.id, "Введи цену:")
	await SetCount.waiting5.set()

@dp.message_handler(state=SetCount.waiting5)
async def update_sdfsdf(message: types.Message, state):
	global set_ids
	global quantity3
	quantity3 = message.text
	await state.finish()
	await bot.send_message(message.chat.id, "Введи название - это личка или доставка?")
	await SetCount.waiting6.set()


@dp.message_handler(state=SetCount.waiting6)
async def update_sdfsdf(message: types.Message, state):
	global set_ids
	global quantity4
	quantity4 = message.text
	if quantity4 == 'личка':
		await state.finish()
		await bot.send_message(message.chat.id, "Введите время/дата:")
		await SetCount.waiting7.set()
	elif quantity4 == 'доставка':
		await state.finish()
		await bot.send_message(message.chat.id, "Загрузите фотку доставки:")
		await SetCount.waiting8.set()

@dp.message_handler(state=SetCount.waiting7)
async def update_sdfsdf(message: types.Message, state):
	global set_ids
	quantity5 = message.text
	global quantity2
	global quantity3
	global quantity1
	global user_teg
	if result4:
		for value in result4:
			group_id = -1002210462273
			await bot.send_message(group_id, f'ПОЛЬЗОВАТЕЛЬ @{user_teg} ВЗЯЛ ЛИЧКУ\n\nНазвание: {value[2]}\nРазмер: {value[3]}\nЦена: {quantity3}\nВремя: {quantity5}\nКоличество пар забронировал: {quantity}')
			await bot.send_message(message.chat.id, f"Вы взяли доставку ✅")

	await state.finish()


@dp.message_handler(content_types=['photo'], state=SetCount.waiting8)
async def update_sdfsdf(message: types.Message, state):
	global set_ids
	global quantity6
	quantity6 = message.photo[0].file_id
	await state.finish()
	await bot.send_message(message.chat.id, "Введите время:")
	await SetCount.waiting9.set()

@dp.message_handler(state=SetCount.waiting9)
async def update_sdfsdf(message: types.Message, state):
	global set_ids
	global quantity7
	quantity7 = message.text
	await state.finish()
	await bot.send_message(message.chat.id, "Введите пункт выдачи:")
	await SetCount.waiting10.set()

@dp.message_handler(state=SetCount.waiting10)
async def update_sdfsdf(message: types.Message, state):
	global set_ids
	global quantity8
	quantity8 = message.text
	await state.finish()
	await bot.send_message(message.chat.id, "Введите трек номер:")
	await SetCount.waiting11.set()

@dp.message_handler(state=SetCount.waiting11)
async def update_sdfsdf(message: types.Message, state):
	global set_ids
	global quantity
	global quantity3
	global quantity6
	global quantity7
	global quantity8
	global quantity9
	quantity9 = message.text
	await state.finish()
	if result4:
		for value in result4:
			group_id = -1002210462273
			await bot.send_photo(group_id, quantity6, f'ПОЛЬЗОВАТЕЛЬ @{user_teg} ОТПРАВИЛ ДОСТАВКУ\n\nНазвание: {value[2]}\nРазмер: {value[3]}\nЦена: {quantity3}\nВремя: {quantity7}\nПункт выдачи: {quantity8}\nТрек номер: {quantity9}\nКоличество пар забронировал: {quantity}')
			await bot.send_message(message.chat.id, f"Вы взяли личку ✅")


############################################################# EDIT CROSSOVKI #############################################################


@dp.message_handler(state=SetCount.waiting1)
async def update_quantity(message: types.Message, state):
	global set_ids
	quantity = message.text
	try:
		sqlite_db.cur.execute("UPDATE crossovki SET quantity=? WHERE ids=?", (quantity, set_ids))
		sqlite_db.base.commit()
	except:
		await message.answer("Продукт удалён из базы данных!")

	await state.finish()
	await bot.send_message(message.chat.id, "Успешно изменнено.")

@dp.message_handler(state=SetCount.waiting2)
async def update_name(message: types.Message, state):
	global set_ids
	quantity = message.text
	sqlite_db.cur.execute("UPDATE crossovki SET name=? WHERE ids=?", (quantity, set_ids))
	sqlite_db.base.commit()
	await state.finish()
	await bot.send_message(message.chat.id, "Успешно изменнено.")

@dp.message_handler(state=SetCount.waiting3)
async def update_size(message: types.Message, state):
	global set_ids
	quantity = message.text
	try:
		sqlite_db.cur.execute("UPDATE crossovki SET size=? WHERE ids=?", (quantity, set_ids))
		sqlite_db.base.commit()
	except:
		await message.answer( "Продукт удалён из базы данных!")

	await state.finish()
	await bot.send_message(message.chat.id, "Успешно изменнено.")



############################################################# CANCEL #############################################################


async def cancel_handler(message: types.Message, state: FSMContext):
	if ID3 == True:
		current_state = await state.get_state()
		if current_state is None:
			return
		await state.finish()
		await message.reply('OK')


############################################################# ALL FUNC #############################################################

def register_handlers_admin(dp: Dispatcher):
	dp.register_message_handler(autor_admin, commands=['admin'])
	dp.register_message_handler(sql_read, commands='all_admin')
	dp.register_message_handler(cm_start1, commands='add_admin', State=None)
	dp.register_message_handler(load_admin_id, state=FSMAdmin1.admin_id)

	dp.register_message_handler(cm_start, commands='new_crossovki', state=None)
	dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo1)
	dp.register_message_handler(load_photo2, content_types=['photo'], state=FSMAdmin.photo2)
	dp.register_message_handler(load_name, state=FSMAdmin.name)
	dp.register_message_handler(load_quantity, state=FSMAdmin.quantity)
	dp.register_message_handler(load_size, state=FSMAdmin.size)
	
	dp.register_message_handler(sell_products, commands='sell_product', state=None)
	dp.register_message_handler(sell_write, state=FSMAdmin3.message_sell)


	dp.register_message_handler(delete, commands='edit', state=None)
	dp.register_message_handler(delete_write, state=FSMAdmin2.message_delete)

	
	dp.register_message_handler(cancel_handler, state="*", commands='отмена')
	dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
