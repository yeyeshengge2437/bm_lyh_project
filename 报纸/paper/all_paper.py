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
from guizhoujiankang_paper import get_guizhoujiankang_paper  # 贵州健康报
from sichuannongcun_paper import get_sichuannongcun_paper  # 四川农村日报
from qingdaozao_paper import get_qingdaozao_paper  # 青岛早报
from qinghaikeji_paper import get_qinghaikeji_paper  # 青海科技报
from sichuankeji_paper import get_sichuankeji_paper  # 四川科技报
from guangxinongken_paper import get_guangxinongken_paper  # 广西农垦报
from henankeji_paper import get_henankeji_paper  # 河南科技报
from gansukeji_paper import get_gansukeji_paper  # 甘肃科技报
from shenzhentequ_paper import get_shenzhentequ_paper  # 深圳特区报
from henandahe_paper import get_dahe_paper  # 大河报
from liaoningfazhi_paper import get_liaoningfazhi_paper  # 辽宁法治报
from dalian_paper import get_dalian_paper  # 大连日报
from dalian_lastpaper import get_dalian_lastpaper  # 大连晚报
from shenyang_lastpaper import get_shenyang_lastpaper  # 沈阳晚报
from chinazhishi_paper import get_chinazhishi_paper  # 中国知识产权报
from chinafangdichan_paper import get_chinafangdichan_paper  # 中国房地产报
from chinajijin_paper import get_chinajijin_paper  # 中国基金报
from chinagaoxinjishu_paper import get_chinagaoxinjishu_paper  # 中国高新技术产业导报
from chinalvyou_paper import get_chinalvyou_paper  # 中国旅游报
from chinawenwu_paper import get_chinawenwu_paper  # 中国文物报
from beijing_paper import get_beijing_paper  # 北京日报
from nongmin_paper import get_nongmin_paper  # 农民日报
from guangxizhengxie_paper import get_guangxizhengxie_paper  # 广西政协报
from changchun_lastpaper import get_changchun_lastpaper  # 长春晚报
from yunnan_paper import get_yunnan_paper  # 云南日报
from wulumuqi_lastpaper import get_wulumuqi_lastpaper  # 乌鲁木齐晚报
from lasa_paper import get_lasa_paper  # 拉萨日报
from chinahezuo_paper import get_chinahezuo_paper  # 中华合作时报
from huashang_paper import get_huashang_paper  # 华商报
from geermu_paper import get_geermu_paper  # 格尔木日报
from jiatingyisheng_paper import get_jiatingyisheng_paper  # 家庭医生报
from shangrao_paper import get_shangrao_paper  # 上饶日报
from qiaoxiangkeji_paper import get_qiaoxiangkeji_paper  # 侨乡科技报
from wenzhou_lastpaper import get_wenzhou_lastpaper  # 温州晚报
from wenzhou_paper import get_wenzhou_paper  # 温州日报
from wenzhoudushi_paper import get_wenzhoudushi_paper  # 温州都市报
from wenzhoushang_paper import get_wenzhoushang_paper  # 温州商报
from yiwushang_paper import get_yiwushang_paper  # 义务商报
from shichangdao_paper import get_shichangdao_paper  # 市场导报
from zhengquanshi_paper import get_zhengquanshi_paper  # 证券时报
from lianyi_paper import get_lianyi_paper  # 联谊报
from xiaofeizhiliang_paper import get_xiaofeizhiliang_paper  # 消费质量报
from huaxishequ_paper import get_huaxishequ_paper  # 华西社区报
from yuncheng_lastpaper import get_yuncheng_lastpaper  # 运城晚报
from shenghuo_paper import get_shenghuo_paper  # 生活报
from tumenjiang_paper import get_tumenjiang_paper  # 图们江报
from chinazhiliang_paper import get_chinazhiliang_paper  # 中国质量报
from chinaxiaofeizhe_paper import get_chinaxiaofei_paper  # 中国消费者报
from chinashiyou_paper import get_chinashiyou_paper  # 中国石油报
from linzhi_paper import get_linzhi_paper  # 林芝报
from shannan_paper import get_shannan_paper  # 山南报
from changdu_paper import get_changdu_paper  # 昌都报
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
    '深圳晚报': get_shenzhen_lastpaper,
    '深圳商报': get_shenzhenshang_paper,
    '晶报': get_jingbao_paper,
    '贵州健康报': get_guizhoujiankang_paper,
    '四川农村日报': get_sichuannongcun_paper,
    '青岛早报': get_qingdaozao_paper,
    '青海科技报': get_qinghaikeji_paper,
    '四川科技报': get_sichuankeji_paper,
    '广西农垦报': get_guangxinongken_paper,
    '河南科技报': get_henankeji_paper,
    '甘肃科技报': get_gansukeji_paper,
    '深圳特区报': get_shenzhentequ_paper,
    '大河报': get_dahe_paper,
    '辽宁法治报': get_liaoningfazhi_paper,
    '大连日报': get_dalian_paper,
    '大连晚报': get_dalian_lastpaper,
    '沈阳晚报': get_shenyang_lastpaper,
    '中国知识产权报': get_chinazhishi_paper,
    '中国房地产报': get_chinafangdichan_paper,
    '中国基金报': get_chinajijin_paper,
    '中国高新技术产业导报': get_chinagaoxinjishu_paper,
    '中国旅游报': get_chinalvyou_paper,  # '2020-01-01'
    '中国文物报': get_chinawenwu_paper,  # '2022-07-01'
    '北京日报': get_beijing_paper,  # '2020-07-13'
    '农民日报': get_nongmin_paper,  # '2010-12-14'
    '广西政协报': get_guangxizhengxie_paper,  # '2022-01-01'
    '长春晚报': get_changchun_lastpaper,  # '2017-04-22'
    '云南日报': get_yunnan_paper,  #  '2019-01-01'
    '乌鲁木齐晚报': get_wulumuqi_lastpaper,  # '2024-06-07'
    '拉萨日报': get_lasa_paper,  # '2024-01-01'
    '中华合作时报': get_chinahezuo_paper,
    '华商报': get_huashang_paper,
    '格尔木日报': get_geermu_paper,
    '家庭医生报': get_jiatingyisheng_paper,
    '上饶日报': get_shangrao_paper,
    '侨乡科技报': get_qiaoxiangkeji_paper,
    '温州晚报': get_wenzhou_lastpaper,
    '温州日报': get_wenzhou_paper,
    '温州都市报': get_wenzhoudushi_paper,
    '温州商报': get_wenzhoushang_paper,
    '义务商报': get_yiwushang_paper,
    '市场导报': get_shichangdao_paper,
    '证券时报': get_zhengquanshi_paper,
    '联谊报': get_lianyi_paper,
    '消费质量报': get_xiaofeizhiliang_paper,
    '华西社区报': get_huaxishequ_paper,
    '运城晚报': get_yuncheng_lastpaper,
    '生活报': get_shenghuo_paper,
    '图们江报': get_tumenjiang_paper,
    '中国质量报': get_chinazhiliang_paper,
    '中国消费者报': get_chinaxiaofei_paper,
    '中国石油报': get_chinashiyou_paper,
    '林芝报': get_linzhi_paper,
    '山南报': get_shannan_paper,
    '昌都报': get_changdu_paper,
}

