from 通过公司名称查公司基础信息_徐昂 import qcc_search_company_xuang
from 通过公司名称查公司基础信息_池悦 import qcc_search_company_chiyue
from 通过公司名称查公司基础信息_孙笑笑 import qcc_search_company_sunxiaoxiao
import random
import time
from lxml import etree
from api_qcc import qcc_parse_success, qcc_parse_fail, qcc_parse_next, qcc_upload_detail_info, qcc_upload_info_list
import datetime
import time
from threading import Thread, Event
count = 0


def collect_information(qcc_search_company):
    random_num = random.randint(3, 9)
    try:
        value = qcc_parse_next()
    except Exception as e:
        time.sleep(5)
        return None
    time.sleep(random_num)
    if value:
        try:
            id = value['value']['id']
        except:
            time.sleep(5)
            return None
        search_type = value["value"]["search_type"]
        if search_type == 'corp_qcc_list':  # 根据企业名称查询列表
            company_name = value.get('value')
            company_name = company_name.get('name')
            try:
                search_flag, search_value = qcc_search_company(company_name)
            except Exception as e:
                data = {
                    'id': id,
                    'description': f'{e}',
                }
                qcc_parse_fail(data)
                return None
            if search_flag == True:
                # print('_______________________________________')
                data = {'corp_info': search_value}
                qcc_upload_detail_info(data=data)
                success_data = {
                    'id': id
                }
                qcc_parse_success(success_data)
            elif search_flag == False:
                data = {'corp_summary_array': search_value}
                qcc_upload_info_list(data)
                success_data = {
                    'id': id
                }
                qcc_parse_success(success_data)
            elif search_flag == "失败":
                data = {
                    'id': id,
                    'description': '没有json数据',
                }
                qcc_parse_fail(data)
    else:
        time.sleep(8)
    print(count)


def is_time_to_run():
    """检查当前时间是否在晚上8点至次日5点之间"""
    current_time = datetime.datetime.now().time()
    return current_time >= datetime.time(20, 0) or current_time < datetime.time(5, 0)



def worker(param, stop_event):
    """工作线程函数"""
    try:
        while not stop_event.is_set() and is_time_to_run():
            collect_information(param)
            time.sleep(1)  # 每次任务间隔1秒
    except Exception as e:
        print(f"参数 {param} 的线程发生错误: {e}")


def main_loop():
    """主控制循环"""
    while True:
        # 等待直到进入工作时间段
        while not is_time_to_run():
            time.sleep(60)  # 每分钟检查一次

        # 创建停止事件
        stop_event = Event()

        # 创建并启动三个工作线程
        params = ["qcc_search_company_xuang", "qcc_search_company_chiyue", "qcc_search_company_sunxiaoxiao"]  # 替换为您的实际参数
        threads = [
            Thread(target=worker, args=(param, stop_event))
            for param in params
        ]

        for thread in threads:
            thread.start()

        # 持续监控时间直到超出工作时间段
        while is_time_to_run():
            time.sleep(60)  # 每分钟检查一次

        # 通知所有线程停止
        stop_event.set()

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        print("当日任务已全部停止，等待次日运行...")


if __name__ == "__main__":
    main_loop()

