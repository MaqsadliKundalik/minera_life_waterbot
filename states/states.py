from aiogram.dispatcher.filters.state import StatesGroup, State

class log_in_admin_state(StatesGroup):
    login = State()
    parol = State()

class add_location_state(StatesGroup):
    id = State()
    name = State()
    phone = State()
    about = State()
    location = State()
    confirm = State()

class del_location_state(StatesGroup):
    id = State()
