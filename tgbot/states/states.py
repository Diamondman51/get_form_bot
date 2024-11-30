from aiogram.fsm.state import StatesGroup, State


class GetPhone(StatesGroup):
    phone = State()


class GetForm(StatesGroup):
    name = State()
    longitude = State()
    latitude = State()
    price = State()


class GetDate(StatesGroup):
    date = State()
