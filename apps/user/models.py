from store.gino import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    chat_id = db.Column(db.Integer(), nullable=False, primary_key=True)
    username = db.Column(db.String(32), nullable=False, primary_key=True)
    state = db.Column(db.String(32), nullable=False)
    tags = db.Column(db.String(32), nullable=True)
    timer = db.Column(db.String(32), nullable=True)


class SendedNews(db.Model):
    __tablename__ = "sended_news"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    link = db.Column(db.Text(), nullable=False)
    chat_id = db.Column(db.Integer(), nullable=False)
    tag = db.Column(db.Text(), nullable=False)
