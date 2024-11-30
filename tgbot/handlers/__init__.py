from aiogram import F, Router
from aiogram.filters import CommandStart, Command

from handlers.commands import do_not_verify, get_all_forms, get_date, get_form, get_forms_by_date, get_location, get_name, get_phone, get_price, start_command_handler, verify
from states.states import GetDate, GetForm, GetPhone


def setup() -> Router:
    router = Router()

    router.message.register(start_command_handler, CommandStart())
    router.callback_query.register(verify, F.data == 'verify')
    router.callback_query.register(do_not_verify, F.data == 'pass')
    router.message.register(get_form, F.text == 'Отправить форму')
    router.message.register(get_phone, GetPhone.phone)
    router.message.register(get_name, GetForm.name)
    router.message.register(get_price, GetForm.price)
    router.message.register(get_location, GetForm.longitude)
    router.message.register(get_all_forms, F.text == "Получить все формы")
    router.message.register(get_all_forms, Command('all'))
    router.message.register(get_forms_by_date, F.text == "Получить формы по дате")
    router.message.register(get_forms_by_date, Command('by_date'))
    router.message.register(get_date, GetDate.date)
    return router
