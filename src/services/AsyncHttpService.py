import aiohttp
from aiogram.types import User

from settings.config import env_settings
from services.generators import password_generator
from services.RedisService import RedisService


class AsyncHttpService:
    @staticmethod
    async def get_jwt_token(telegram_id, password):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{env_settings.EXTERNAL_API_URL}/api/v1/auth/token/",
                data={
                    "telegram_id": telegram_id,
                    "password": password
                }
            ) as response:
                data = await response.json()

                return data

    @staticmethod
    async def create_user(user: User):
        pwd = password_generator()

        data = {
            "telegram_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": pwd
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{env_settings.EXTERNAL_API_URL}/api/v1/users/",
                    data=data
                ) as response:
                    if response.status == 201:
                        return pwd

                    return response.status

        except Exception as err:
            return err

    @staticmethod
    async def get_user(telegram_id):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{env_settings.EXTERNAL_API_URL}/api/v1/users/?telegram_id={telegram_id}",
                ) as response:
                    data = await response.json()
                    user = data.get('results')
                    return user
        except Exception as err:
            print(err)
            return None

    @staticmethod
    async def create_habit(habit: dict, telegram_id):
        token = await RedisService.get_token(telegram_id)

        data = {
            "title": habit['title'],
            "repeat": habit['periodic'],
            "execution_time": habit['time']
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{env_settings.EXTERNAL_API_URL}/api/v1/habits/",
                    data=data,
                    headers={
                        'Authorization': f'Bearer {token['access']}'
                    }
                ) as response:
                    if response.status == 201:
                        return True
        except Exception as err:
            return err

    @staticmethod
    async def get_list_habits(telegram_id):
        token = await RedisService.get_token(telegram_id)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{env_settings.EXTERNAL_API_URL}/api/v1/habits/",
                    headers={
                        'Authorization': f'Bearer {token['access']}'
                    }
                ) as response:
                    if response.status == 200:
                        dats = await response.json()
                        return dats.get('results')
        except Exception as err:
            return err

    @staticmethod
    async def create_habit_log(telegram_id, habit_id, status):
        token = await RedisService.get_token(telegram_id)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{env_settings.EXTERNAL_API_URL}/api/v1/habits/{habit_id}/logs/",
                    data={"is_done": status},
                    headers={
                        'Authorization': f'Bearer {token['access']}'
                    }
                ) as response:
                    if response.status == 201:
                        return True
        except Exception as err:
            print(err)
            return False

    @staticmethod
    async def get_list_habit_log(telegram_id, habit_id):
        token = await RedisService.get_token(telegram_id)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"{env_settings.EXTERNAL_API_URL}/api/v1/habits/{habit_id}/logs/",
                        headers={
                            'Authorization': f'Bearer {token['access']}'
                        }
                ) as response:
                    if response.status == 200:
                        dats = await response.json()
                        return dats.get('results')
        except Exception as err:
            return err