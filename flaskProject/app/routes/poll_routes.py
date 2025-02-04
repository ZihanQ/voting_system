from flask import Blueprint, request, jsonify, render_template, redirect, flash, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Poll, PollOption, Vote, User
from datetime import datetime

poll_bp = Blueprint('poll', __name__)

# 创建投票
@poll_bp.route('/', methods=['POST'])
@jwt_required()
def create_poll():
    try:
        user_id = get_jwt_identity()
        if user_id is None:
            flash("You need to be logged in.", "error")
            return redirect(url_for('auth.login'))  # 确保有登录处理

        title = request.form.get('title')
        description = request.form.get('description')
        options = request.form.get('options')
        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time')
        is_anonymous = request.form.get('is_anonymous') == 'on'
        # 验证输入
        if not title or not options:
            flash("Title and options are required.", "error")
            return redirect(url_for('poll.create_poll_page'))

        option_list = [option.strip() for option in options.split(',') if option.strip()]
        if len(option_list) < 2:
            flash("At least two options are required.", "error")
            return redirect(url_for('poll.create_poll_page'))

        # 转换时间格式
        try:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)
        except (ValueError, TypeError):
            flash("Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS).", "error")
            return redirect(url_for('poll.create_poll_page'))

        # 创建投票
        new_poll = Poll(
            title=title,
            description=description,
            creator_id=user_id,
            start_time=start_time,
            end_time=end_time,
            is_anonymous = is_anonymous
        )
        db.session.add(new_poll)
        db.session.commit()

        # 创建投票选项
        for option_text in option_list:
            new_option = PollOption(poll_id=new_poll.id, option_text=option_text)
            db.session.add(new_option)

        db.session.commit()

        flash("Poll created successfully!", "success")
        return redirect(url_for('poll.get_polls'))

    except Exception as e:
        # 处理所有未捕获的异常
        db.session.rollback()  # 如果有事务未提交，回滚数据库
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('poll.create_poll_page'))


@poll_bp.route('/create', methods=['GET'])
def create_poll_page():
    return render_template('create_poll.html')


# 获取所有投票
@poll_bp.route('/', methods=['GET'])
def get_polls():
    # 获取筛选和排序参数
    sort_by = request.args.get('sort', 'start_time')
    order = request.args.get('order', 'desc')
    status_filter = request.args.get('status', 'all')

    query = Poll.query

    # 应用状态筛选
    now = datetime.now()
    if status_filter == 'ongoing':
        query = query.filter(Poll.start_time <= now, Poll.end_time >= now)
    elif status_filter == 'ended':
        query = query.filter(Poll.end_time < now)

    # 应用排序
    if sort_by in ['start_time', 'end_time']:
        order_column = getattr(Poll, sort_by)
        if order == 'asc':
            query = query.order_by(order_column.asc())
        else:
            query = query.order_by(order_column.desc())

    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    polls = query.paginate(page=page, per_page=size, error_out=False)

    # 获取当前时间
    now = datetime.now()

    result = [{
        "id": poll.id,
        "title": poll.title,
        "description": poll.description,
        "creator": User.query.get(poll.creator_id).username if poll.creator_id else "Unknown",
        "start_time": poll.start_time,
        "end_time": poll.end_time
    } for poll in polls.items]

    return render_template('poll_list.html', polls=result, now=now,
                           current_sort=sort_by, current_order=order,
                           current_status=status_filter)
# 获取投票详情
@poll_bp.route('/<int:poll_id>', methods=['GET'])
def get_poll_details(poll_id):
    poll = Poll.query.get(poll_id)
    if not poll:
        return jsonify({"message": "Poll not found."}), 404

    options = PollOption.query.filter_by(poll_id=poll.id).all()
    result = {
        "id": poll.id,
        "title": poll.title,
        "description": poll.description,
        "start_time": poll.start_time,
        "end_time": poll.end_time,
        "options": [{"id": option.id, "text": option.option_text} for option in options]
    }

    return render_template('poll_detail.html', poll=poll, result=result,now=datetime.now())


