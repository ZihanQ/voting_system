from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, redirect, flash, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Poll, Vote

admin_bp = Blueprint('admin', __name__)


# 管理员权限检查装饰器
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or not current_user.is_admin:
            flash("Access denied", "danger")
            return redirect(url_for('auth.login'))
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
        'ongoing_polls': Poll.query.filter(Poll.end_time >= datetime.now()).count()
    }

    return render_template('admin_dashboard.html', stats=stats)


@admin_bp.route('/polls')
@admin_required
def manage_polls():
    polls = Poll.query.order_by(Poll.created_at.desc()).all()
    return render_template('admin_polls.html', polls=polls)


@admin_bp.route('/toggle_poll/<int:poll_id>')
@admin_required
def toggle_poll(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    poll.is_disabled = not poll.is_disabled
    db.session.commit()
    flash(f"Poll {'disabled' if poll.is_disabled else 'enabled'} successfully", "success")
    return redirect(url_for('admin.manage_polls'))


@admin_bp.route('/users')
@admin_required
def manage_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)


@admin_bp.route('/votes')
@admin_required
def view_votes():
    votes = Vote.query.options(db.joinedload(Vote.user), db.joinedload(Vote.poll)).all()
    return render_template('admin_votes.html', votes=votes)