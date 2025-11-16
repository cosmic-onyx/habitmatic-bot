from aiogram.fsm.state import State, StatesGroup


class HabitState(StatesGroup):
    habit_title = State()
    habit_time = State()