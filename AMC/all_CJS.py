import time

from api_paper import paper_queue_next, paper_queue_success, paper_queue_fail
from yindeng_zhuanranggonggao import get_yindengzhongxin_zhuanranggonggao   # 银登中心转让公告
from shanghaichanjiaosuo_zhaiquanxiangmu import get_shanghaichanjiangsuo_zhaiquanxiangmu   # 上海联合产权交易所——债权项目
from beijingchanquanjiaoyisuo_zhaiquanzichan import get_beijingchanquanjiaoyi_zhaiquanzichan  # 北京产权交易所——债权资产
from quanguochanquanhangye import get_quanguochanquanhangye_zhaiquan   # 全国产权交易行业——债权
from xinjiangchanquanjiaoyisuo import get_xinjiangchanquanjiaoyisuo_zhaiquan   # 新疆产权交易所——债权
from xiamenchanquanjiaoyizhongxin import get_xiamenchanquanjiaoyizhongxin    # 厦门产权交易所
from yantailianhechanquanjiaoyizhongxin import get_yantailianhechanquanjiaoyizhongxin   # 烟台联合产权交易中心
from henanshengchanquanjiaoyizhongxin import get_henanshengchanquanjiaoyizhongxin   # 河南省产权交易中心
from heilongjiangchanquanjiaoyisuo import get_heilongjiangchanquanjiaoyisuo   # 黑龙江产权交易所
from foshannanfangchanquanjiaoyi import get_fuoshannanfangchanquanjiaoyi   # 佛山市南方产权交易所
from ningxiachanquanjiaoyisuo import get_ningxiachanquanjiaoyi    # 宁夏产权交易
from hainanchanquanjiaoyi import get_hainanchanquanjiaoyi    # 海南产权交易
# from changzhoujiaoyishichang import get_changzhoujiaoyishichang    # 常州交易市场
from chongqingchanquanjiaoyi import get_chongqingchanquanjiaoyi    # 重庆产权交易所
from neimengguchanjiao import get_neimengguchanquanjiaoyi_zichanchaoshizhaiquan    # 内蒙古产权交易所_资产超市债权
from neimengguchanjiao import get_neimengguchanquanjiaoyi_guapaixiangmuzhaiquan     # 内蒙古产权交易所_挂牌项目债权
from hunanshenglianhechanquanjiaoyi import get_hunanchanquanlianhejiaoyi    # 湖南产权联合交易
from nanfanglianhechanquanjiaoyi import get_nanfanglianhechanquanjiaoyi    # 南方联合产权交易所
from qinghaishengchanquanjiaoyishichang import get_qinghaishengchanquanjiaoyishichang   # 青海省产权交易市场
from gansushengchanquanjiaoyisuoxinzhi import get_gansushengchanquanjiaoyisuoxinzhi    # 甘肃省产权交易所新址
from gansushengchanquanjiaoyijiuzhi import get_gansushengchanquanjiaoyijiuzhi    # 甘肃省产权交易所旧址
from guizhouyangguangchanquanjiaoyisuo import get_guizhouyangguangchanquanjiaoyisuo    # 贵州阳光产权交易所
from shenzhenlianhechanquanjiaoyisuo import get_shenzhenlianhechanquanjiaoyisuo    # 深圳联合产权交易所
from guandonglianhechanquanjiaoyizhongxin import get_guandonglianhechanquanjiaoyizhongxin    # 广东省联合产权交易中心
from changshalianhechanquanjiaoyisuo import get_changshalianhechanquanjiaoyisuo    # 长沙联合产权交易所
from wuhanguanggulianhejiaoyisuo import get_wuhanguanggulianhejiaoyisuo    # 武汉光谷联合交易所
from qingdaochanquanjiaoyisuo import get_qingdaochanquanjiaoyisuo    # 青岛产权交易所
from jiangxishengchanquanjiaoyisuo import get_jiangxishengchanquanjiaoyisuo    # 江西省产权交易所
from fujianchanquanjiaoyiwang import get_fujianchanquanjiaoyiwang    # 福建产权交易网
from anhuichanquanjiaoyizhongxin import get_anhuichanquanjiaoyizhongxin    # 安徽省产权交易中心
from taizhoushichanquanjiaoyisuo import get_taizhoushichanquanjiaoyisuo    # 台州市产权交易市场
from zhejiangchanquanjiaoyisuo import get_zhejiangchanquanjiaoyisuo    # 浙江产权交易所
from suzhouchanquanjiaoyizhongxin import get_suzhouchanquanjiaoyizhongxin    # 苏州市产权交易中心
from dalianchanquanjiaoyisuo import get_dalianchanquanjiaoyisuo    # 大连产权交易所
from shandongchanquanjiaoyizhongxin import get_shandongchanquanjiaoyizhongxin    # 山东省产权交易中心
from wenzhoulianhechanquanjiaoyizhongxin import get_wenzhoulianhechanquanjiaoyizhongxin    # 温州联合产权交易中心
from guangxijiaoyisuojituan import get_guangxijiaoyisuojituan    # 广西交易集团
from yiwuchanquanjiaoyisuo import get_yiwuchanquanjiaoyisuo    # 义乌产权交易所
from tianjingchanquanjiaoyipingtai import get_tianjingchanquanjiaoyipingtai    # 天津产权交易中心
from guangzhouchanquanjiaoyisuo import get_guangzhouchanquanjiaoyisuo    # 广州产权交易所
from beibuwanchanquanjiaoyisuo import get_beibuwanchanquanjiaoyisuo    # 北部湾产权交易所
from xinanlianhechanquanjiaoyisuo import get_xinanlianhechanquanjiaoyisuo    # 西南联合产权交易所
from jiangsuchanquanshichangwang import get_jiangsuchanquanshichangwang    # 江苏产权市场网
from quanguochanquanjiaoyizhongxin import get_quanguochanquanjiaoyizhongxin    # 全国产权交易中心
from shanxishengchanquanjiaoyishichang import get_shanxishengchanquanjiaoyizhongxin    # 山西省产权交易中心

