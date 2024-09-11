import time

from AMC.api_paper import paper_queue_next, paper_queue_success, paper_queue_fail
from zhejiangzheshang_chuzhigonggao import get_zhejiangzheshang_chuzhigonggao  # 浙江省浙商资产管理有限公司
from zhongyuanzichan_chuzhigonggao import get_zhongyuanzichan_chuzhigonggao  # 中原资产管理有限公司
from guangdongzichuan_chuzhigonggao import guangdongzichan_chuzhigonggao  # 广东粤财资产管理有限公司
from fujiantouzi_chuzhigonggao import fujiantouzi_chuzhigonggao  # 福建闽投资产管理有限公司
from sichuanfazhan_chuzhigonggao import sichuanfazhan_chuzhigonggao  # 四川发展资产管理有限公司
from huarunyukang_chuzhigonggao import huarunyukang_chuzhigonggao  # 华润渝康资产管理有限公司
from hubeizichan_chuzhigonggao import hubeizichan_chuzhigonggao  # 湖北省资产管理有限公司 --模板(全都从页面中获取)
from jiangxizichan_chuzhigonggao import get_jiangxizichan_chuzhigonggao  # 江西省金融资产管理股份有限公司

methods = {
    'https://www.zsamc.com/index.php/infor/index/20.html#tabNav': get_zhejiangzheshang_chuzhigonggao,  # 浙江省浙商资产管理有限公司
    'https://www.zyamc.net/#/asset-zone/4': get_zhongyuanzichan_chuzhigonggao,  # 中原资产管理有限公司
    'https://www.utrustamc.com/czgg/list.aspx#SubMenu': guangdongzichan_chuzhigonggao,  # 广东粤财资产管理有限公司
    'http://www.mtamc.com.cn/zcxx/czgg/index_1.htm': fujiantouzi_chuzhigonggao,  # 福建闽投资产管理有限公司
    'http://www.scdamc.com/chuzhigonggao': sichuanfazhan_chuzhigonggao,  # 四川发展资产管理有限公司
    'https://crykasset.com/Assets/index.html': huarunyukang_chuzhigonggao,  # 华润渝康资产管理有限公司
    'https://hubeiamc.com/Asset_Disposal_Announcement.html': hubeizichan_chuzhigonggao,  # 湖北省资产管理有限公司
    'https://www.jxfamc.com/jxjrzc/chuzhigonggao/czgg.shtml': get_jiangxizichan_chuzhigonggao,  # 江西省金融资产管理股份有限公司
}

web_list = [
    'https://www.zsamc.com/index.php/infor/index/20.html#tabNav',
    'https://www.zyamc.net/#/asset-zone/4',
    'https://www.utrustamc.com/czgg/list.aspx#SubMenu',
    'http://www.mtamc.com.cn/zcxx/czgg/index_1.htm',
    'http://www.scdamc.com/chuzhigonggao',
    'https://crykasset.com/Assets/index.html',
    'https://hubeiamc.com/Asset_Disposal_Announcement.html',
    'https://www.jxfamc.com/jxjrzc/chuzhigonggao/czgg.shtml'
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
