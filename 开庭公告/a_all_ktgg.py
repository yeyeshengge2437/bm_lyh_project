import time

from heilongjiang_ktgg import get_lhjcourt_info
from chongqing_ktgg import get_cqcourt_info
from zhejiang_ktgg import get_zjcourt_info
from shanxi_ktgg import get_sxcourt_1_info
from a_ktgg_api import queue_next, queue_success, queue_fail

methods = {
    'http://www.hljcourt.gov.cn/ktgg': get_lhjcourt_info,  # 黑龙江省高级人民法院
    'http://www.cqfygzfw.gov.cn/gggs/toListKtggNL.shtml?page=1': get_cqcourt_info,  # 重庆法院公众服务网
    'https://www.zjsfgkw.gov.cn/jkts/search/ktgglist.do': get_zjcourt_info,  # 浙江法院网
    'http://sxgaofa.cn/sxssfw/ktgg/toListKtggNL.shtml': get_sxcourt_1_info,  # 陕西法院诉讼服务网
}
web_list = [
    'http://www.hljcourt.gov.cn/ktgg',
    'http://www.cqfygzfw.gov.cn/gggs/toListKtggNL.shtml?page=1',
    'https://www.zjsfgkw.gov.cn/jkts/search/ktgglist.do',
    'http://sxgaofa.cn/sxssfw/ktgg/toListKtggNL.shtml'
]

while True:
    try:
        from_queue = queue_next(webpage_url_list=web_list)
        if from_queue is None or len(from_queue) == 0:
            time.sleep(30)
            continue
        else:
            queue_id = from_queue["id"]
            webpage_id = from_queue["webpage_id"]
            webpage_url = from_queue["webpage_url"]
            try:
                methods[webpage_url](queue_id, webpage_id)
                data = {
                    "id": queue_id,
                    'description': 'success',
                }
                queue_success(data=data)
            except Exception as e:
                data = {
                    "id": queue_id,
                    'description': str(e),
                }
                queue_fail(data=data)
    except Exception as e:
        time.sleep(90)
        print("解析过程中发生错误")
