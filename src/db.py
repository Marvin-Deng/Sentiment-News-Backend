from dotenv import load_dotenv
import os
from tortoise import Tortoise

load_dotenv()

DB_CONFIG = {
    "connections": {
        "default": os.getenv('DATABASE_URL'),
    },
    "apps": {
        "models": {
            "models": ["models.article_model", "models.ticker_model"],
            "default_connection": "default",
        }
    }
}


async def init_db():
    await Tortoise.init(config=DB_CONFIG)
    await Tortoise.generate_schemas()
