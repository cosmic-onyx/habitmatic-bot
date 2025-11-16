from repositories.RedisRepository import RedisRepository


class RedisService:
    @staticmethod
    async def set_token(telegram_id, token):
        RedisRepository().set_data(telegram_id, token)

    @staticmethod
    async def get_token(telegram_id):
        token = RedisRepository().get_data(telegram_id)
        return token