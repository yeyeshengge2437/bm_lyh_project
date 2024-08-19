from datetime import datetime

from bandao_paper import get_bandao_paper    # 半岛晨报
from chinahuanjing_paper import get_chinahuanjiang_paper  # 中国环境报
from fazhi_paper import get_fazhi_paper  # 法制日报
from henanshang_paper import get_henanshang_paper  # 河南商报
from huaxi_paper import get_huaxi_paper  # 华西都市报
from kaifeng_paper import get_kaifeng_paper  # 开封日报
from kejijinrong import get_jinrong_paper  # 科技金融报
from luoyang_paper import get_luoyang_paper  # 洛阳日报
from meiri_paper import get_meiri_paper  # 每日新报
from qingdao_lastpaper import get_qingdao_lastpaper  # 青岛晚报
from shandongshang_paper import get_shandongshang_paper  # 山东商报
from shichangxing_paper import get_shichangxing_paper  # 市场星报
from tianmen_paper import get_tianmen_paper  # 天门日报
from weifang_lastpaper import get_weifang_lastpaper  # 潍坊晚报
from sichuanjingji_paper import get_sichuanjingji_paper     # 四川经济报


def date_conversion(date, origin_date, data_type):
    """
    日期格式转换
    :param date: 传入的日期数据
    :param origin_date: 原始日期数据的格式
    :param data_type: 想要的日期格式
    :return: 处理好日期格式的日期
    """
    # 日期格式正则表达式
    date = str(date)
    date_obj = datetime.strptime(date, origin_date)
    date = date_obj.strftime(data_type)
    return date



