from tortoise import Tortoise

from config.env import DATABASE_URL

DB_CONFIG = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["models.article", "models.ticker"],
            "default_connection": "default",
        }
    },
}


async def init_db():
    await Tortoise.init(config=DB_CONFIG)
    await Tortoise.generate_schemas()
