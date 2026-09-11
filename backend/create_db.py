from app import app
from models import db

with app.app_context():   # 进入 app 的"工作上下文"，操作数据库需要它
    db.create_all()       # 按 models.py 里定义的所有模型，创建对应的表
    print("数据库表已创建！")