methods = {
    'https://www.yindeng.com.cn/ywzq/ywzq_bldkzr/bldkzr_xxpl/bldkzr_xxpl_zrgg': get_yindengzhongxin_zhuanranggonggao,  # 银登中心转让公告
    'https://www.suaee.com/suaeeHome/#/projectCenter?pageCode=zhaiquan': get_shanghaichanjiangsuo_zhaiquanxiangmu,  # 上海市产权交易中心-债权项目
    'https://www.cbex.com.cn/xm/zqzc': get_beijingchanquanjiaoyi_zhaiquanzichan,  # 北京市产权交易所-债权资产
    'https://www.cspea.com.cn/list?c=C05&s=A02,A03': get_quanguochanquanhangye_zhaiquan,   # 全国产权行业信息化综合服务平台
    'https://xjcqjy.ejy365.com/EJY/Project?projectType=001001001&HeadId=1': get_xinjiangchanquanjiaoyisuo_zhaiquan,   # 新疆产权交易所——债权
    'https://www.xemas.com.cn/project-announcement.html?parent-uid=&self-uid=&type=total&sub-uid=': get_xiamenchanquanjiaoyizhongxin,   # 厦门产权交易中心
    'http://www.ytcq.com/tzgg/about.html': get_yantailianhechanquanjiaoyizhongxin,  # 烟台联合产权交易中心
    'https://sta.hnprec.com/client/#/buyerweb/?BusinessTypeId=HouseLand': get_henanshengchanquanjiaoyizhongxin,  # 河南省产权交易中心
    'https://hljcqjy.ejy365.com/EJY/Project?searchKids=%E5%80%BA%E6%9D%83': get_heilongjiangchanquanjiaoyisuo,    # 黑龙江产权交易所
    'https://www.fsaee.com/?cid-288_lbid-7_qycq.html': get_fuoshannanfangchanquanjiaoyi,  # 佛山南方产权交易市场
    'http://www.sdcqjy.com/zccz/articlelist/cjgg': get_shandongchanquanjiaoyizhongxin,    # 山东省产权交易中心
    'http://www.naee.com.cn/newsLists.do?classId=185': get_ningxiachanquanjiaoyi,    # 宁夏产权交易中心
    'http://www.hncq.cn/index.php?m=content&c=index&a=lists&catid=17&proType=&areaid=&keyword=': get_hainanchanquanjiaoyi,   # 海南产权交易
    # 'http://www.czcq.com.cn/czcq/property': get_changzhoujiaoyishichang,    # 常州市产权交易市场
    'https://www.cquae.com/Project?q=s&projectID=5&#name1': get_chongqingchanquanjiaoyi,   # 重庆产权交易市场
    'https://nmgcqjy.ejy365.com/FinanceReform/NewsIndex?firTypeName=%E8%B5%84%E4%BA%A7%E8%B6%85%E5%B8%82&secTypeName=%E5%80%BA%E6%9D%83&secID=10653&firID=10636&HeadId=4': get_neimengguchanquanjiaoyi_zichanchaoshizhaiquan,   # 内蒙古产权交易所-资产超市债权
    'https://nmgcqjy.ejy365.com/FinanceReform/ProjectIndex?projectType=%E5%80%BA%E6%9D%83&HeadId=2' : get_neimengguchanquanjiaoyi_guapaixiangmuzhaiquan,   # 内蒙古产权交易所-挂牌项目债权
    'https://www.hnaee.com/hnaee/xmzx.jsp': get_hunanchanquanlianhejiaoyi,    # 湖南产权联合交易
    'https://www.csuaee.com.cn/searchItem.html?keyword=%E5%80%BA%E6%9D%83' : get_nanfanglianhechanquanjiaoyi,    # 南方联合产权交易中心
    'http://www.qhcqjy.com/info.do' : get_qinghaishengchanquanjiaoyishichang,    # 青海省产权交易市场
    'http://jrzc.gscq.com.cn:9116/#/example/project?a=2290&b=%E6%8E%A8%E4%BB%8B%E6%9C%9F' : get_gansushengchanquanjiaoyisuoxinzhi,    # 甘肃省产权交易所新址
    'https://old.gscq.com.cn/index.php?s=xm&c=category&id=4' : get_gansushengchanquanjiaoyijiuzhi,    # 甘肃省产权交易所旧址
    'https://www.prechina.net/project/project.php?class3=52' : get_guizhouyangguangchanquanjiaoyisuo,    # 贵州阳光产权交易所
    'https://www.sotcbb.com/xmgg?id=xmggjrzczrzspl': get_shenzhenlianhechanquanjiaoyisuo,    # 深圳联合产权交易所
    'https://www.gduaee.com/www/article/tzgg/xxgg' :get_guandonglianhechanquanjiaoyizhongxin,    # 广东联合产权交易中心
    'https://www.cscqjy.com.cn/xiangmuzhongxin/teshuzichan' : get_changshalianhechanquanjiaoyisuo,    # 长沙联合产权交易所
    'https://www.ovupre.com/list/19.html?type=new' : get_wuhanguanggulianhejiaoyisuo,  # 武汉光谷联合交易所
    'https://cqjy.qdcq.net/pro/?UTRM&proType=bondproc&status=all': get_qingdaochanquanjiaoyisuo,   # 青岛产权交易所
    'https://jxcq.jxggzyjy.cn/cqjy/004/004005/project_center.html': get_jiangxishengchanquanjiaoyisuo,    # 江西省产权交易所
    'https://www.fjcqjy.com/html/list-content-4n3y18347bt227rw7soh.html': get_fujianchanquanjiaoyiwang,    # 福建产权交易网
    'https://aaee.com.cn/xmzx.html#/financial_assets': get_anhuichanquanjiaoyizhongxin,    # 安徽省产权交易中心
    'http://www.tzpre.com/index.php/cms/item-search?keyword=%E5%80%BA%E6%9D%83&submit=%E6%90%9C%E7%B4%A2': get_taizhoushichanquanjiaoyisuo,    # 台州市产权交易市场
    'https://www.zjpse.com/page/s/prjs/zhjy/index': get_zhejiangchanquanjiaoyisuo,    # 浙江产权交易所
    'https://www.szee.com.cn/jrzc': get_suzhouchanquanjiaoyizhongxin,    # 苏州市产权交易中心
    'https://www.daee.cn/article/xmdt/jrzq': get_dalianchanquanjiaoyisuo,    # 大连产权交易所
    'https://sxcqsc.sxcqjy.cn/xmzx.html#/dept': get_shanxishengchanquanjiaoyizhongxin,    # 山东省产权交易中心
    'https://www.wzcqpt.com/WZPT/page/s/announcement/equity/index': get_wenzhoulianhechanquanjiaoyizhongxin,   # 温州联合产权交易中心
    'http://www.gxcq.com.cn/list-154.html#assetsTypeParent=ZQ': get_guangxijiaoyisuojituan,   # 广西产权交易所集团
    'https://www.ywcq.com/article/xmgg/zczr': get_yiwuchanquanjiaoyisuo,    # 义乌产权交易所
    'https://trade.tpre.cn/finance-view/project-info/special-assets': get_tianjingchanquanjiaoyipingtai,    # 天津产权交易平台
    'http://gz.gemas.com.cn/portal/page?to=cmsUtrSearchAll&pageIndex=1&sysEname=MGZL&queryKey=%E5%80%BA%E6%9D%83': get_guangzhouchanquanjiaoyisuo,    # 广州产权交易所
    'https://bbwcq.com/projects?pageNumber=1&pageSize=12&proTypeSearch=3&bidTypeSearch=6&areaCtyCode=%E5%85%A8%E9%83%A8&keyWord=&priceLow=0&priceHigh=0&status=0&orderType=0&orderBy=desc': get_beibuwanchanquanjiaoyisuo,    # 北部湾产权交易所
    'https://www.swuee.com/#/project?parentId=&operationId=1408017492266409986': get_xinanlianhechanquanjiaoyisuo,    # 西南联合产权交易所
    'https://www.jscq.com.cn/jscq/cqjy/zypt/blzcjypt/index.shtml': get_jiangsuchanquanshichangwang,    # 江苏产权市场网
    'https://www.ejy365.com/jygg_more?project_type=ZQ': get_quanguochanquanjiaoyizhongxin,    # 全国产权交易中心
}

