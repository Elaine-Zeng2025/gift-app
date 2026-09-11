from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建数据库工具实例（先不绑定 app，稍后在 app.py 里绑）
db = SQLAlchemy()


class Person(db.Model):
    __tablename__ = "persons"   # 表名

    id = db.Column(db.Integer, primary_key=True)          # 主键，自动编号
    name = db.Column(db.String(100), nullable=False)      # 姓名，必填
    occupation = db.Column(db.String(100))                # 职业，可空
    preference_notes = db.Column(db.Text)                 # 喜好备注，长文本
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间，自动填