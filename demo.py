import re

# 包含报纸名称的字符串
text = """
'半岛都市报': get_bandao_paper,
'中国环境报': get_chinahuanjiang_paper,
'中国经济时报': get_chinajingji_paper,
'中国企业报': get_chinaqiye_paper,
'法制日报': get_fazhi_paper,
'甘肃经济日报': get_gansujingji_paper,
'广西法制报': get_guangxifazhi_paper,
'河南商报': get_henanshang_paper,
'华西都市报': get_huaxi_paper,
'开封日报': get_kaifeng_paper,
'辽沈晚报': get_liaoshen_lastpaper,
'洛阳日报': get_luoyang_paper,
'每日新报': get_meiri_paper,
'农业科技报': get_nongyekeji_paper,
'青岛晚报': get_qingdao_lastpaper,
'山东商报': get_shandongshang_paper,
'市场星报': get_shichangxing_paper,
'四川经济日报': get_sichuanjingji_paper,
'天门日报': get_tianmen_paper,
'潍坊晚报': get_weifang_lastpaper,
'新乡日报': get_xinxiang_paper,
'证券日报': get_zhengquan_paper,
'工商导报': get_gongshangdao_paper,
'北海日报': get_beihai_paper,
'楚雄日报': get_chuxiong_paper,
'河南法制报': get_henanfazhi_paper,
'消费日报': get_xiaofei_paper,
'重庆晨报': get_chongqingchen_paper,
'青海法制报': get_qinghaifazhi_paper,
'贵州法制报': get_guizhoufazhi_paper,
'科技金融时报': get_kejijinrong_paper,
'甘肃法制报': get_gansufazhi_paper,
'河南日报': get_henan_paper,
'贵州日报': get_guizhou_paper,
"""

# 使用正则表达式匹配所有中文报纸名称
chinese_papers = re.findall(r"'(.*?)'", text)
list1 = []
# 打印匹配到的中文报纸名称
for paper in chinese_papers:
    list1.append(paper)

print(list1)