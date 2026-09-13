from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ---------- 中间表（多对多）----------
# 中间表不需要定义成类，用这种简洁写法即可

person_tags = db.Table(
    "person_tags",
    db.Column("person_id", db.Integer, db.ForeignKey("persons.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)

holiday_persons = db.Table(
    "holiday_persons",
    db.Column("holiday_id", db.Integer, db.ForeignKey("holidays.id"), primary_key=True),
    db.Column("person_id", db.Integer, db.ForeignKey("persons.id"), primary_key=True),
)

gift_idea_tags = db.Table(
    "gift_idea_tags",
    db.Column("gift_idea_id", db.Integer, db.ForeignKey("gift_ideas.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


# ---------- 主表 ----------

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)         # 登录标识，不重复
    password_hash = db.Column(db.String(255))              # 加密后的密码，绝不存明文
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Person(db.Model):
    __tablename__ = "persons"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # 预留：属于哪个用户
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100))
    preference_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系（方便从一个对象直接拿到相关数据）
    gift_records = db.relationship("GiftRecord", backref="person", cascade="all, delete-orphan")
    special_dates = db.relationship("SpecialDate", backref="person", cascade="all, delete-orphan")
    tags = db.relationship("Tag", secondary=person_tags, backref="persons")


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50))    # relationship / hobby / style / occupation
    select_type = db.Column(db.String(20)) # single / multi


class GiftRecord(db.Model):
    __tablename__ = "gift_records"

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"), nullable=False)  # 外键
    direction = db.Column(db.String(20), nullable=False)   # given / received
    gift_name = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float)                            # 可空，选填
    reason = db.Column(db.String(50))                       # holiday / birthday / meetup
    feedback = db.Column(db.String(20))                     # liked / neutral / disliked
    image_url = db.Column(db.String(500))
    note = db.Column(db.Text)
    date = db.Column(db.Date)


class SpecialDate(db.Model):
    __tablename__ = "special_dates"

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"), nullable=False)  # 外键
    type = db.Column(db.String(20))        # birthday / anniversary / custom
    date = db.Column(db.Date)
    remind = db.Column(db.Boolean, default=True)
    days_before = db.Column(db.Integer, default=10)


class Holiday(db.Model):
    __tablename__ = "holidays"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # 仅自定义节日需要
    name = db.Column(db.String(100))       # 双语名称
    region = db.Column(db.String(20))      # China / Canada
    date = db.Column(db.Date)              # 公历（农历以后再处理）
    enabled = db.Column(db.Boolean, default=True)
    is_custom = db.Column(db.Boolean, default=False)

    persons = db.relationship("Person", secondary=holiday_persons, backref="holidays")


class GiftIdea(db.Model):
    __tablename__ = "gift_ideas"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(100))
    image_url = db.Column(db.String(500))

    tags = db.relationship("Tag", secondary=gift_idea_tags, backref="gift_ideas")