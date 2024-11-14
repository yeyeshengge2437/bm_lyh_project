from KIMI_free_api import api_alive
import time


while True:
    # 开始时间
    start_time = time.time()
    # 调用api_alive函数
    api_alive()
    # 结束时间
    end_time = time.time()
    # 计算运行时间，如果小于5分钟，等到剩余时间
    if end_time - start_time < 300:
        time.sleep(300 - (end_time - start_time))

