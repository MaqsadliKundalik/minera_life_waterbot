from aiogram.types import Message, ReplyKeyboardRemove
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Command
from data import db
from states.states import *
from keyboards.default.allkeyboards import *


@dp.message_handler(CommandStart())
async def start_command_answer(message: Message):
    user = db.get_user(message.from_user.id)
    if user:
        if user["login"]:
            await message.answer("Assalomu alaykum, admin!", reply_markup=start_command_keyboards)
        else:
            await message.answer("Assalomu alaykum, zakaz id raqamini kiriting.")
    else:
        db.add_user(message.from_user.id, "", "")
        await message.answer("Assalomu alaykum, zakaz id raqamini kiriting.")


@dp.message_handler(Command("water"))
async def log_in_admin(message: Message):
    await message.answer("Login kiriting.")
    await log_in_admin_state.login.set()

@dp.message_handler(state=log_in_admin_state.login)
async def check_login_answer(message: Message, state: FSMContext):
    if message.text.lower() == "minera life water admin":
        await state.update_data(login=message.text)
        await message.answer("Parolni kiriting.")
        await log_in_admin_state.parol.set()

    else:
        await message.answer("Login noto'g'ri!")

@dp.message_handler(state=log_in_admin_state.parol)
async def check_parol_answer(message: Message, state:FSMContext):
    if message.text.lower() == "mineralifeparol":
        data = await state.get_data()
        db.set_admin(message.from_user.id, "minera life water admin", "mineralifeparol")
        await message.answer("Xush kelibsiz, admin!", reply_markup=start_command_keyboards)
        await state.finish()
    else: await message.answer("Noto'g'ri parol!")




@dp.message_handler(lambda message: message.text == "zakaz qo'shish")
async def add_location_answer(message: Message):
    user = db.get_user(message.from_user.id)
    if user:
        if user["login"]:
            await message.answer("Zakaz uchun yangi ID kiriting.", reply_markup=cancel_keyboard)
            await add_location_state.id.set()
        else:
            await get_location_answer(message)
    else:
        await get_location_answer(message)

@dp.message_handler(state=add_location_state.id)
async def add_location_id_answer(message: Message, state: FSMContext):
    if message.text != "🚫 Bekor qilish":
        await state.update_data(id=message.text)
        await message.answer("Endi menga buyurtmachi ismini kiriting.")
        await add_location_state.name.set()
    else:
        await state.finish()
        await message.answer("Jarayon bekor qilindi!", reply_markup=start_command_keyboards)


@dp.message_handler(state=add_location_state.name)
async def add_location_name_answer(message: Message, state: FSMContext):
    if message.text != "🚫 Bekor qilish":
        await state.update_data(name=message.text)
        await message.answer("Endi menga buyurtmachi telefon raqamini kiriting.")
        await add_location_state.phone.set()
    else:
        await state.finish()
        await message.answer("Jarayon bekor qilindi!", reply_markup=start_command_keyboards)

@dp.message_handler(state=add_location_state.phone)
async def add_location_phone_answer(message: Message, state: FSMContext):
    if message.text != "🚫 Bekor qilish":
        await state.update_data(phone=message.text)
        await message.answer("Endi menga buyurtma haqida izoh yuboring.")
        await add_location_state.about.set()
    else:
        await state.finish()
        await message.answer("Jarayon bekor qilindi!", reply_markup=start_command_keyboards)

@dp.message_handler(state=add_location_state.about)
async def add_location_about_answer(message: Message, state: FSMContext):
    if message.text != "🚫 Bekor qilish":
        await state.update_data(about=message.text)
        await message.answer("Endi menga lokatsiyani yuboring.")
        await add_location_state.location.set()
    else:
        await state.finish()
        await message.answer("Jarayon bekor qilindi!", reply_markup=start_command_keyboards)

