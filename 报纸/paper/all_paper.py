import time
from datetime import datetime, timedelta
from multiprocessing import Process, Queue, Pool
from bandao_paper import get_bandao_paper  # 半岛都市报
from chinahuanjing_paper import get_chinahuanjiang_paper  # 中国环境报
from chinajingji_paper import get_chinajingji_paper  # 中国经济时报
from chinaqiye_paper import get_chinaqiye_paper  # 中国企业报
from fazhi_paper import get_fazhi_paper  # 法制日报
from kejijinrong import get_kejijinrong_paper  # 科技金融时报
from gansujingji_paper import get_gansujingji_paper  # 甘肃经济日报
from gansufazhi_paper import get_gansufazhi_paper  # 甘肃法治报
from guangxifazhi_paper import get_guangxifazhi_paper  # 广西法治日报
from henanshang_paper import get_henanshang_paper  # 河南商报
from huaxi_paper import get_huaxi_paper  # 华西都市报
from kaifeng_paper import get_kaifeng_paper  # 开封日报
from liaoshen_lastpaper import get_liaoshen_lastpaper  # 辽沈晚报
from luoyang_paper import get_luoyang_paper  # 洛阳日报
from meiri_paper import get_meiri_paper  # 每日新报
from nongyekeji import get_nongyekeji_paper  # 农业科技报
from qingdao_lastpaper import get_qingdao_lastpaper  # 青岛晚报
from shandongshang_paper import get_shandongshang_paper  # 山东商报
from shichangxing_paper import get_shichangxing_paper  # 市场星报
from sichuanjingji_paper import get_sichuanjingji_paper  # 四川经济日报
from tianmen_paper import get_tianmen_paper  # 天门日报
from weifang_lastpaper import get_weifang_lastpaper  # 潍坊晚报
from xinxiang_paper import get_xinxiang_paper  # 新乡日报
from zhengquan_paper import get_zhengquan_paper  # 证券日报
from gongshangdao_paper import get_gongshangdao_paper  # 工商导报
from beihai_paper import get_beihai_paper  # 北海日报
from chuxiong_paper import get_chuxiong_paper  # 楚雄日报
from henanfazhi_paper import get_henanfazhi_paper  # 河南法制报
from xiaofei_paper import get_xiaofei_paper  # 消费日报
from chongqingchen_paper import get_chongqingchen_paper  # 重庆晨报
from qinghaifazhi_paper import get_qinghaifazhi_paper  # 青海法治报
from guizhoufazhi_paper import get_guizhoufazhi_paper  # 贵州法治报
from henan_paper import get_henan_paper  # 河南日报
from guizhou_paper import get_guizhou_paper  # 贵州日报
from sichuanzhengxie_paper import get_sichuanzhenxie_paper  # 四川政协报
from minzhuxieshang_paper import get_minzhuxieshang_paper  # 民主协商报
from guizhouminzu_paper import get_guizhouminzu_paper  # 贵州民族报
from hainannongken_paper import get_hainannongkeng_paper  # 海南农垦报
from guangzhou_paper import get_guangzhou_paper  # 广州日报
from shenzhen_lastpaper import get_shenzhen_lastpaper  # 深圳晚报
from shenzhenshang_paper import get_shenzhenshang_paper  # 深圳商报
from jingbao_paper import get_jingbao_paper  # 晶报
from api_paper import paper_queue_next, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url

methods = {
    '半岛都市报': get_bandao_paper,
    '中国环境报': get_chinahuanjiang_paper,
    '中国经济时报': get_chinajingji_paper,
    '中国企业报': get_chinaqiye_paper,
    '法制日报': get_fazhi_paper,
    '甘肃经济日报': get_gansujingji_paper,
    '广西法治日报': get_guangxifazhi_paper,
    '河南商报': get_henanshang_paper,
    '华西都市报': get_huaxi_paper,
    '开封日报': get_kaifeng_paper,
    '辽沈晚报': get_liaoshen_lastpaper,
    '洛阳日报': get_luoyang_paper,
    '每日新报': get_meiri_paper,
    '农业科技报': get_nongyekeji_paper,
    '青岛晚报': get_qingdao_lastpaper,
    '山东商报': get_shandongshang_paper,
    '市场星报': get_shichangxing_paper,
    '四川经济日报': get_sichuanjingji_paper,
    '天门日报': get_tianmen_paper,
    '潍坊晚报': get_weifang_lastpaper,
    '新乡日报': get_xinxiang_paper,
    '证券日报': get_zhengquan_paper,
    '工商导报': get_gongshangdao_paper,
    '北海日报': get_beihai_paper,
    '楚雄日报': get_chuxiong_paper,
    '河南法制报': get_henanfazhi_paper,
    '消费日报': get_xiaofei_paper,
    '重庆晨报': get_chongqingchen_paper,
    '青海法治报': get_qinghaifazhi_paper,
    '贵州法治报': get_guizhoufazhi_paper,
    '科技金融时报': get_kejijinrong_paper,
    '甘肃法治报': get_gansufazhi_paper,
    '河南日报': get_henan_paper,
    '贵州日报': get_guizhou_paper,
    '四川政协报': get_sichuanzhenxie_paper,
    '民主协商报': get_minzhuxieshang_paper,
    '贵州民族报': get_guizhouminzu_paper,
    '海南农垦报': get_hainannongkeng_paper,
    '广州日报': get_guangzhou_paper,
    '深圳晚报': get_shenzhen_lastpaper,  # 未在队列 'https://wb.sznews.com'
    '深圳商报': get_shenzhenshang_paper,  # 未在队列 'https://szsb.sznews.com'
    '晶报': get_jingbao_paper,  # 未在队列 'https://jb.sznews.com'
}

