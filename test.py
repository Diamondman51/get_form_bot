from datetime import datetime
import os
from venv import create
import time
import xlsxwriter
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from tgbot.database.models import session, User, UserForms
import asyncio


async def get():
    print('Making file')
    async with session() as conn:    
        workbook = xlsxwriter.Workbook(f"forms/forms.xlsx")
        worksheet = workbook.add_worksheet()
        forms = select(UserForms).options(selectinload(UserForms.user))
        users = select(User)
        users = await conn.execute(users)
        users = users.scalars()
        res = await conn.execute(forms)
        # print(res.all())
        forms = res.scalars()

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
                 form.created_at) for form in forms if form.user.user_tg_id in [user.user_tg_id for user in users]]
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

    # await asyncio.sleep(5)
    try:
        await os.remove('forms/forms.xlsx')
    except:
        pass       


async def g():
    async with session() as conn:
        users = select(User)
        users = await conn.execute(users)
        users = users.unique().scalars().all()
        print(users)

async def main():
    await g()

if __name__ == "__main__":
    asyncio.run(main())




from sqlalchemy import func

async def sort_forms_by_date(formatted_date) -> None: 
    async with session() as conn:
        stmt = select(UserForms).filter(
            func.DATE(UserForms.created_at) == formatted_date.date()
        )
        res = await conn.execute(stmt)
        forms = res.scalars().all()
        return forms
