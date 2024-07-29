from apscheduler.schedulers.blocking import BlockingScheduler


def my_task():
    print("定时任务执行中...")


scheduler = BlockingScheduler()
scheduler.add_job(my_task, 'interval', seconds=86400)  # 每隔24小时执行一次
scheduler.start()
