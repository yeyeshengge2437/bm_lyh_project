import time

from AMC.api_paper import paper_queue_next, paper_queue_success, paper_queue_fail
from zhejiangzheshang_chuzhigonggao import get_zhejiangzheshang_chuzhigonggao  # 浙江省浙商资产管理有限公司
from zhongyuanzichan_chuzhigonggao import get_zhongyuanzichan_chuzhigonggao  # 中原资产管理有限公司
from guangdongzichuan_chuzhigonggao import guangdongzichan_chuzhigonggao  # 广东粤财资产管理有限公司
from fujiantouzi_chuzhigonggao import fujiantouzi_chuzhigonggao  # 福建闽投资产管理有限公司
from sichuanfazhan_chuzhigonggao import sichuanfazhan_chuzhigonggao  # 四川发展资产管理有限公司
from huarunyukang_chuzhigonggao import huarunyukang_chuzhigonggao  # 华润渝康资产管理有限公司
from hubeizichan_chuzhigonggao import hubeizichan_chuzhigonggao  # 湖北省资产管理有限公司 --模板(全都从页面中获取)
from jiangxizichan_chuzhigonggao import get_jiangxizichan_chuzhigonggao  # 江西省金融资产管理股份有限公司  --模板(全都从接口中获取)
from ningbozichan_chuzhigonggao import get_ningbozichan_chuzhigonggao  # 宁波金融资产管理股份有限公司 --含有附件
from suzhouzichan_chuzhigonggao import get_suzhouzichan_chuzhigonggao  # 苏州资产管理有限公司
from jiangsuzichan_chuzhigonggao import get_jiangsuzichan_chuzhigonggao  # 江苏资产管理有限公司
from ningxiajinrong_chuzhigonggao import get_ningxiajinrong_chuzhigonggao  # 宁夏金融资产管理有限公司
from shanxijinrong_chuzhigonggao import get_shanxijinrong_chuzhigonggao  # 陕西金融资产管理股份有限公司
from guangzhouzichan_chuzhigonggao import get_guangzhouzichan_chuzhigonggao  # 广州资产管理有限公司 --模板(全都从页面中获取)含有附件, 增加判断截图出错情况
from changshaxiangjiang_chuzhigonggao import get_changshaxiangjiang_chuzhigonggao  # 长沙湘江资产管理有限公司
from hunancaixin_chuzhigonggao import get_hunancaixin_chuzhigonggao  # 湖南省财信资产管理有限公司
from henanzichan_chuzhigonggao import get_henanzichan_chuzhigonggao  # 河南资产管理有限公司
from zhongxinqinggao_chuzhigonggao import get_zhongxinqingdao_chuzhigonggao  # 中信青岛资产管理有限公司
from xingyezichan_chuzhigonggao import get_xinyezichan_chuzhigonggao  # 兴业资产管理有限公司
from azhuizhongan_chuzhigonggao import get_anhuizhongan_chuzhigonggao  # 安徽省中安金融资产管理股份有限公司
from guangdazichan_chuzhigonggao import get_guangdazichan_chuzhigonggao  # 光大金瓯资产管理有限公司
from jilinshengrong_chuzhigonggao import get_jilinshengrong_chuzhigonggao  # 吉林省盛融资产管理有限责任公司
from shanghaiguoyou_chuzhigonggao import get_shanghaiguoyou_chuzhigonggao  # 上海国有资产经营有限公司
from neimenggujinrong_chuzhigonggao import get_neimenggujinrong_chuzhigonggao  # 内蒙古金融资产管理有限公司
from hebeiziguan_chuzhigonggao import get_hebeiziguan_chuzhigonggao  # 河北省资产管理有限公司
from yunnanzichan_chuzhigonggao import get_yunnanzichan_chuzhigonggao  # 云南省资产管理有限公司
from hainanlianhe_chuzhigonggao import get_hainanzichan_chuzhigonggao  # 海南联合资产管理有限公司
from shenzenzichan_chuzhigonggao import get_shenzenzichan_chuzhigonggao  # 深圳资产管理有限公司
from shenzhenzhaoshang_chuzhigonggao import get_shenzhenzhaoshang_chuzhigonggao  # 深圳市招商平安资产管理有限责任公司
from liaoningzichan_chuzhigonggao import get_liaoningzichan_chuzhigonggao  # 辽宁资产管理有限公司
from azhuiguohou_chuzhigonggao import get_azhuiguohou_chuzhigonggao  # 安徽国厚金融资产管理有限公司
from GZH_zhongxinjinrongjiangsu import zhongxinjinrongjiangsu_gzh  # 中国中信金融资产江苏分公司(公众号)
from GZH_zhongxinjinrongguangdong import zhongxinjinrongguangdong_gzh  # 中国中信金融资产广东分公司(公众号)
from GZH_zhongxinjinrongzhejiang import zhongxinjinrongzhejiang_gzh  # 中国中信金融资产浙江分公司(公众号)
from jiangsuzichan_zichantuijie import get_jiangsuzichan_zichantuijie    # 江苏资产管理有限公司_资产推介
from zhongguochangchengzichan_zichanyingxiao import get_zhongguochangchengzichan_zichanyingxiao   # 中国长城资产管理股份有限公司_资产营销
from zhejiangzheshang_zichantuijie import get_zhejiangzheshang_zichantuijie  # 浙江省浙商资产管理有限公司_资产推介
from changshaxiangjiang_zichantuijie import get_changshaxiangjiang_zichantuijie  # 长沙湘江资产管理有限公司_资产推介
from fujiantouzi_tuijiexinxi import fujiantouzi_tuijiexinxi  # 福建闽投资产管理有限公司_资产推介
from hunancaixin_zichantuijie import get_hunancaixin_zichantuijie  # 湖南省财信资产管理有限公司_资产推介
from zhongxinqingdao_zichantuijie import get_zhongxinqingdao_zichantuijie  # 中信青岛资产管理有限公司_资产推介
from guangzhouzichan_tuijiexinxi import get_guangzhouzichan_zichantuijie   # 广州资产管理有限公司_资产推介
from henanzichan_zichantuijie import get_henanzichan_zichantuijie  # 河南资产管理有限公司_资产推介
from sichuanfazhan_zichantuijie import sichuanfazhan_zichantuijie   # 四川发展资产管理有限公司_资产推介
from zhongyuanzichan_zichantuijie import get_zhongyuanzichan_zichantuijie  # 中原资产管理有限公司_资产推介
from xingyezichan_zichantuijie import get_xinyezichan_zichantuijie  # 兴业资产管理有限公司_资产推介
from azhuiguohou_zichantuijie import get_azhuiguohou_zichantuijie  # 安徽国厚金融资产管理有限公司_资产推介
from suzhouzichan_zichantuijie import get_suzhouzichan_zichantuijie    # 苏州资产管理有限公司_资产推介
from jiangxizichan_zichanzhanshi import get_jiangxizichan_zichanzhanshi    # 江西省金融资产管理股份有限公司_资产展示
from jiangxiruijingzichan_zichantuijie import get_jiangxiruijin_zichantuijie   # 江西瑞京资产管理有限公司_资产推介
from heilongjiangguoruizichan_xiangmutuijie import get_heilongjiangguoruizichan_xiangmutuijie    # 黑龙江国瑞资产管理有限公司_项目推介
from yunnanzichan_zichantuijie import get_yunnanzichan_zichantuijie  # 云南省资产管理有限公司_资产推介