webpage_url_list = [
    'https://newpaper.dahe.cn/hnsb/html',
    'https://szb.gansudaily.com.cn/gsjjrb',
    'https://epaper.kf.cn/paper/kfrb',
    # 'https://lyrb.lyd.com.cn',  # 洛阳日报封ip严重
    'https://epaper.lnd.com.cn',
    'https://www.scxb.com.cn',
    # 'https://tmrb.tmwcn.com/tmrb',  # 天门日报没有pdf
    'https://epaper.scjjrb.com',
    # 'https://www.wccdaily.com.cn', # pdf无法获取
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
    'https://ipaper.pagx.cn',   # 广西法治日报暂停处理, 请求头动态密码
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
    'https://newspaper.gzdaily.cn',
    'http://www.gzswssy.com/paper',
    'https://country.scol.com.cn',
    'https://epaper.guanhai.com.cn/conpaper/qdzb',
    'https://www.xepaper.com/qhkjb',
    'http://kjb.sckjw.com.cn',
    'https://sztqb.sznews.com',
    'https://szsb.sznews.com',
    'https://jb.sznews.com',
    'https://wb.sznews.com',
    'https://gxnkb.ihwrm.com',
    'http://dzb.kjxww.cn',
    'http://www.gskjb.cn/gskjb',
    'https://newpaper.dahe.cn/dhb',
    'https://epaper.lnd.com.cn/lnfzbpaper/pc/layout',
    'http://szb.dltv.cn/epaper/dlrb/pc/layout',
    'http://szb.dltv.cn/epaper/dlwb/pc/layout',
    'https://epaper.syd.com.cn/sywb',
    'http://sz.iprchn.com/bz/html/index.html',
    'https://flbook.com.cn/c/fhFB9tLQvm',
    'https://www.chnfund.com/epaper',
    'http://paper.chinahightech.com/pc/layout',
    'http://wlmqszb.womob.cn',
    'http://www.lasaribao.cn',
    'https://www.ctnews.com.cn/paper',
    'http://www.zhongguowenwubao.com',
    'https://bjrbdzb.bjd.com.cn/bjrb',
    'https://szb.farmer.com.cn',
    'http://www.gxzxbxwzx.com.cn/dzszb/szbcf/index.html',
    'http://epaper.changchunews.com/ccwb/pc/paper/layout',
    'https://yndaily.yunnan.cn',
    'http://www.zh-hz.com',
    'http://ehsb.hspress.net',
    'https://www.geermurb.com',
    'http://jyb.ncrbw.cn',
    'http://paper.srxww.com',
    'https://www.xepaper.com/qxkjb',
    'http://szb.66wz.com/newspaper?mediaKey=wzwb',
    'http://szb.66wz.com/newspaper?mediaKey=wzrb',
    'http://szb.66wz.com/newspaper?mediaKey=wzdsb',
    'http://szb.66wz.com/newspaper?mediaKey=wzsb',
    'http://szb1.ywcity.cn/layout',
    'https://epaper.zjscdb.com',
    'https://epaper.stcn.com',
    'http://www.lybs.com.cn',
    'https://xzb.scol.com.cn',
    'https://www.wccdaily.com.cn/shtml/index_hxdsbsq.shtml',
    'http://epaper.sxycrb.com/wbpaper/pc/layout',
    'http://epaper.hljnews.cn/shb/pc/layout',
    'http://www.tmjnews.net/newspaper.asp',
    'http://zgzlb.183read.cc',
    'https://zxb.ccn.com.cn',
    'http://epaper.cnpc.com.cn/zgsyb',
    'http://www.linzhinews.com/portal/#/list',
    'http://epaper.xzsnw.com/snbhw/html',
    'http://sz.cdbao.cn/cdb',
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
                time.sleep(30)
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
            time.sleep(360)
            print(f"解析过程中发生错误: {e}")


if __name__ == '__main__':
    """
    多进程5个
    """
    process_list = []
    for i in range(5):
        process = Process(target=get_paper_data, args=())
        process_list.append(process)

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()
