from sanic import Blueprint, response

from models.user import User

bp = Blueprint('user', url_prefix='/user')

@bp.route('/list')
async def list_all(request):
    users = await User.all()
    return response.json({"users": [str(user) for user in users]})


@bp.route('/users')
async def add_user(request):
    users = await User.all()
    return response.json({"users": [str(user) for user in users]})


@bp.route("/user/<pk:int>")
async def get_user(request, pk):
    user = await User.query(pk=pk)
    return response.json({"user": str(user)})