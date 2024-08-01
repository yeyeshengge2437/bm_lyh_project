import logging
import codecs
import sys
from logging.handlers import TimedRotatingFileHandler


# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, filename="log/all.log")

# 创建TimedRotatingFileHandler
# 设置时间间隔为1天（24小时），点位符%Y-%m-%d指定日志文件的日期格式
# time_rotate_file_handler = TimedRotatingFileHandler(filename="log/all.log", when="midnight", backupCount=30,
#                                                     encoding="utf-8")
# time_rotate_file_handler.suffix = "%Y-%m-%d"
# time_rotate_file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))

# 获取根日志器，并添加我们的TimedRotatingFileHandler
# base = logging.getLogger()
# base.addHandler(time_rotate_file_handler)
base = None


def log_init(name):
    print("log_init: " + name)
    global base
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    log_path = "log/all_" + name + ".log"
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, filename=log_path)
    time_rotate_file_handler = TimedRotatingFileHandler(filename=log_path, when="midnight", backupCount=30,
                                                        encoding="utf-8")
    time_rotate_file_handler.suffix = "%Y-%m-%d"
    time_rotate_file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
    base = logging.getLogger()
    base.addHandler(time_rotate_file_handler)

# api = logging.getLogger("api")
# api.setLevel(logging.INFO)
# api_handler = logging.FileHandler("log/api.log")
# api_handler.setFormatter(logging.Formatter(LOG_FORMAT))
# api.addHandler(api_handler)




