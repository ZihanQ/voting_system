from flask import Blueprint, render_template

# 创建蓝图
user1_bp = Blueprint('user1', __name__)

# 首页路由
@user1_bp.route('/')
def home():
    return render_template('index.html')