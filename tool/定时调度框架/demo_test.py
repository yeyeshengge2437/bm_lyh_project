from apscheduler.schedulers.blocking import BlockingScheduler


def my_task():
    print("定时任务执行中...")


scheduler = BlockingScheduler()
scheduler.add_job(my_task, 'interval', seconds=5)  # 每隔5秒执行一次
scheduler.start()
