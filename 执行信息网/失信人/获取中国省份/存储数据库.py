import pymongo

# 连接数据库
client = pymongo.MongoClient()
db = client['sxr_data']
search_key = db['search_key']
# # 数据库清空
# search_key.delete_many({})
# provinces = [
#     '黑龙江', '吉林', '辽宁', '河北', '山西', '陕西', '甘肃', '四川',
#     '贵州', '云南', '浙江', '江苏', '安徽', '山东', '河南', '湖北',
#     '湖南', '江西', '福建', '台湾', '广东', '海南', '广西', '内蒙古',
#     '新疆', '西藏', '宁夏', '青海', '北京', '天津', '上海', '重庆',
#     '香港', '澳门'
# ]
# for province in provinces:
#     search_key.insert_one({'province': province})
#
# print('存储完成')
# key = search_key.find_one_and_delete({}, {"_id": 0})
# print(key)
key = search_key.find_one({}, {"_id": 0})
print(key)