methods = {
    'https://www.zsamc.com/index.php/infor/index/20.html#tabNav': get_zhejiangzheshang_chuzhigonggao,  # 浙江省浙商资产管理有限公司
    'https://www.zyamc.net/#/asset-zone/4': get_zhongyuanzichan_chuzhigonggao,  # 中原资产管理有限公司
    'https://www.utrustamc.com/czgg/list.aspx#SubMenu': guangdongzichan_chuzhigonggao,  # 广东粤财资产管理有限公司
    'http://www.mtamc.com.cn/zcxx/czgg/index_1.htm': fujiantouzi_chuzhigonggao,  # 福建闽投资产管理有限公司
    'http://www.scdamc.com/chuzhigonggao': sichuanfazhan_chuzhigonggao,  # 四川发展资产管理有限公司
    'https://crykasset.com/Assets/index.html': huarunyukang_chuzhigonggao,  # 华润渝康资产管理有限公司
    'https://hubeiamc.com/Asset_Disposal_Announcement.html': hubeizichan_chuzhigonggao,  # 湖北省资产管理有限公司
    'https://www.jxfamc.com/jxjrzc/chuzhigonggao/czgg.shtml': get_jiangxizichan_chuzhigonggao,  # 江西省金融资产管理股份有限公司
    'http://www.nbfamc.com/List.html?menuId=44': get_ningbozichan_chuzhigonggao,  # 宁波金融资产管理股份有限公司
    'https://www.sz-amc.com/business/Publicity?id=3': get_suzhouzichan_chuzhigonggao,  # 苏州资产管理有限公司
    'https://www.jsamc.com.cn/assets-promote/promote-information#处置公告': get_jiangsuzichan_chuzhigonggao,
    # 江苏资产管理有限公司
    'https://nxfamc.com/jyzx/blzcczyw1.htm': get_ningxiajinrong_chuzhigonggao,  # 宁夏金融资产管理有限公司
    'https://www.snfamc.com/news/notice': get_shanxijinrong_chuzhigonggao,  # 陕西金融资产管理股份有限公司
    'https://www.guangzhouamc.com/asset/chuzhigonggao.html': get_guangzhouzichan_chuzhigonggao,  # 广州资产管理有限公司
    'http://www.xiangjiang-amc.com/zcczgg/31617': get_changshaxiangjiang_chuzhigonggao,  # 长沙湘江资产管理有限公司
    'https://amc.hnchasing.com/cxamc/zcxx53/zcczgg79/index.html': get_hunancaixin_chuzhigonggao,  # 湖南省财信资产管理有限公司
    'http://www.henanamc.com.cn/czgg19': get_henanzichan_chuzhigonggao,  # 河南资产管理有限公司
    'http://www.qdamc.citic/announcement-54-1.html': get_zhongxinqingdao_chuzhigonggao,  # 中信青岛资产管理有限公司
    'http://www.ciamc.com.cn/ciamc/insetInfo/disposal-Notice.html': get_xinyezichan_chuzhigonggao,  # 兴业资产管理有限公司
    'https://www.amcah.com/new.php?class_id=102102': get_anhuizhongan_chuzhigonggao,  # 安徽省中安金融资产管理股份有限公司
    'https://www.cebamc.com/#/assets/list/0': get_guangdazichan_chuzhigonggao,  # 光大金瓯资产管理有限公司
    'http://srzcamc.com/index/lists/listss.html?type=258&t=237': get_jilinshengrong_chuzhigonggao,  # 吉林省盛融资产管理有限责任公司
    'https://www.ssaocorp.com/site/information_report': get_shanghaiguoyou_chuzhigonggao,  # 上海国有资产经营有限公司
    'https://www.amcim.com/cms/about/4.html': get_neimenggujinrong_chuzhigonggao,  # 内蒙古金融资产管理有限公司
    'https://www.hebamc.com/index.php/Cn/Info/index/classid/61.html': get_hebeiziguan_chuzhigonggao,  # 河北省资产管理有限公司
    'http://www.yndamc.com/list/cnPC/1/20/auto/12/0.html': get_yunnanzichan_chuzhigonggao,  # 云南省资产管理有限公司
    'http://www.hnlhzc.com/index.php?m=content&c=index&a=lists&catid=30': get_hainanzichan_chuzhigonggao,
    # 海南联合资产管理有限公司
    'https://www.szamc.net/home/zcDispose': get_shenzenzichan_chuzhigonggao,  # 深圳资产管理有限公司
    'https://www.cmamc.net.cn/zichan_ye.php?fid=8': get_shenzhenzhaoshang_chuzhigonggao,  # 深圳市招商平安资产管理有限责任公司
    'https://www.lnzcgs.cn/list_34': get_liaoningzichan_chuzhigonggao,  # 辽宁资产管理有限公司
    'http://www.gohoamc.com/info.php?class_id=102104': get_azhuiguohou_chuzhigonggao,  # 安徽国厚金融资产管理有限公司
    'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI5ODk2MTY1Mg==&action=getalbum&album_id=3421134606546747396#wechat_redirect': zhongxinjinrongjiangsu_gzh,  # 中国资产管理有限公司浙江分公司
    'https://mp.weixin.qq.com/mp/homepage?__biz=MzkyOTgxMzc2Mg==&hid=2&sn=5aa8306d099d37332ff2120bf985a6c8&scene=18#wechat_redirect': zhongxinjinrongguangdong_gzh,  # 中国资产管理有限公司广东分公司
    'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzkyNjY4NDEwNg==&action=getalbum&album_id=3465789407292817408#wechat_redirect': zhongxinjinrongzhejiang_gzh,  # 中国资产管理有限公司浙江分公司
    'https://www.jsamc.com.cn/assets-promote/promote-information' : get_jiangsuzichan_zichantuijie, # 江苏资产管理有限公司_资产推介
    'https://www.gwamcc.com/MCInfo.aspx?liName=101': get_zhongguochangchengzichan_zichanyingxiao,  # 中国长城资产管理股份有限公司_资产营销
    'https://www.zsamc.com/index.php/infor/index/21/0/1.html': get_zhejiangzheshang_zichantuijie,  # 浙江省浙商资产管理有限公司_资产推介
    'http://www.xiangjiang-amc.com/assetlist/31614': get_changshaxiangjiang_zichantuijie,  # 长沙湘江资产管理有限公司_资产推介
    'http://www.mtamc.com.cn/zcxx/tjxx/index_1.htm': fujiantouzi_tuijiexinxi,  # 福建闽投资产管理有限公司_资产推介
    'https://amc.hnchasing.com/cxamc/zcxx53/zctj1/index.html': get_hunancaixin_zichantuijie,  # 湖南省财信资产管理有限公司_资产推介
    'http://www.qdamc.citic/announcement-6-1.html': get_zhongxinqingdao_zichantuijie,  # 中信青岛资产管理有限公司_资产推介
    'https://www.guangzhouamc.com/asset/tuijiexinxi.html': get_guangzhouzichan_zichantuijie,    # 广州资产管理有限公司_资产推介
    'http://www.henanamc.com.cn/zctj145': get_henanzichan_zichantuijie,    # 河南资产管理有限公司_资产推介
    'http://www.scdamc.com/zhichantuijian': sichuanfazhan_zichantuijie,    # 四川省发展资产管理有限公司_资产推介
    'https://www.zyamc.net/#/asset-zone/1': get_zhongyuanzichan_zichantuijie,    # 中原资产管理有限公司_资产推介
    'http://www.ciamc.com.cn/ciamc/insetInfo/Refelral-Info.html': get_xinyezichan_zichantuijie,    # 兴业资产管理有限公司_资产推介
    'http://www.gohoamc.com/recommend.php?class_id=107': get_azhuiguohou_zichantuijie,  # 安徽国厚金融资产管理有限公司_资产推介
    'https://www.sz-amc.com/business/recommend': get_suzhouzichan_zichantuijie,   # 苏州资产管理有限公司_资产推介
    'https://www.jxfamc.com/jxjrzc/zichanzhanshi/zczs.shtml': get_jiangxizichan_zichanzhanshi,   # 江西省资产管理公司_资产展示
    'http://www.ruijingamc.com/#/available': get_jiangxiruijin_zichantuijie,   # 江西瑞京资产管理公司_资产推介
    'https://www.gramc.com.cn/case': get_heilongjiangguoruizichan_xiangmutuijie,    # 黑龙江国瑞资产管理有限公司_项目推介
    'http://www.yndamc.com/list/cnPC/1/18/auto/12/0.html': get_yunnanzichan_zichantuijie,   # 云南省资产管理有限公司_资产推介



}

