from sanic import Sanic
from sanic.response import json
from sanic_jwt import Initialize
from uvloop import Loop
from werkzeug.utils import ImportStringError, find_modules, import_string

from config import config
from views.request import Request
from sanic_session import AIORedisSessionInterface, Session
from tortoise.contrib.sanic import register_tortoise


async def retrieve_user():
    pass


async def store_refresh_token():
    pass


async def retrieve_refresh_token():
   pass


def register_blueprints(root: str, app: Sanic) -> None:
    for name in find_modules(root, recursive=True):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            if mod.bp.name == 'admin':
                Initialize(mod.bp, app=app, authenticate="",
                           retrieve_user=retrieve_user,
                           store_refresh_token=store_refresh_token,
                           retrieve_refresh_token=retrieve_refresh_token,
                           secret=config.JWT_SECRET,
                           expiration_delta=config.EXPIRATION_DELTA)
            app.blueprint(mod.bp)


# 根据需要重写 Sanic 类
class MainSanic(Sanic):
    # 例如可以自定义 url_for 方法
    def url_for(self, view_name: str, **kwargs) -> str:
        pass



app = MainSanic(__name__, request_class=Request)
register_blueprints('views', app)

session = Session()
client = None
redis = None


@app.listener('before_server_start')
async def setup_db(app: Sanic, loop: Loop) -> None:
    # 可以初始化数据库
    register_tortoise(
        app, db_url="mysql://root:root@localhost/test", modules={"models": ["models"]}, generate_schemas=True
    )
    # 可以初始化app
    pass


@app.listener('after_server_stop')
async def close_aiohttp_session(sanic_app, _loop) -> None:
    pass


@app.middleware('request')
async def setup_context(request: Request) -> None:
    pass


@app.middleware('response')
async def add_spent_time(request, response):
    pass


async def _sitemap(request):
    pass


@app.route('sitemap.xml')
async def sitemap(request):
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)