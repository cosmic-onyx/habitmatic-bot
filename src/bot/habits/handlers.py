from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from bot.habits.states import *
from bot.habits.keyboards import *
from services.AsyncHttpService import AsyncHttpService
from utils.plurals import *


habit_router = Router()


@habit_router.message(F.text == 'Создать привычку')
async def start_create_habit(message: Message, state: FSMContext):
    text = "Введите название привычки"
    await state.set_state(HabitState.habit_title)
    await message.answer(text)


@habit_router.message(F.text == "Мои привычки")
async def get_list_habits(message: Message):
    habits = await AsyncHttpService.get_list_habits(message.chat.id)
    if isinstance(habits, list):
        text = ""
        for i, habit in enumerate(habits, 1):
            text += f"{i}. Название: {habit['title']}\n    Периодичность: {habit['repeat']}\n    Время напоминания: {habit['execution_time'][:-3]}\n\n"

        if text:
            await message.answer(text.strip())
        else:
            await message.answer("У вас нет ни одной привычки. Создайте!")
    else:
        await message.answer(f"❌ Произошла неизвестная ошибка")


@habit_router.message(F.text == "Выполнить привычку")
async def choice_habit(message: Message):
    habits = await AsyncHttpService.get_list_habits(message.chat.id)
    kb = await get_list_habits_kb(habits)
    await message.answer(
        "Выберите привычку, которую хотите выполнить",
        reply_markup=kb.as_markup()
    )


@habit_router.message(F.text == "Статистика")
async def choice_habit(message: Message):
    habits = await AsyncHttpService.get_list_habits(message.chat.id)
    kb = await get_list_habits_kb(habits, prefix='stat')
    await message.answer(
        "Выберите привычку, у которой хотите увидеть статистику",
        reply_markup=kb.as_markup()
    )


async def manage_habit(message: Message | CallbackQuery, state: FSMContext):
    data = await state.get_data()

    title = data.get('title')
    time = data.get('time')
    periodic = data.get('periodic')

    text = ""
    if title:
        text += f"Название привычки: {title}"
    if time:
        text += f"\n\nВремя напоминания {time}"
    if periodic:
        text += f"\n\nПереодичность: {periodic}"

    kb = await get_create_habit_kb()

    if isinstance(message, CallbackQuery):
        await message.message.edit_text(
            text,
            reply_markup=kb.as_markup()
        )
    else:
        await message.answer(
            text,
            reply_markup=kb.as_markup()
        )


@habit_router.message(HabitState.habit_title)
async def get_title(message: Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)
    await manage_habit(message, state)


@habit_router.callback_query(lambda cq: cq.data == 'change_title')
async def change_title(callback_query: CallbackQuery, state: FSMContext):
    text = "Введите название привычки"
    await state.set_state(HabitState.habit_title)
    await callback_query.message.edit_text(text)


@habit_router.callback_query(lambda cq: cq.data == 'choice_periodic')
async def choice_periodic(callback_query: CallbackQuery):
    text = "Выберите переодичность напоминания"
    kb = await get_choice_periodic_kb()
    await callback_query.message.edit_text(
        text=text,
        reply_markup=kb.as_markup()
    )


@habit_router.callback_query(lambda cq: "periodic:" in cq.data)
async def get_periodic(callback_query: CallbackQuery, state: FSMContext):
    periodic = callback_query.data.split(":")[-1]
    await state.update_data(periodic=periodic)
    await manage_habit(callback_query, state)


@habit_router.callback_query(lambda cq: cq.data == 'choice_time')
async def choice_time(callback_query: CallbackQuery, state: FSMContext):
    text = "Введите время напоминания\n\nПоддерживающие форматы: <blockquote>20:30\n20 30</blockquote>"
    await state.set_state(HabitState.habit_time)
    await callback_query.message.edit_text(
        text=text,
        parse_mode="HTML"
    )


@habit_router.message(HabitState.habit_time)
async def get_time(message: Message, state: FSMContext):
    time = message.text
    if not (':' in time):
        time = ':'.join(time.split(' '))

    await state.update_data(time=time)
    await manage_habit(message, state)


@habit_router.callback_query(lambda cq: cq.data == 'create_habit')
async def final_create_habit(callback_query: CallbackQuery, state: FSMContext):
    habit = await state.get_data()
    is_created = await AsyncHttpService.create_habit(habit, callback_query.message.chat.id)
    await state.clear()
    if is_created is True:
        await callback_query.message.edit_text("✅ Привычка была успешно создана")
    else:
        await callback_query.message.edit_text(f"❌ Произошла неизвестная ошибка")


@habit_router.callback_query(lambda cq: 'id:' in cq.data)
async def get_habit(callback_query: CallbackQuery, state: FSMContext):
    habit_id = callback_query.data.split(":")[-1]
    await state.update_data(habit_id=habit_id)

    kb = await get_is_done_kb()

    await callback_query.message.edit_text(
        "Выберите статус выполнения привычки за этот день",
        reply_markup=kb.as_markup()
    )


@habit_router.callback_query(lambda cq: 'is_done:' in cq.data)
async def create_log_habit(callback_query: CallbackQuery, state: FSMContext):
    is_done = callback_query.data.split(':')[-1]
    data = await state.get_data()
    habit_id = data.get('habit_id')

    await state.clear()

    is_created = await AsyncHttpService().create_habit_log(
        callback_query.message.chat.id,
        habit_id,
        is_done
    )
    if is_created:
        await callback_query.message.edit_text(
            f"✅ Привычка успешно получила статус: {is_done}"
        )
    else:
        await callback_query.message.edit_text(
            "❌ Произошла неизвестная ошибка"
        )


@habit_router.callback_query(lambda cq: 'id_stat:' in cq.data)
async def get_stat_habit(callback_query: CallbackQuery):
    habit_id = callback_query.data.split(":")[-1]

    habit_log = await AsyncHttpService().get_list_habit_log(
        callback_query.message.chat.id,
        habit_id
    )
    if habit_log:
        habit = habit_log[0]['habit']
        created_at = datetime.strptime(
            habit['created_at'],
            "%Y-%m-%d %H:%M:%S"
        )
        now_dt = datetime.now()

        delta = now_dt - created_at
        stat_text = f"""Привычка: {habit['title']}

За {plural_day(delta.days) if delta.days > 0 else "этот день"}, привычка была выполнена {plural_count(len(habit_log))}
"""
        await callback_query.message.edit_text(stat_text)
    else:
        await callback_query.message.edit_text(
            "Вы ни разу не выполняли эту привычку"
        )