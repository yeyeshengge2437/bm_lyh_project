import pymongo
# 连接MongoDB数据库
client = pymongo.MongoClient('192.168.31.195', 27017)
# 连接数据库
db = client['ceshi']
# 连接集合
collection = db['ceshi']
# 插入数据
collection.insert_one({'name': '张三', 'age': 18, 'gender': '男'})
client.close()