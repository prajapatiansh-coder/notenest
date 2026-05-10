from flask_login import login_user, logout_user
from ..extensions import db
from ..models.user import User
import structlog

logger = structlog.get_logger()

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        if User.query.filter_by(username=username).first():
            return None, "Username already exists"
        if User.query.filter_by(email=email).first():
            return None, "Email already exists"
            
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        logger.info("user_registered", username=username, email=email)
        return user, None

    @staticmethod
    def login_user(email, password, remember=False):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            logger.info("user_logged_in", user_id=user.id, email=email)
            return True
        return False

    @staticmethod
    def logout_user():
        logout_user()
