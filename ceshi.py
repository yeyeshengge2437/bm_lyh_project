import re

# 正则表达式模式
explicit_claims = re.compile(r'.*(?:债权|转让|受让|处置|招商|营销|信息|联合|催收|催讨).*的.*'
                             r'(?:通知书|告知书|通知公告|登报公告|补登公告|补充公告|拍卖公告|公告|通知)$')

# 关键词列表
keywords = ['债权', '转让', '受让', '处置', '招商', '营销', '信息', '联合', '催收', '催讨']

# 结尾词汇列表
endings = ['通知书', '告知书', '通知公告', '登报公告', '补登公告', '补充公告', '拍卖公告', '公告', '通知']

# 生成所有关键词和结束词汇的组合
all_combinations = []
for keyword in keywords:
    for ending in endings:
        # 创建一个简单的测试字符串
        test_string = f"{keyword}的测试内容{ending}"
        # 检查是否匹配
        if explicit_claims.match(test_string):
            all_combinations.append(test_string)

# 打印所有匹配的组合
for combo in all_combinations:
    print(combo)

