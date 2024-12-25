import jieba
# import jieba.analyse
# 待分词的字符串
text = "本院定于二〇二四年十二月二十六日14:30到18:00在第三法庭开庭审理(2024)渝民终413号原告重庆辉联埔程物业管理有限公司,重庆辉联埔程国际物流有限公司诉被告中铁建工集团有限公司案外人执行异议之诉一案"


#  进行分词
seg_list = jieba.cut(text)
words = list(seg_list)
print("分词结果：", "/ ".join(words))
