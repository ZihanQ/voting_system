from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, make_response, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token
from app.models import db, User, Poll

# 创建蓝图
user_bp = Blueprint('user', __name__)

# 首页路由
@user_bp.route('/')
def home():
    return render_template('index.html')

# 注册路由
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    # 处理表单或 JSON 数据
    if request.is_json:
        data = request.json  # JSON 格式提交
    else:
        data = request.form  # 表单格式提交

    # 获取用户数据
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # 检查用户名或邮箱是否已存在
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "Username or email already exists."}), 400

    # 创建新用户
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    # return jsonify({"message": "Registration successful!", "redirect": '/login'}), 201
    return redirect(url_for('user.login'))

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # 清理过期提示cookie
        response = make_response(render_template('login.html'))
        response.set_cookie('auto_show_expired_alert', '', max_age=0)
        return response


    # 统一处理表单提交
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    # 验证失败处理
    if not user or not check_password_hash(user.password_hash, password):
        flash("用户名或密码错误", "error")  # 添加中文错误提示
        return redirect(url_for('user.login'))  # 重定向回登录页

    # access_token = create_access_token(identity=user.id)
    access_token = create_access_token(identity=str(user.id))

    response = make_response(redirect(url_for('user.dashboard')))
    response.set_cookie('auto_show_expired_alert', '', max_age=0)  # 新增清理提示cookie
    response.set_cookie(
        'access_token_cookie',  # 默认名称
    access_token,
    httponly=True,          # 防止前端脚本访问
    secure=False,           # 确保开发环境中为 False，生产环境中为 True
    samesite='Lax',         # 设置为 'Lax' 或 'Strict' 以控制跨站点行为
    max_age=3600            # 设置 Cookie 过期时间
    )
    return response

# 获取用户资料
@user_bp.route('/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404
    return render_template('profile.html',user=user)

# 更新用户资料
@user_bp.route('/user/profile', methods=['PUT','POST'])
@jwt_required(locations=["cookies"])  # 指定从 cookies 中获取令牌
def update_profile():
    user_id = get_jwt_identity()
    if request.is_json:
        data = request.json
    else:
        data = request.form

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    # 更新用户信息
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.avatar_url = data.get('avatar_url', user.avatar_url)
    db.session.commit()
    return jsonify({"message": "Profile updated successfully!"})

@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()  # 指定从 cookies 中获取令牌
def dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found."}), 404
    polls = Poll.query.filter_by(creator_id=user_id).all()
    poll_data = [{
        "id": poll.id,
        "title": poll.title,
        "start_time": poll.start_time,
        "end_time": poll.end_time,
        "is_active": poll.is_active
    } for poll in polls]

    return render_template(
        'dashboard.html',
        username=user.username,
        email=user.email,
        polls=poll_data
    )


@user_bp.route('/logout', methods=['GET', 'POST'])  # 同时支持两种方法
def logout():
    # 创建响应对象（根据请求方法决定重定向路径）
    redirect_url = url_for('user.home') if request.method == 'GET' else url_for('user.home')
    response = make_response(redirect(redirect_url))

    # 清除Cookie（保持原有逻辑）
    response.set_cookie(
        'access_token_cookie',
        '',
        expires=0,
        httponly=True,
        secure=False,
        samesite='Lax',
        path='/'
    )

    # 添加清除其他可能存在的认证信息
    response.delete_cookie('refresh_token_cookie')  # 如果有refresh token

    return response