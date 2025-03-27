import time

from jingdongsifapaimai import by_keyword_search, get_detail_info
from api_paimai import sub_queues_next, paper_queue_next, sub_queues_fail, paper_queue_fail, paper_queue_success

webpage_url_list = [
    'https://auction.jd.com/sifa.html'
]

value = paper_queue_next(webpage_url_list)
if value:
    id_value = value['id']
    webpage_id_value = value['webpage_id']
    search_keyword = value['name']
    webpage_url_value = value['webpage_url']
    print(id_value, webpage_id_value, search_keyword, webpage_url_value)
    sub_queue_data_list = by_keyword_search(id_value, webpage_id_value, webpage_url_value, search_keyword)
    if sub_queue_data_list:
        success_data = {
            'id': id_value,
            'data_list': sub_queue_data_list
        }
    else:
        success_data = {
            'id': id_value,
        }
    print(success_data)
    paper_queue_success(success_data)

while True:
    sub_value = sub_queues_next(webpage_url_list)
    if sub_value:
        sub_id_value = sub_value['id']
        name_value = sub_value['name']
        sub_web_queue_id_value = sub_value['web_queue_id']
        print(sub_id_value, name_value, sub_web_queue_id_value)
        get_detail_info(sub_id_value, name_value, sub_web_queue_id_value)
    else:
        time.sleep(3)
        break