webpage_url_list = [
    'https://newpaper.dahe.cn/hnsb/html',
    'https://szb.gansudaily.com.cn/gsjjrb',
    'https://epaper.kf.cn/paper/kfrb',
    'https://lyrb.lyd.com.cn',  # 洛阳日报封ip，目前已解除
    'https://epaper.lnd.com.cn',
    'https://www.scxb.com.cn',
    # 'https://tmrb.tmwcn.com/tmrb',  # 天门日报没有pdf
    'https://epaper.scjjrb.com',
    'https://www.wccdaily.com.cn',
    'https://epaper.cenews.com.cn',
    'https://epaper.qingdaonews.com',
    'https://dzb.subaoxw.com',
    'https://bddsb.bandao.cn',
    'https://wfwb.wfnews.com.cn',
    'https://epaper.tianjinwe.com/mrxb',
    'http://eb.nkb.com.cn/nykjb',
    'http://epaper.legaldaily.com.cn/fzrb',
    'http://gsdbs.baozhanmei.net',
    'https://rb.xxrb.com.cn/epaper',
    'https://epaper.zqrb.cn',
    'https://jjsb.cet.com.cn',
    'http://kjb.zjol.com.cn',
    'http://epaper.zqcn.com.cn',
    'https://ipaper.pagx.cn',
    'http://epaper.chuxiong.cn',
    'https://newpaper.dahe.cn/jrab/html/2024-07/18/node_2170.htm',
    'https://epaper.bhxww.com/bhrb',
    'https://newpaper.dahe.cn/hnrb',
    'http://szb.eyesnews.cn',
    'https://szb.gansudaily.com.cn/gsfzb',
    'https://szb.fzshb.cn/fzshb',
    'https://epaper.cqcb.com',
    'http://dzb.xfrb.com.cn',
    'https://www.qhfzb.com',
    'https://www.sczx.gov.cn/newspaper',
    'http://szb.mzxsb.com',
    'http://47.108.237.88',
    'http://www.hnnkb.cn',
    'https://newspaper.gzdaily.cn'
]


# webpage_url_list_test = ['https://szb.gansudaily.com.cn/gsjjrb']
def get_paper_data():
    while True:
        try:
            # 调用paper_queue_next函数并获取返回值
            paper_queue = paper_queue_next(
                webpage_url_list=webpage_url_list)
            # 检查返回值是否符合预期
            if paper_queue is None or len(paper_queue) == 0:
                time.sleep(1800)
                pass
            else:
                webpage_name = paper_queue['webpage_name']
                queue_day = paper_queue['day']
                queue_id = paper_queue['id']
                webpage_id = paper_queue["webpage_id"]
                print(queue_day)
                try:
                    methods[webpage_name](queue_day, queue_id, webpage_id)
                except Exception as e:
                    if '该日期没有报纸' in str(e):
                        print('该日期没有报纸')
                        data = {
                            "id": queue_id,
                            'description': f'该日期没有报纸',
                        }
                        paper_queue_delay(data)
                    else:
                        print(f"{e}")
                        fail_data = {
                            "id": queue_id,
                            'description': f'程序异常：{e}',
                        }
                        paper_queue_fail(fail_data)

        except Exception as e:
            time.sleep(3600)
            print(f"解析过程中发生错误: {e}")


if __name__ == '__main__':
    """
    多进程1个
    """
    process_list = []
    for i in range(1):
        process = Process(target=get_paper_data, args=())
        process_list.append(process)

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()
