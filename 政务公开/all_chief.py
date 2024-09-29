import time

from canquechanpinzhaohui import get_car_xinwen_data, get_xiaofei_xinwen_data, get_car_gg_data, get_xiaofei_gg_data
from guizhou_yjj import get_yjj_data
from api_chief import paper_queue_next, paper_queue_success, paper_queue_fail
from chinadizhikancha import get_quanguoyichangminglu_data, get_quanguodizhikanchadanwei_data, \
    get_yanzhongshixinmingdan_data
# from shichangjianguanchufawenshu import get_shichangjianguanchufawenshu_data
from chanpinzhiliang_buhegechanpin import get_buhegechanpin_data
from chanpinzhiliangju_gonggao import get_bensigonggao_data
from liaoningzfhcxjst_gonggao import get_liaoningzfhcxjst_gonggao
from chanpinzhilaing_chanpinchoucha import get_chanpinchoucha_data

methods = {
    'https://www.samrdprc.org.cn/qczh/gnzhqc/': get_car_xinwen_data,  # 召回汽车新闻
    'https://www.samrdprc.org.cn/xfpzh/xfpgnzh': get_xiaofei_xinwen_data,  # 召回消费品新闻
    'https://www.samrdprc.org.cn/qczh/qczhgg1': get_car_gg_data,  # 召回汽车公告
    'https://www.samrdprc.org.cn/xfpzh/xfpzhgg': get_xiaofei_gg_data,  # 召回消费品公告
    'https://yjj.guizhou.gov.cn/xwdt/tzgg': get_yjj_data,  # 贵州省药品监督管理局
    'https://dkjgfw.mnr.gov.cn/#/site/credit/abnormal': get_quanguoyichangminglu_data,  # 全国异常名录
    'https://dkjgfw.mnr.gov.cn/#/site/unit/1': get_quanguodizhikanchadanwei_data,  # 全国地质勘查单位
    # 'https://dkjgfw.mnr.gov.cn/#/site/credit/blacklist': get_yanzhongshixinmingdan_data,  # 全国地质勘察行业严重失信名单
    "https://www.samr.gov.cn/zljds/jdcc/index.html": get_buhegechanpin_data,  # 国家市场监督管理总局产品质量安全监督管理局 监督抽查不合格产品发布
    "https://www.samr.gov.cn/zljds/zlgg/bsgg/index.html": get_bensigonggao_data,  # 国家市场监督管理总局产品质量安全监督管理局 本司公告
    # 'https://cfws.samr.gov.cn/list.html?49_ss=16': get_shichangjianguanchufawenshu_data,  # 中国市场监管行政处罚文书网
    'https://zjt.ln.gov.cn/zjt/gsgg/index.shtml': get_liaoningzfhcxjst_gonggao,  # 辽宁省住房和城乡建设厅 公告公示
    'https://psp.e-cqs.cn/ecqsNationalCheckWeb/jdcc/jdcc.jsp': get_chanpinchoucha_data,  # 国家市场监督管理总局产品质量安全监督管理局 产品抽查

}

web_list = [
    'https://www.samrdprc.org.cn/qczh/gnzhqc/',
    'https://www.samrdprc.org.cn/xfpzh/xfpgnzh',
    'https://www.samrdprc.org.cn/qczh/qczhgg1',
    'https://www.samrdprc.org.cn/xfpzh/xfpzhgg',
    'https://yjj.guizhou.gov.cn/xwdt/tzgg',
    'https://dkjgfw.mnr.gov.cn/#/site/credit/abnormal',
    'https://dkjgfw.mnr.gov.cn/#/site/unit/1',
    'https://dkjgfw.mnr.gov.cn/#/site/credit/blacklist',
    "https://www.samr.gov.cn/zljds/jdcc/index.html",
    "https://www.samr.gov.cn/zljds/zlgg/bsgg/index.html",
    'https://zjt.ln.gov.cn/zjt/gsgg/index.shtml',
    'https://psp.e-cqs.cn/ecqsNationalCheckWeb/jdcc/jdcc.jsp',
    # 'https://cfws.samr.gov.cn/list.html?49_ss=16', # 数据量较大，单独运行
]

while True:
    try:
        paper_queue = paper_queue_next(webpage_url_list=web_list)
        if paper_queue is None or len(paper_queue) == 0:
            time.sleep(1800)
            pass
        else:
            queue_id = paper_queue['id']
            webpage_id = paper_queue["webpage_id"]
            webpage_url = paper_queue["webpage_url"]
            try:
                methods[webpage_url](queue_id, webpage_id)
                data = {
                    "id": queue_id,
                    'description': f'数据获取成功',
                }
                paper_queue_success(data=data)
            except Exception as e:
                print(e)
                data = {
                    "id": queue_id,
                    'description': f'程序异常:{e}',
                }
                paper_queue_fail(data=data)
    except Exception as e:
        time.sleep(60)
        print(f"解析过程中发生错误：{e}")
