from tortoise import Tortoise

from constants.env_consts import DATABASE_URL

DB_CONFIG = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["models.article_model", "models.ticker_model"],
            "default_connection": "default",
        }
    },
}


async def init_db():
    await Tortoise.init(config=DB_CONFIG)
    await Tortoise.generate_schemas()
