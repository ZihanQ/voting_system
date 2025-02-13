from datetime import datetime

from app import db

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)

class Poll(db.Model):
    __tablename__ = 'Polls'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    creator_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    is_disabled = db.Column(db.Boolean, default=False)  # 新增禁用状态

    def calculate_results(self):
        options = PollOption.query.filter_by(poll_id=self.id).all()
        total_votes = Vote.query.filter_by(poll_id=self.id).count()

        results = []
        for option in options:
            vote_count = Vote.query.filter_by(option_id=option.id).count()
            percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
            results.append({
                "option_text": option.option_text,
                "vote_count": vote_count,
                "percentage": percentage
            })

        return {
            "total_votes": total_votes,
            "options": results
        }

class PollOption(db.Model):
    __tablename__ = 'PollOptions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('Polls.id'), nullable=False)
    option_text = db.Column(db.String(255), nullable=False)

class Vote(db.Model):
    __tablename__ = 'Votes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('Polls.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('PollOptions.id'), nullable=False)
    vote_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # 新增关系定义
    user = db.relationship('User', backref='votes')
    poll = db.relationship('Poll', backref='votes')
    option = db.relationship('PollOption', backref='votes')
