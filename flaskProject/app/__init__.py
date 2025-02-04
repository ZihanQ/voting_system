import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, get_jwt_identity  # 新增导入


db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'as175050'  # 生产环境应使用更安全的随机字符串
    db_path = r"D:\sqlite3\db\base_record.db"

    # 配置 SQLAlchemy 数据库 URI
    app.config.update(
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path.replace('\\', '/')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY='as175050',
        JWT_TOKEN_LOCATION=['cookies'],
        JWT_COOKIE_SECURE=False,  # 开发环境为False，生产环境必须为True
        JWT_COOKIE_CSRF_PROTECT=False  # 根据安全需求调整
    )

    db.init_app(app)
    jwt.init_app(app)

    from app.models import User  # 新增模型导入

    # 注册蓝图
    from app.routes.user_routes import user_bp
    from app.routes.poll_routes import poll_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(user_bp, url_prefix='/')
    app.register_blueprint(poll_bp, url_prefix='/poll')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # 新增模板上下文处理器（关键修复）
    @app.context_processor
    def inject_user():
        try:
            user_id = get_jwt_identity()
            if user_id:
                current_user = User.query.get(user_id)
                return dict(current_user=current_user)
        except RuntimeError:  # JWT未加载时的处理
            pass
        return dict(current_user=None)

    # JWT错误处理（修复路由引用）
    @jwt.expired_token_loader
    def handle_expired_token(jwt_header, jwt_payload):
        response = redirect(url_for('user.login'))  # 原'auth.login'改为'user.login'
        response.set_cookie('auto_show_expired_alert', '1', max_age=2)
        return response

    @jwt.unauthorized_loader
    def handle_unauthorized(error):
        return redirect(url_for('user.login'))  # 修复路由名称

    @jwt.invalid_token_loader
    def handle_invalid_token(error):
        return redirect(url_for('user.login'))  # 修复路由名称

    return app