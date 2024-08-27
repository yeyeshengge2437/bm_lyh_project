from canquechanpinzhaohui import get_xinwen_data, get_gonggao_data
from api_chief import paper_queue_next, paper_queue_success, paper_queue_fail

web_list = ['https://www.samrdprc.org.cn/qczh/gnzhqc/']
paper_queue = paper_queue_next(webpage_url_list=web_list)
queue_id = paper_queue['id']
webpage_id = paper_queue["webpage_id"]
try:
    get_xinwen_data('canquechanpinzhaohui_car', queue_id, webpage_id, database="col")
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


