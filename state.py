from aiogram.fsm.state import StatesGroup,State

class order(StatesGroup):
    telefon = State()
    manzil = State()
    tasdiqlash = State()