# 投票
@poll_bp.route('/<int:poll_id>/vote', methods=['POST'])
@jwt_required()
def vote_on_poll(poll_id):
    user_id = get_jwt_identity()
    poll = Poll.query.get(poll_id)
    if not poll:
        flash("Poll not found.", "error")
        return redirect(url_for('poll.get_polls'))

    selected_option = request.form.get('selected_option')
    print(f"Selected option type: {type(selected_option)}, value: {selected_option}")
    # 空值检查
    if not selected_option:
        flash("Please select a valid option.", "error")
        return redirect(url_for('poll.get_poll_details', poll_id=poll_id))

    # 类型转换检查
    try:
        option_id = int(selected_option)
    except ValueError:
        flash("Invalid option selected.", "error")
        return redirect(url_for('poll.get_poll_details', poll_id=poll_id))

    # 选项有效性验证
    option = PollOption.query.get(option_id)
    if not option or option.poll_id != poll_id:
        flash("Invalid poll option.", "error")
        return redirect(url_for('poll.get_poll_details', poll_id=poll_id))
    # 检查用户是否已经投票
    existing_vote = Vote.query.filter_by(user_id=user_id, poll_id=poll_id).first()
    if existing_vote:
        flash("You have already voted on this poll.", "error")
        return redirect(url_for('poll.get_poll_details', poll_id=poll_id))

        # 投票保存逻辑
    new_vote = Vote(
        user_id=user_id,
        poll_id=poll_id,
        option_id=option.id
    )
    db.session.add(new_vote)
    db.session.commit()
    # 修改重复投票检查逻辑
    if not poll.is_anonymous:
        existing_vote = Vote.query.filter_by(user_id=user_id, poll_id=poll_id).first()
        if existing_vote:
            flash("You have already voted on this poll.", "error")
    flash("Vote submitted successfully!", "success")
    return redirect(url_for('poll.get_poll_details', poll_id=poll_id))


# 获取投票结果
@poll_bp.route('/<int:poll_id>/results', methods=['GET'])
@jwt_required(optional=True)
def poll_results(poll_id):
    poll = Poll.query.get_or_404(poll_id)

    # 获取当前用户
    current_user = None
    try:
        user_id = get_jwt_identity()
        if user_id:
            current_user = User.query.get(user_id)
    except RuntimeError:
        pass

    # 权限检查
    if not current_user:
        flash("Please login to view detailed results", "info")
        return redirect(url_for('user.login'))

    if not current_user.is_admin:
        has_voted = Vote.query.filter_by(
            user_id=current_user.id,
            poll_id=poll_id
        ).first() is not None

        if not has_voted:
            flash("You can only view polls you've participated in", "danger")
            return redirect(url_for('poll.get_polls'))

    # 结果计算
    options = PollOption.query.filter_by(poll_id=poll.id).all()
    total_votes = Vote.query.filter_by(poll_id=poll_id).count()

    results = []
    for option in options:
        vote_count = Vote.query.filter_by(option_id=option.id).count()
        results.append({
            "option_text": option.option_text,
            "vote_count": vote_count,
            "percentage": (vote_count / total_votes * 100) if total_votes > 0 else 0
        })

    return render_template(
        'poll_results.html',
        poll=poll,
        results=results,
        total_votes=total_votes,
        current_user=current_user
    )


@poll_bp.route('/my_votes')
@jwt_required()
def my_votes():
    user_id = get_jwt_identity()
    votes = Vote.query.filter_by(user_id=user_id).all()
    polls = []
    for vote in votes:
        poll = Poll.query.get(vote.poll_id)
        if poll:
            polls.append({
                "poll": poll,
                "voted_option": PollOption.query.get(vote.option_id).option_text
            })
    return render_template('user_votes.html', polls=polls)
