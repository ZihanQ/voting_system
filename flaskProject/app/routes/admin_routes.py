from datetime import datetime
from functools import wraps
from operator import or_

from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc

from app.models import db, User, Poll, Vote, PollOption

admin_bp = Blueprint('admin', __name__)


# 管理员权限检查装饰器
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or not current_user.is_admin:
            flash("Access denied", "danger")
            return redirect(url_for('user.login'))
        return fn(*args, **kwargs)

    return wrapper


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # 统计信息
    stats = {
        'total_users': User.query.count(),
        'total_polls': Poll.query.count(),
        'active_polls': Poll.query.filter_by(is_disabled=False).count(),
        'ongoing_polls': Poll.query.filter(Poll.end_time >= datetime.now()).count(),
        'total_votes': Vote.query.count()  # 新增总投票数
    }

    return render_template('admin_dashboard.html', stats=stats)


@admin_bp.route('/polls')
@admin_required
def manage_polls():
    polls = Poll.query.order_by(Poll.start_time.desc()).all()
    return render_template('admin_polls.html',
                         polls=polls,
                         now=datetime.utcnow())  # 添加当前时间

@admin_bp.route('/users')
@admin_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    query = User.query
    if search:
        query = query.filter(or_(
            User.username.ilike(f'%{search}%'),
            User.email.ilike(f'%{search}%')
        ))

    users = query.order_by(desc(User.id)).paginate(page=page, per_page=10)
    return render_template('admin_users.html', users=users, search=search)


@admin_bp.route('/votes')
@admin_required
def manage_votes():
    page = request.args.get('page', 1, type=int)
    poll_id = request.args.get('poll_id')

    query = Vote.query.options(
        db.joinedload(Vote.user),
        db.joinedload(Vote.poll),
        db.joinedload(Vote.option)
    )

    if poll_id:
        query = query.filter(Vote.poll_id == poll_id)

    votes = query.order_by(desc(Vote.vote_time)).paginate(page=page, per_page=15)
    polls = Poll.query.with_entities(Poll.id, Poll.title).all()

    return render_template('admin_votes.html',
                           votes=votes,
                           polls=polls,
                           current_poll=poll_id)

@admin_bp.route('/toggle_user/<int:user_id>')
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f"User {user.username} admin status updated", "success")
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/toggle_poll/<int:poll_id>')
@admin_required
def toggle_poll(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    poll.is_disabled = not poll.is_disabled
    db.session.commit()
    flash(f"投票「{poll.title}」已{'禁用' if poll.is_disabled else '启用'}", "success")
    return redirect(url_for('admin.manage_polls'))

