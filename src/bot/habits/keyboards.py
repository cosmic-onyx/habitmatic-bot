from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


async def get_create_habit_kb():
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(
            text="Изменить название",
            callback_data="change_title"
        )
    )

    kb.row(
        InlineKeyboardButton(
            text="Переодичность",
            callback_data="choice_periodic"
        ),
        InlineKeyboardButton(
            text="Время напоминания",
            callback_data="choice_time"
        )
    )

    kb.row(
        InlineKeyboardButton(
            text="Создать",
            callback_data="create_habit"
        )
    )

    return kb


async def get_choice_periodic_kb():
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(
            text="каждый день",
            callback_data="periodic:каждый день"
        ),
        InlineKeyboardButton(
            text="по будням",
            callback_data="periodic:по будням"
        ),
        InlineKeyboardButton(
            text="по выходным",
            callback_data="periodic:по выходным"
        )
    )

    return kb


async def get_list_habits_kb(habits, prefix=None):
    split = 2

    kb = InlineKeyboardBuilder()
    btn_in_row = []
    for habit in habits:
        habit_id = habit['id']
        habit_title = habit['title']

        btn_in_row.append(
            InlineKeyboardButton(
                text=f"{habit_title}",
                callback_data=f"id{'_'+prefix if prefix else ''}:{habit_id}"
            )
        )
        if len(btn_in_row) >= split:
            kb.row(*btn_in_row)
            btn_in_row = []

    else:
        if btn_in_row:
            kb.row(*btn_in_row)

    return kb


async def get_is_done_kb():
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(
            text="Cделано",
            callback_data="is_done:сделано"
        ),
        InlineKeyboardButton(
            text="Не сделано",
            callback_data="is_done:не сделано"
        )
    )

    return kb