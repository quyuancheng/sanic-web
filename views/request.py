from sanic.request import Request as _Request

import config
from models.user import User


class Request(_Request):
    user: User
    partials = config.partials
