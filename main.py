import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
import sqlite3

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp

import logging

logging.basicConfig(level=logging.INFO)

def init_bd():
    conn = sqlite3.connect("school_data.db")
    cur = conn.cursor()
    cur.execute(
        """ 
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            grade TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()
    print("База данных создана и таблица students успешно добавлена.")


init_bd()


# Инициализация бота и диспетчера
API_TOKEN = TOKEN
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def name(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("В каком классе ты учишься?")
    await state.set_state(Form.grade)


@dp.message(Form.grade)
async def city(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    print(user_data)  # Для отладки
    print(user_data.get('name'), user_data.get('age'), user_data.get('grade'))

    conn = sqlite3.connect("school_data.db")
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''', (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()
    await message.answer(f"Вы написали:\nИмя: {user_data.get('name')}\nВозраст: {user_data.get('age')}\nКласс: {user_data.get('grade')}")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())