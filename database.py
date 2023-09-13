#
# database.py
#

import logging
from tortoise import Tortoise, run_async

log = logging.getLogger(__name__)


async def init_db():
    # Initialize database and models
    await Tortoise.init(db_url="mysql://root:mysql123@127.0.0.1:3306/test", modules={'models': ['tortoise_models', 'aerich.models', "models.user"]})


async def generate_schema() -> None:
    log.info("Initializing Tortoise...")
    await init_db()

    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()

    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())