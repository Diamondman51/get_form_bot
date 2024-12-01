from datetime import datetime
import sys
from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from sqlalchemy import exists, select, func
from sqlalchemy.orm import selectinload
from keyboards.keyboards import *
from database.models import User, UserForms, session
from states.states import GetDate, GetForm, GetLoc, GetPhone
from aiogram.enums import ParseMode
import dotenv
import os
import xlsxwriter


dotenv.load_dotenv()


async def start_command_handler(message: types.Message, state: FSMContext) -> None:
    
    from_user = message.from_user

    user = select(exists().where(User.user_tg_id == from_user.id))

    async with session() as conn:
        res = await conn.execute(user)
        res = res.scalar()
        if from_user.id == int(os.getenv('admin_id')):
            greeting_text = f"С возвращением, Админ! Чем могу помочь?"
            await message.answer(greeting_text, reply_markup=admin_keyboards)
        elif res:
            greeting_text = f"С возвращением, {from_user.full_name}! Чем могу помочь?"
            await message.answer(greeting_text, reply_markup=send_form)
        else:
            greeting_text = f"Здравствуйте, давайте для начала пройдем регистрацию"
            await message.answer(greeting_text, reply_markup=registration_key)


async def make_excel_file(forms: UserForms):
    print('Making file')
    async with session() as conn:    
        workbook = xlsxwriter.Workbook(f"forms/forms.xlsx")
        worksheet = workbook.add_worksheet()


        # Write some data
        worksheet.write("A1", "Имя и Фамилия")
        worksheet.write("B1", "Никнейм")
        worksheet.write("C1", "Телефон номер")
        worksheet.write("D1", "Название вещи")
        worksheet.write("E1", "Цена")
        worksheet.write("F1", "Долгота")
        worksheet.write("G1", "Широта")
        worksheet.write("H1", "Время заполнения")
        data = [(form.user.full_name, 
                 form.user.username,
                 form.user.phone,
                 form.name,
                 form.price,
                 form.longitude,
                 form.latitude,
                 form.created_at) for form in forms if form.user and form.user.user_tg_id]
    date_format = workbook.add_format({'num_format': 'YYYY-mm-dd, hh:mm:ss'})
    # Write multiple rows efficiently
    for row, (full_name, 
            username,
            phone,
            name,
            price,
            longitude,
            latitude,
            created_at) in enumerate(data, start=1):
        worksheet.write(row, 0, full_name)
        worksheet.write(row, 1, username)
        worksheet.write(row, 2, phone)
        worksheet.write(row, 3, name)
        worksheet.write(row, 4, price)
        worksheet.write(row, 5, longitude)
        worksheet.write(row, 6, latitude)
        worksheet.write(row, 7, created_at, date_format)

# # Close the workbook
    workbook.close()


async def get_all_forms(message: types.Message, bot: Bot) -> None:
    if message.from_user.id == int(os.getenv('admin_id')):
        await message.answer("Пожалуйста подождите, ваш файл собирается.")
        async with session() as conn:
            forms = select(UserForms).options(selectinload(UserForms.user))
            res = await conn.execute(forms)
            # print(res.all())
            forms = res.scalars()
        await make_excel_file(forms)
        file = r"E:\kwork-bot\forms\forms.xlsx"
        # await message.reply_document(document=types.FSInputFile(file))
        await bot.send_document(chat_id=os.getenv('admin_id'), document=types.FSInputFile(file))
        try:
            os.remove('forms/forms.xlsx')
        except:
            pass
    else:
        # await message.answer(f"Извините, это команда для администратора. Если хотите такой же бот, обращайтесь к этому аккаунту: <a>@Diamondman51</a>")
        await message.answer(f"Извините, это команда для администратора.")


async def get_forms_by_date(message: types.Message, state: FSMContext)-> None:
    admin = int(os.getenv('admin_id'))
    if message.from_user.id == admin:
        await message.answer("Введите дату как на примере:\n<b>2024-11-30</b>")
        await state.set_state(GetDate.date)
    else:
        # await message.answer(f"Извините, это команда для администратора. Если хотите такой же бот, обращайтесь к этому аккаунту: <a>@Diamondman51</a>")
        await message.answer(f"Извините, это команда для администратора.")


