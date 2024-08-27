from canquechanpinzhaohui import get_car_xinwen_data, get_xiaofei_xinwen_data, get_car_gg_data, get_xiaofei_gg_data
from api_chief import paper_queue_next, paper_queue_success, paper_queue_fail

methods = {
    'https://www.samrdprc.org.cn/qczh/gnzhqc/': get_car_xinwen_data,
    'https://www.samrdprc.org.cn/xfpzh/xfpgnzh': get_xiaofei_xinwen_data,
}

web_list = ['https://www.samrdprc.org.cn/qczh/gnzhqc/',
            'https://www.samrdprc.org.cn/xfpzh/xfpgnzh'
            ]
paper_queue = paper_queue_next(webpage_url_list=web_list)
queue_id = paper_queue['id']
webpage_id = paper_queue["webpage_id"]
webpage_url = paper_queue["webpage_url"]
try:
    methods[webpage_url](queue_id, webpage_id)
    data = {
        "id": queue_id,
        'description': f'数据获取成功',
    }
    paper_queue_success(data=data)
except Exception as e:
    print(e)
    data = {
        "id": queue_id,
        'description': f'程序异常:{e}',
    }
    paper_queue_fail(data=data)