web_list = [
    'https://www.zsamc.com/index.php/infor/index/20.html#tabNav',
    'https://www.zyamc.net/#/asset-zone/4',
    'https://www.utrustamc.com/czgg/list.aspx#SubMenu',
    'http://www.mtamc.com.cn/zcxx/czgg/index_1.htm',
    'http://www.scdamc.com/chuzhigonggao',
    'https://crykasset.com/Assets/index.html',
    'https://hubeiamc.com/Asset_Disposal_Announcement.html',
    'https://www.jxfamc.com/jxjrzc/chuzhigonggao/czgg.shtml',
    'http://www.nbfamc.com/List.html?menuId=44',
    'https://www.sz-amc.com/business/Publicity?id=3',
    'https://www.jsamc.com.cn/assets-promote/promote-information#处置公告',
    'https://nxfamc.com/jyzx/blzcczyw1.htm',
    'https://www.snfamc.com/news/notice',
    'https://www.guangzhouamc.com/asset/chuzhigonggao.html',
    'http://www.xiangjiang-amc.com/zcczgg/31617',
    'https://amc.hnchasing.com/cxamc/zcxx53/zcczgg79/index.html',
    'http://www.henanamc.com.cn/czgg19',
    'http://www.qdamc.citic/announcement-54-1.html',
    'http://www.ciamc.com.cn/ciamc/insetInfo/disposal-Notice.html',
    'https://www.amcah.com/new.php?class_id=102102',
    'https://www.cebamc.com/#/assets/list/0',
    'http://srzcamc.com/index/lists/listss.html?type=258&t=237',
    'https://www.ssaocorp.com/site/information_report',
    'https://www.amcim.com/cms/about/4.html',
    'https://www.hebamc.com/index.php/Cn/Info/index/classid/61.html',
    'http://www.yndamc.com/list/cnPC/1/20/auto/12/0.html',
    'http://www.hnlhzc.com/index.php?m=content&c=index&a=lists&catid=30',
    'https://www.szamc.net/home/zcDispose',
    'https://www.cmamc.net.cn/zichan_ye.php?fid=8',
    'https://www.lnzcgs.cn/list_34',
    'http://www.gohoamc.com/info.php?class_id=102104',
    'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI5ODk2MTY1Mg==&action=getalbum&album_id=3421134606546747396#wechat_redirect',
    'https://mp.weixin.qq.com/mp/homepage?__biz=MzkyOTgxMzc2Mg==&hid=2&sn=5aa8306d099d37332ff2120bf985a6c8&scene=18#wechat_redirect',
    'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzkyNjY4NDEwNg==&action=getalbum&album_id=3465789407292817408#wechat_redirect',
    'https://www.jsamc.com.cn/assets-promote/promote-information',
    'https://www.gwamcc.com/MCInfo.aspx?liName=101',
    'https://www.zsamc.com/index.php/infor/index/21/0/1.html',
    'http://www.xiangjiang-amc.com/assetlist/31614',
    'http://www.mtamc.com.cn/zcxx/tjxx/index_1.htm',
    'https://amc.hnchasing.com/cxamc/zcxx53/zctj1/index.html',
    'http://www.qdamc.citic/announcement-6-1.html',
    'https://www.guangzhouamc.com/asset/tuijiexinxi.html',
    'http://www.henanamc.com.cn/zctj145',
    'http://www.scdamc.com/zhichantuijian',
    'https://www.zyamc.net/#/asset-zone/1',
    'http://www.ciamc.com.cn/ciamc/insetInfo/Refelral-Info.html',
    'http://www.gohoamc.com/recommend.php?class_id=107',
    'https://www.sz-amc.com/business/recommend',
    'https://www.jxfamc.com/jxjrzc/zichanzhanshi/zczs.shtml',
    'http://www.ruijingamc.com/#/available',
    'https://www.gramc.com.cn/case',
    'http://www.yndamc.com/list/cnPC/1/18/auto/12/0.html',
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