async def get_date(message: types.Message, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    date = message.text
    format_of_date = '%Y-%m-%d'
    formatted_date = datetime.strptime(date, format_of_date)
    await sort_forms_by_date(bot, formatted_date)


async def get_user_location(message: types.Message, state: FSMContext) -> None:
    await message.answer('Введите долготу и широту: ')
    await state.set_state(GetLoc.loc)


async def send_loc(message: types.Message, state: FSMContext) -> None:
    longitude, latitude = message.text.split(" ")
    await message.reply_location(latitude=latitude, longitude=longitude, reply_markup=admin_keyboards)


async def sort_forms_by_date(bot: Bot, formatted_date: datetime) -> None: 
    admin = os.getenv("admin_id")
    async with session() as conn:
        forms = select(UserForms).options(selectinload(UserForms.user)).filter(func.DATE(UserForms.created_at) == formatted_date.date())
        res = await conn.execute(forms)
        forms = res.scalars().all()
        
    if forms:
        await make_excel_file(forms)
        file = r"E:\kwork-bot\forms\forms.xlsx"
        await bot.send_document(chat_id=admin, document=types.FSInputFile(file), reply_markup=admin_keyboards)

        try:
            os.remove('forms/forms.xlsx')
        except:
            pass
    else:
        await bot.send_message(chat_id=admin, text='Нет форм по этой дате', reply_markup=admin_keyboards)


async def do_not_verify(callback: types.CallbackQuery) -> None:
    # await callback.answer()
    await callback.answer("Без регистрации не сможете пользоваться этим ботом", show_alert=True)


async def verify(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.answer('Пожалуйста, отправьте свой номер телефона', 
                                  reply_markup=phone_number_key)
    await state.set_state(GetPhone.phone)


async def get_phone(message: types.Message, state: FSMContext) -> None:
    async with session() as conn:
        contact = message.contact
        if contact:
            user = User(user_tg_id=message.from_user.id, 
                    full_name=message.from_user.full_name,
                    username=message.from_user.username,
                    phone=contact.phone_number)
            conn.add(user)
            await conn.commit()
            await message.answer('Спасибо за регистрацию. Теперь вы можете пользоваться ботом и заполнить формы, нажав на кнопку <b>"Отправить форму"</b>', reply_markup=send_form, parse_mode=ParseMode.HTML)
            await state.clear()
        else:
            await message.answer('Вы отправили неправильный контакт. \nПожалуйста, отправьте свой номер телефона нажав на кнопку <b>"Отправить номер телефона"</b>', reply_markup=phone_number_key, parse_mode=ParseMode.HTML)


async def get_form(message: types.Message, state: FSMContext) -> None:
    await message.answer('Введите название: ', reply_markup=None)
    await state.set_state(GetForm.name)


async def get_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer("Введите цену: ")
    await state.set_state(GetForm.price)


async def get_price(message: types.Message, state: FSMContext) -> None:
    await state.update_data(price=message.text)
    await message.answer('Отправьте местоположение: ', reply_markup=send_loc)
    await state.set_state(GetForm.longitude)


async def get_location(message: types.Message, state: FSMContext, bot: Bot) -> None:
    if message.location:
        data = await state.get_data()
        longitude = message.location.longitude
        latitude = message.location.latitude
        print("Location", longitude, latitude)
        await state.clear()
    
        name = data.get("name")
        price = data.get("price")
        username = message.from_user.username
        full_name = message.from_user.full_name
        admin_id = os.getenv("admin_id")
        async with session() as conn:
            user_form = UserForms(user_id=message.from_user.id, name=name,
                                price=price, 
                                longitude=longitude, 
                                latitude=latitude)
            conn.add(user_form)
            await conn.commit()
            user = select(User).where(User.user_tg_id == message.from_user.id)
            res = await conn.execute(user)
            user = res.scalar()

            await message.answer("Спасибо, форма успешно заполнена", reply_markup=send_form)
            text = f'''Название: {name}
Цена: {price}
Никнейм: {username}
Имя: {full_name}
Телефон номер: {user.phone}
Локация: '''
            await bot.send_message(chat_id=admin_id, text=text)
            await bot.send_location(chat_id=admin_id, longitude=longitude, latitude=latitude, proximity_alert_radius=45)
        
    else:
        await message.answer('Пожалуйста, правильно отправьте локацию', reply_markup=send_loc)
        await state.set_state(GetForm.longitude)