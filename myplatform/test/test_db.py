from backend import db


def test_create_table():
    # 删除表
    db.drop_all()
    # 创建表
    # db.create_all()