@dp.message_handler(content_types=["location", "text"], state=add_location_state.location)
async def add_location_location_answer(message: Message, state: FSMContext):
    if message.text != "🚫 Bekor qilish":
        if message.location:
            await state.update_data(latitude=message.location.latitude)
            await state.update_data(longitude=message.location.longitude)
            data = await state.get_data()
            await message.answer_location(data.get("latitude"), data.get("longitude"))
            await bot.send_message(message.from_user.id, f"ID: {data.get('id')}\nIsm: {data.get('name')}\nTelefon raqam: {data.get('phone')}\ntavsif: {data.get('about')}")
            await message.answer("Ma'lumotlar to'g'rimi?", reply_markup=confirmation_keyboards)
            await add_location_state.confirm.set()
        else:
            await message.answer("Menga lokatsiya yuboring.")
    else:
        await state.finish()
        await message.answer("Jarayon bekor qilindi!", reply_markup=start_command_keyboards)


@dp.message_handler(state=add_location_state.confirm)
async def add_location_confirm_answer(message: Message, state: FSMContext):
    if message.text.lower() == "ha":
        data = await state.get_data()
        db.add_location(
            data.get("id").lower(),
            data.get("name"),
            data.get("phone"),
            data.get("about"),
            data.get("latitude"),
            data.get("longitude")
        )
        await message.answer("Lokatsiya va uning ma'lumotlar saqlandi!")
        await state.finish()
        await message.answer("Bosh menyudasiz!", reply_markup=start_command_keyboards)
    elif message.text.lower() == "yo'q":
        await state.finish()
        await message.answer("Jarayon bekor qilindi!", reply_markup=start_command_keyboards)
    else:
        await message.answer("Pastdagi tugmalardan birini tanlang.", reply_markup=confirmation_keyboards)


@dp.message_handler(lambda message: message.text == "zakaz o'chirish")
async def del_location_answer(message: Message):
    user = db.get_user(message.from_user.id)
    if user:
        if user["login"]:
            await message.answer("Zakaz idsini kiriting.", reply_markup=cancel_keyboard)
            await del_location_state.id.set()
        else:
            await get_location_answer(message)
    else:
        await get_location_answer(message)

@dp.message_handler(state=del_location_state.id)
async def del_location_id_answer(message: Message, state:FSMContext):
    if message.text != "🚫 Bekor qilish":
        if db.remove_location(message.text.lower()):
            await message.answer("Zakaz o'chirildi!", reply_markup=start_command_keyboards)
            await state.finish()
        else:
            await message.answer("Zakaz topilmadi. Fikringizdan qaytgan bo'lsangiz 🚫 Bekor qilish tugmasidan foydalaning.")
    else:
        await state.finish()
        await message.answer("Jarayon bekor qilindi!", reply_markup=start_command_keyboards)

@dp.message_handler(lambda message: message.text == "chiqish")
async def log_oyt_answer(message: Message):
    user = db.get_user(message.from_user.id)
    if user:
        if user["login"]:
            db.set_admin(message.from_user.id, "", "")
            await message.answer("Admin hisobidan chiqdingiz!", reply_markup=ReplyKeyboardRemove())
        else:
            await get_location_answer(message)
    else:
        await get_location_answer(message)



@dp.message_handler()
async def get_location_answer(message: Message):
    user = db.get_user(message.from_user.id)

    data = db.get_location(message.text.lower())
    if user:
        if user["login"]:
            if message.text != "🚫 Bekor qilish":
                if data:
                    await bot.send_location(message.from_user.id, data["latitude"], data["longitude"])
                    await bot.send_message(message.from_user.id,
                                           f"ID: {data['id']}\nIsm: {data['name']}\nTelefon raqam: {data['phone']}\ntavsif: {data['about']}")
                else:
                    await message.answer("Noto'g'ri ID kiritildi!")
            else:
                await message.answer("Bosh menyudasiz!", reply_markup=start_command_keyboards)
        else:
            if data:
                await bot.send_location(message.from_user.id, data["latitude"], data["longitude"])
                await bot.send_message(message.from_user.id,
                                       f"ID: {data['id']}\nIsm: {data['name']}\nTelefon raqam: {data['phone']}\ntavsif: {data['about']}")
            else:
                await message.answer("Noto'g'ri ID kiritildi!")
    else:
        await start_command_answer(message)
