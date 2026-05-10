from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

migrate = Migrate()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)
talisman = Talisman()
api = Api()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*")
cors = CORS()