web_list = [
    # 'https://www.yindeng.com.cn/ywzq/ywzq_bldkzr/bldkzr_xxpl/bldkzr_xxpl_zrgg',
    # 'https://www.suaee.com/suaeeHome/#/projectCenter?pageCode=zhaiquan',
    # 'https://www.cbex.com.cn/xm/zqzc',  # 北京产权交易所的需要更换cookies
    # 'https://www.cspea.com.cn/list?c=C05&s=A02,A03',
    # 'https://xjcqjy.ejy365.com/EJY/Project?projectType=001001001&HeadId=1',
    # 'https://www.xemas.com.cn/project-announcement.html?parent-uid=&self-uid=&type=total&sub-uid=',
    # 'http://www.ytcq.com/tzgg/about.html',
    # 'https://sta.hnprec.com/client/#/buyerweb/?BusinessTypeId=HouseLand',
    # 'https://hljcqjy.ejy365.com/EJY/Project?searchKids=%E5%80%BA%E6%9D%83',
    # 'https://www.fsaee.com/?cid-288_lbid-7_qycq.html',
    # 'http://www.sdcqjy.com/zccz/articlelist/cjgg',
    # 'http://www.naee.com.cn/newsLists.do?classId=185',
    # 'http://www.hncq.cn/index.php?m=content&c=index&a=lists&catid=17&proType=&areaid=&keyword=',
    # 'http://www.czcq.com.cn/czcq/property',
    # 'https://www.cquae.com/Project?q=s&projectID=5&#name1',
    # 'https://nmgcqjy.ejy365.com/FinanceReform/NewsIndex?firTypeName=%E8%B5%84%E4%BA%A7%E8%B6%85%E5%B8%82&secTypeName=%E5%80%BA%E6%9D%83&secID=10653&firID=10636&HeadId=4',
    'https://nmgcqjy.ejy365.com/FinanceReform/ProjectIndex?projectType=%E5%80%BA%E6%9D%83&HeadId=2',
    'https://www.hnaee.com/hnaee/xmzx.jsp',
    'https://www.csuaee.com.cn/searchItem.html?keyword=%E5%80%BA%E6%9D%83',
    'http://www.qhcqjy.com/info.do',
    'http://jrzc.gscq.com.cn:9116/#/example/project?a=2290&b=%E6%8E%A8%E4%BB%8B%E6%9C%9F',
    'https://old.gscq.com.cn/index.php?s=xm&c=category&id=4',
    'https://www.prechina.net/project/project.php?class3=52',
    'https://www.sotcbb.com/xmgg?id=xmggjrzczrzspl',
    'https://www.gduaee.com/www/article/tzgg/xxgg',
    'https://www.cscqjy.com.cn/xiangmuzhongxin/teshuzichan',
    'https://www.ovupre.com/list/19.html?type=new',
    'https://cqjy.qdcq.net/pro/?UTRM&proType=bondproc&status=all',
    'https://jxcq.jxggzyjy.cn/cqjy/004/004005/project_center.html',
    'https://www.fjcqjy.com/html/list-content-4n3y18347bt227rw7soh.html',
    'https://aaee.com.cn/xmzx.html#/financial_assets',
    'http://www.tzpre.com/index.php/cms/item-search?keyword=%E5%80%BA%E6%9D%83&submit=%E6%90%9C%E7%B4%A2',
    'https://www.zjpse.com/page/s/prjs/zhjy/index',
    'https://www.szee.com.cn/jrzc',
    'https://www.daee.cn/article/xmdt/jrzq',
    # 'https://sxcqsc.sxcqjy.cn/xmzx.html#/dept',
    # 'https://www.wzcqpt.com/WZPT/page/s/announcement/equity/index',
    # 'http://www.gxcq.com.cn/list-154.html#assetsTypeParent=ZQ',
    # 'https://www.ywcq.com/article/xmgg/zczr',
    # 'https://trade.tpre.cn/finance-view/project-info/special-assets',
    # 'http://gz.gemas.com.cn/portal/page?to=cmsUtrSearchAll&pageIndex=1&sysEname=MGZL&queryKey=%E5%80%BA%E6%9D%83',
    # 'https://bbwcq.com/projects?pageNumber=1&pageSize=12&proTypeSearch=3&bidTypeSearch=6&areaCtyCode=%E5%85%A8%E9%83%A8&keyWord=&priceLow=0&priceHigh=0&status=0&orderType=0&orderBy=desc',
    # 'https://www.swuee.com/#/project?parentId=&operationId=1408017492266409986',
    # 'https://www.jscq.com.cn/jscq/cqjy/zypt/blzcjypt/index.shtml',
    # 'https://www.ejy365.com/jygg_more?project_type=ZQ',
]


while True:
    try:
        paper_queue = paper_queue_next(webpage_url_list=web_list)
        if paper_queue is None or len(paper_queue) == 0:
            time.sleep(600)
            continue
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

