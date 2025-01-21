import time

from heilongjiang_ktgg import get_lhjcourt_info
from chongqing_ktgg import get_cqcourt_info
from zhejiang_ktgg import get_zjcourt_info
from shanxi_ktgg import get_sxcourt_1_info
from jiangsu_ktgg import get_jscourt_info
from shanghai_ktgg import get_shcourt_info
from xuzhou_ktgg import get_xzcourt_info
from wuxi_ktgg import get_wxcourt_info
from guangdong_ktgg import get_gdcourt_info
from shanxi_ktgg_shan import get_sxcourt_info_shan
from chinashenpan_ktgg import get_chinacourt_info
from beijing_ktgg import get_bjcourt_info
from a_ktgg_api import queue_next, queue_success, queue_fail

methods = {
    'http://www.hljcourt.gov.cn/ktgg': get_lhjcourt_info,  # 黑龙江省高级人民法院
    'http://www.cqfygzfw.gov.cn/gggs/toListKtggNL.shtml?page=1': get_cqcourt_info,  # 重庆法院公众服务网
    'https://www.zjsfgkw.gov.cn/jkts/search/ktgglist.do': get_zjcourt_info,  # 浙江法院网
    'http://sxgaofa.cn/sxssfw/ktgg/toListKtggNL.shtml': get_sxcourt_1_info,  # 陕西法院诉讼服务网
    'https://ssfw.jsfy.gov.cn/#/ywym?onetitle=4&title=ktgg': get_jscourt_info,  # 江苏法院诉讼服务网
    'https://www.hshfy.sh.cn/shwfy/ssfww/ktgg.jsp': get_shcourt_info,  # 上海法院诉讼服务网
    "https://ssfw.xzfy.gov.cn/#/fyxx?label=0": get_xzcourt_info,  # 徐州法院诉讼服务网
    "https://ssfw.wxfy.gov.cn/lawsuit/case/#/sfgk": get_wxcourt_info,  # 无锡法院诉讼服务网
    "https://www.gdcourts.gov.cn/ktgg/index.html": get_gdcourt_info,  # 广东法院网
    "https://www.shanxify.gov.cn/ktgg/index.jhtml": get_sxcourt_info_shan,  # 山西法院诉讼服务网
    "https://splcgk.court.gov.cn/gzfwww//ktgg": get_chinacourt_info,  # 中国审判流程信息公开网
    "https://www.bjcourt.gov.cn": get_bjcourt_info,  # 北京法院审判信息网
}
web_list = [
    'http://www.hljcourt.gov.cn/ktgg',
    'http://www.cqfygzfw.gov.cn/gggs/toListKtggNL.shtml?page=1',
    'https://www.zjsfgkw.gov.cn/jkts/search/ktgglist.do',
    'http://sxgaofa.cn/sxssfw/ktgg/toListKtggNL.shtml',
    'https://ssfw.jsfy.gov.cn/#/ywym?onetitle=4&title=ktgg',
    'https://www.hshfy.sh.cn/shwfy/ssfww/ktgg.jsp',
    "https://ssfw.xzfy.gov.cn/#/fyxx?label=0",
    "https://ssfw.wxfy.gov.cn/lawsuit/case/#/sfgk",
    "https://www.gdcourts.gov.cn/ktgg/index.html",
    "https://www.shanxify.gov.cn/ktgg/index.jhtml",
    "https://splcgk.court.gov.cn/gzfwww//ktgg",
    "https://www.bjcourt.gov.cn",
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
