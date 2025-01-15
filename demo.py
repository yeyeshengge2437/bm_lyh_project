import time


def timenum_to_time(timenum):
    """
    时间戳转时间
    :param timenum: 时间戳
    :return:
    """
    return time.strftime("%Y-%m-%d", time.localtime(timenum / 1000))

print(timenum_to_time(1694102400))