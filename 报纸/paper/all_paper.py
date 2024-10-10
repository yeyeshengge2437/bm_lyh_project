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
from tulufan_paper import get_tulufan_paper  # 吐鲁番日报
from kezile_paper import get_kezile_paper  # 克孜勒苏日报
from boerta_paper import get_boerta_paper  # 博尔塔拉报
from tacheng_paper import get_tacheng_paper  # 塔城日报
from changji_paper import get_changji_paper  # 昌吉日报
from yili_paper import get_yili_paper  # 伊犁日报
from azletai_paper import get_aletai_paper  # 阿勒泰日报
from chaidamu_paper import get_chaidamu_paper  # 柴达木日报
from guoluo_paper import get_guoluo_paper  # 果洛报
from nanhuang_paper import get_nanhuang_paper  # 黄南报
from haidong_paper import get_haidong_paper  # 海东日报
from lanzhouxinqu_paper import get_lanzhouxinqu_paper  # 兰州新区报
from lanzhou_paper import get_lanzhou_paper  # 兰州日报
from xian_paper import get_xian_paper  # 西安日报
from nanshaxinqu_paper import get_nanshaxiqu_paper  # 南沙新区报
from chaozhou_paper import get_chaozhou_paper  # 潮州日报
from changsha_lastpaper import get_changsha_lastpaper  # 长沙晚报
from zhangjiajie_paper import get_zhangjiajie_lastpaper  # 张家界日报
from changde_paper import get_changde_paper  # 常德日报
from yiyang_paper import get_yiyang_paper  # 益阳日报
from minnan_paper import get_minnan_paper  # 闽南日报
from taizhou_lastpaper import get_taizhou_lastpaper  # 泰州晚报
from taizhou_paper import get_taizhou_paper  # 泰州日报
from azqing_paper import get_anqing_paper  # 安庆日报
from taigu_paper import get_taigu_paper  # 太谷报
from chinarenshizuzhi_paper import get_chinarenshizuzhi_paper  # 组织人事报
from azhuinongcun_paper import get_anhuinongcun_paper  # 安徽日报.农村版
from beifangshucai_paper import get_beifangshucai_paper  # 北方蔬菜报
from shouguang_paper import get_shouguang_paper  # 寿光日报
from shichangxinxi_paper import get_shichangxinxi_paper  # 市场信息报
from dongfangchengxiang_paper import get_dongfangchengxiang_paper  # 东方城乡报
from guangdongkeji_paper import get_guangdongkeji_paper  # 广东科技报
from wuhankeji_paper import get_wuhankeji_paper  # 武汉科技报
from kexuedao_paper import get_kexuedao_paper  # 科学导报
from kepushi_paper import get_kepushi_paper  # 科普时报
from yinchuan_paper import get_yinchuan_paper  # 银川日报
from yinchuan_lastpaper import get_yinchuan_lastpaper  # 银川晚报
from xizangshang_paper import get_xizangshang_paper  # 西藏商报
from chuncheng_lastpaper import get_chuncheng_lastpaper  # 春城晚报
from xihaidushi_paper import get_xihaidushi_paper  # 西海都市报
from xining_lastpaper import get_xining_lastpaper  # 西宁晚报
from lanzhouchen_paper import get_lanzhouchen_paper  # 兰州晨报
from lanzhou_lastpaper import get_lanzhou_lastpaper  # 兰州晚报
from xian_lastpaper import get_xian_lastpaper  # 西安晚报
from xiaoxiangchen_paper import get_xiaoxiangchen_paper  # 潇湘晨报
from yueyang_paper import get_yueyang_paper  # 岳阳日报
from zhengzhou_lastpaper import get_zhengzhou_lastpaper  # 郑州晚报
from qianjiang_lastpaper import get_qianjiang_lastpaper  # 钱江晚报
from lianyungang_paper import get_lianyungang_paper  # 连云港日报
from wuxi_paper import get_wuxi_paper  # 无锡日报
from jiangnan_lastpaper import get_jiangnan_lastpaper  # 江南晚报
from yangzi_lastpaper import get_yangzi_lastpaper  # 扬子晚报
from binzhou_paper import get_binzhou_paper  # 滨州日报
from fuzhou_paper import get_fuzhou_paper  # 福州日报
from fuzhou_lastpaper import get_fuzhou_lastpaper  # 福州晚报
from zhaotong_paper import get_zhaotong_paper  # 昭通日报
from langfang_paper import get_langfang_paper  # 廊坊日报
from langfangdushi_paper import get_langfangdushi_paper  # 廊坊都市报
from jiatingyushenghuo_paper import get_jiatingyuyisheng_paper  # 家庭与生活报
from nanchong_paper import get_nanchong_paper  # 南充日报
from luoyang_lastpaper import get_luoyang_lastpaper  # 洛阳晚报
from qinzhou_paper import get_qinzhou_paper  # 钦州日报
from zhengzhou_paper import get_zhengzhou_paper  # 郑州日报
from jianghuaichen_paper import get_jianghuaichen_paper  # 江淮晨报
from dajiang_lastpaper import get_dajiang_lastpaper  # 大江晚报
from wuhu_paper import get_wuhu_paper  # 芜湖日报
from hefei_lastpaper import get_hefei_lastpaper  # 合肥晚报
from hefei_paper import get_hefei_paper  # 合肥日报
from qingniaozao_paper import get_qingniaozao_paper  # 青鸟早报
from zhihuishenghuo_paper import get_zhihuishenghuo_paper  # 智慧生活报
from shijiazhuang_paper import get_shijiazhuang_paper  # 石家庄日报
from hebeiqingnian_paper import get_hebeiqingnian_paper  # 河北青年报
from yanzhao_lastpaper import get_yanzhao_lastpaper  # 燕赵晚报
from yanzhaodushi_paper import get_yanzhaodushi_paper  # 燕赵都市报
from bandaochen_paper import get_bandaochen_paper  # 半岛晨报
from xinmin_lastpaper import get_xinmin_lastpaper  # 新民晚报
from beijing_lastpaper import get_beijing_lastpaper  # 北京晚报
from xinanshang_paper import get_xinanshang_paper  # 西南商报
from changjiangshang_paper import get_changjiangshang_paper  # 长江商报
from henanjingji_paper import get_henanjingji_paper  # 河南经济报
from pudongshi_paper import get_pudongshi_paper  # 浦东时报
from diyicaijing_paper import get_diyicaijing_paper  # 第一财经日报
from qiyeguancha_paper import get_qiyeguancha_paper  # 企业观察报
from chinagaige_paper import get_chinagaige_paper  # 中国改革报
from gansunongmin_paper import get_gansunongmin_paper  # 甘肃农民报
from azhui_paper import get_anhui_paper  # 安徽日报
from minzushi_paper import get_minzushi_paper  # 民族时报
from fazhishi_paper import get_fazhishi_paper  # 法治时报
from xizangfazhi_paper import get_xizangfazhi_paper  # 西藏法制报
from zhishibolanguofang_paper import get_zhishibolanguofang_paper  # 知识博览报.国防教育周刊
from haisishang_paper import get_haisishang_paper  # 海丝商报
from shishi_paper import get_shishi_paper  # 石狮日报
from jingshenwenming_paper import get_jingshenwenming_paper  # 精神文明报
from jilinnongcun_paper import get_jilinnongcun_paper  # 吉林农村报
from xuexishi_paper import get_xuexishi_paper  # 学习时报
from yantai_paper import get_yantai_paper  # 烟台日报
from jingjicankao_paper import get_jingjicankao_paper  # 经济参考报
from tengzhou_paper import get_tengzhou_paper  # 滕州日报
from linanminzu_paper import get_linanminzu_paper  # 临夏民族日报
from lianhe_paper import get_lianhe_paper  # 联合日报
from renminzhengxie_paper import get_renminzhengxie_paper  # 人民政协报
from xizang_paper import get_xizang_paper  # 西藏日报
from kashi_paper import get_kashi_paper  # 喀什日报
from guangming_paper import get_guangming_paper  # 光明日报
from minzhuyufazhi_paper import get_minzhuyufazhi_paper  # 民主与法制时报 ------------------------（以下为没有高清图片和pdf的报纸）
from shanxi_paper import get_shanxi_paper  # 山西日报
from chinaxumushou_paper import get_chinaxumushou_paper  # 中国畜牧兽医报
from shenghuore_paper import get_shenghuore_paper  # 生活日报
from huaxiazao_paper import get_huaxiazao_paper  # 华夏早报
from gejiedao_paper import get_gejiedao_paper  # 各界导报
from meireshang_paper import get_meireshang_paper  # 每日商报
from xinxishi_paper import get_xinxishi_paper  # 信息时报
from nanfangnongcun_paper import get_nanfangnongcun_paper  # 南方农村报
from chinaqingnian_paper import get_chinaqingnian_paper  # 中国青年报
from jinan_paper import get_jinan_paper  # 济南日报
from yilikenqu_paper import get_yilikenqu_paper  # 伊犁垦区报
from shantou_paper import get_shantou_paper  # 汕头日报
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
    '吐鲁番日报': get_tulufan_paper,
    '克孜勒苏日报': get_kezile_paper,
    '博尔塔拉报': get_boerta_paper,
    '塔城日报': get_tacheng_paper,
    '昌吉日报': get_changji_paper,
    '伊犁日报': get_yili_paper,
    '阿勒泰日报': get_aletai_paper,
    '柴达木日报': get_chaidamu_paper,
    '果洛报': get_guoluo_paper,
    '黄南报': get_nanhuang_paper,
    '海东日报': get_haidong_paper,
    '兰州新区报': get_lanzhouxinqu_paper,
    '兰州日报': get_lanzhou_paper,
    '西安日报': get_xian_paper,
    '南沙新区报': get_nanshaxiqu_paper,
    '潮州日报': get_chaozhou_paper,
    '长沙晚报': get_changsha_lastpaper,
    '张家界日报': get_zhangjiajie_lastpaper,
    '常德日报': get_changde_paper,
    '益阳日报': get_yiyang_paper,
    '闽南日报': get_minnan_paper,
    '泰州晚报': get_taizhou_lastpaper,
    '泰州日报': get_taizhou_paper,
    '安庆日报': get_anqing_paper,
    '太谷报': get_taigu_paper,
    '组织人事报': get_chinarenshizuzhi_paper,
    '安徽日报.农村版': get_anhuinongcun_paper,
    '北方蔬菜报': get_beifangshucai_paper,
    '寿光日报': get_shouguang_paper,
    '市场信息报': get_shichangxinxi_paper,
    '东方城乡报': get_dongfangchengxiang_paper,
    '广东科技报': get_guangdongkeji_paper,
    '武汉科技报': get_wuhankeji_paper,
    '科学导报': get_kexuedao_paper,
    '科普时报': get_kepushi_paper,
    '银川日报': get_yinchuan_paper,
    '银川晚报': get_yinchuan_lastpaper,
    '西藏商报': get_xizangshang_paper,
    '春城晚报': get_chuncheng_lastpaper,
    '西海都市报': get_xihaidushi_paper,
    '西宁晚报': get_xining_lastpaper,
    '兰州晨报': get_lanzhouchen_paper,
    '兰州晚报': get_lanzhou_lastpaper,
    '西安晚报': get_xian_lastpaper,
    '潇湘晨报': get_xiaoxiangchen_paper,
    '岳阳日报': get_yueyang_paper,
    '郑州晚报': get_zhengzhou_lastpaper,
    '钱江晚报': get_qianjiang_lastpaper,
    '连云港日报': get_lianyungang_paper,
    '无锡日报': get_wuxi_paper,
    '江南晚报': get_jiangnan_lastpaper,
    '扬子晚报': get_yangzi_lastpaper,
    '滨州日报': get_binzhou_paper,
    '福州日报': get_fuzhou_paper,
    '福州晚报': get_fuzhou_lastpaper,
    '昭通日报': get_zhaotong_paper,
    '廊坊日报': get_langfang_paper,
    '廊坊都市报': get_langfangdushi_paper,
    '家庭与生活报': get_jiatingyuyisheng_paper,
    '南充日报': get_nanchong_paper,
    '洛阳晚报': get_luoyang_lastpaper,
    '钦州日报': get_qinzhou_paper,
    '郑州日报': get_zhengzhou_paper,
    '江淮晨报': get_jianghuaichen_paper,
    '大江晚报': get_dajiang_lastpaper,
    '芜湖日报': get_wuhu_paper,
    '合肥晚报': get_hefei_lastpaper,
    '合肥日报': get_hefei_paper,
    '青鸟早报': get_qingniaozao_paper,
    '智慧生活报': get_zhihuishenghuo_paper,
    '石家庄日报': get_shijiazhuang_paper,
    '河北青年报': get_hebeiqingnian_paper,
    '燕赵晚报': get_yanzhao_lastpaper,
    '燕赵都市报': get_yanzhaodushi_paper,
    '半岛晨报': get_bandaochen_paper,
    '新民晚报': get_xinmin_lastpaper,
    '北京晚报': get_beijing_lastpaper,
    '西南商报': get_xinanshang_paper,
    '长江商报': get_changjiangshang_paper,
    '河南经济报': get_henanjingji_paper,
    '浦东时报': get_pudongshi_paper,
    '第一财经日报': get_diyicaijing_paper,
    '企业观察报': get_qiyeguancha_paper,
    '中国改革报': get_chinagaige_paper,
    '甘肃农民报': get_gansunongmin_paper,
    '安徽日报': get_anhui_paper,
    '民族时报': get_minzushi_paper,
    '法治时报': get_fazhishi_paper,
    '西藏法制报': get_xizangfazhi_paper,
    '知识博览报.国防教育周刊': get_zhishibolanguofang_paper,
    '海丝商报': get_haisishang_paper,
    '石狮日报': get_shishi_paper,
    '精神文明报': get_jingshenwenming_paper,
    '吉林农村报': get_jilinnongcun_paper,
    '学习时报': get_xuexishi_paper,
    '烟台日报': get_yantai_paper,
    '经济参考报': get_jingjicankao_paper,
    '滕州日报': get_tengzhou_paper,
    '临夏民族日报': get_linanminzu_paper,
    '联合日报': get_lianhe_paper,
    '人民政协报': get_renminzhengxie_paper,
    '西藏日报': get_xizang_paper,
    '喀什日报': get_kashi_paper,
    '光明日报': get_guangming_paper,
    '民主与法制时报': get_minzhuyufazhi_paper,
    '山西日报': get_shanxi_paper,
    '中国畜牧兽医报': get_chinaxumushou_paper,
    '生活日报': get_shenghuore_paper,
    '华夏早报': get_huaxiazao_paper,
    '各界导报': get_gejiedao_paper,
    '每日商报': get_meireshang_paper,
    '信息时报': get_xinxishi_paper,
    '南方农村报': get_nanfangnongcun_paper,
    '中国青年报': get_chinaqingnian_paper,
    '济南日报': get_jinan_paper,
    '伊犁垦区报': get_yilikenqu_paper,
    '汕头日报': get_shantou_paper,
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
    'http://appepaper.tlfw.net:8080/epaper/cn-pc/tlfrb',
    'https://www.xepaper.com/kz/html',
    'http://szb.tcxw.cc/pc/layout',
    'http://pcepaper.cjxww.cn',
    'https://www.ylxw.com.cn/epaper/ylrb',
    'https://alt-szb.xjmty.com',
    'https://www.cdmrb.com.cn',  # 未开始处理
    'http://files.eguoluo.com',
    'http://hnb.huangnan.gov.cn',
    'http://epaper.dbcsq.com',
    'https://szb.gansudaily.com.cn/lzxqb',
    'https://lzrb.lzbs.com.cn',
    'https://epaper.xiancn.com/newxarb',
    'https://www.cnepaper.com/nsxqb',
    'http://www.chaozhoudaily.com/upload/czrb/html',
    'https://www.icswb.com/default.php?mod=newspaper&a=gen_one&channel_id=15',
    'http://paper.zjjnews.cn:8081/zjjrbpc/layout',
    'http://rb.cdyee.com',
    'https://epaper.yyrb.cn',
    'http://zzxww.com',
    'http://sz.tznews.cn/tzwb/pc/layout',
    'http://sz.tznews.cn/tzrb/pc/layout',
    'http://aqdzb.aqnews.com.cn/epaper/read.do',
    'https://www.tgxcw.gov.cn/tgblink',
    'https://www.zuzhirenshi.com/newspaper/index',
    'https://szb.ahnews.com.cn/ncb/pad/layout',
    'https://szb.sgnet.cc/sgrb/bfscb/pc/layout',
    'https://szb.sgnet.cc/sgrb/sgrb/pc/layout',
    'http://sz.scxxb.com.cn',
    'https://www.dfcxb.com',
    'https://epaper.gdkjb.com/epaper/index.html',
    'http://kj.kexing100.com',
    'http://www.kxdb.com/dzbk/list.php?catid=33',
    'https://digitalpaper.stdaily.com/http_www.kjrb.com/kjwzb/html',
    'https://szb.ycfbapp.com',
    'https://szb.ycfbapp.com/ycwb/pc/layout',
    'http://e.xzxw.com/xzsb',
    'https://ccwb.yunnan.cn',
    'https://epaper.tibet3.com/xhdsb',
    'http://www.xnwbw.com',
    'http://lzcbszb.benliuxinwen.com',
    'https://lzwb.lzbs.com.cn',
    'http://epaper.xiancn.com/newxawb',
    'http://epaper.xxcb.cn/xxcba',
    'https://papers.803.com.cn/yyrb',
    'https://zzwb.zynews.cn/html',
    'http://qjwb.thehour.cn',
    'http://lygrbepaper.lygfb.cn',
    'http://szb.wxrb.com',
    'http://szb.wxrb.com/jnwb/pc/layout',
    'https://epaper.yzwb.net/pc/layout',
    'http://paper.bzrb.net/bzrb',
    'https://mag.fznews.com.cn',
    'https://mag.fznews.com.cn/fzwb',
    'https://dubao.ztnews.net',
    'http://epaper.lfcmw.com/rbpaper/pc/layout',
    'http://epaper.lfcmw.com/dsbpaper/pc/layout',
    'https://homelife.scol.com.cn',
    'http://xncrb.cnncw.cn',
    'https://lywb.lyd.com.cn',
    'https://qzrb.gxqzxw.com',
    'https://zzrb.zynews.cn',
    'https://newspaper.hf365.com/jhcb/pc/layout',
    'https://epaper.wuhunews.cn/pc/djwb/layout',
    'https://epaper.wuhunews.cn/pc/whrb/layout',
    'https://newspaper.hf365.com/hfwb/pc/layout',
    'https://newspaper.hf365.com/hfrb/pc/layout',
    'https://epaper.qingdaonews.com/qdzb',
    'http://shcb.x-publish.com',
    'http://sjzrb.sjzdaily.com.cn/sjzrbpaper/pc/layout',
    'https://www.hbynet.net/html/heqing/daohang/dianzibao/index.html',
    'http://yzwb.sjzdaily.com.cn/yzwbpaper/pc/layout',
    'https://yzdsb.hebnews.cn/pc/paper/layout',
    'http://www.bdcb.cn',
    'https://paper.xinmin.cn',
    'https://bjrbdzb.bjd.com.cn/bjwb',
    'http://www.xnsbdzb.com/xnsb',
    'http://www.changjiangtimes.com/szb',
    'https://dzb.zyjjw.cn',
    'http://www.pdtimes.com.cn',
    'https://www.yicai.com/epaper/pc',
    'http://baozhi.cneo.com.cn',
    'http://www.cfgw.net.cn/epaper',
    'https://szb.gansudaily.com.cn/gsnmb',
    'https://szb.ahnews.com.cn/ahrb/layout',
    'https://mzsb.yunnan.cn',
    'https://szb.hnfazhi.com',
    'https://e.xzxw.com/fzb',
    'https://www.icswb.com/default.php?mod=newspaper&a=gen_one&channel_id=101058',
    'https://hssb.fjdaily.com/pc/col',
    'https://ssrb.fjdaily.com/pc/col',
    'https://www.jswmb.cn',
    'http://www.jlncb.cn/jlncb/pc/paper/layout',
    'https://paper.cntheory.com/html',
    'https://www.shm.com.cn/szb/ytrb/paper/pc/layout',
    'http://dz.jjckb.cn/www/pages',
    'https://www.tzdaily.com.cn',
    'http://szb.chinalxnet.com/pc/layout',
    'https://app.lhwww.com.cn/dzb',
    'http://dzb.rmzxb.com.cn/rmzxbPaper/pc/layout',
    'http://www.jjckb.cn/www/pages',
    'https://e.xzxw.com/xzrb',
    'http://www.zgkashi.com/yw/sp',
    'https://epaper.gmw.cn/gmrb',
    'http://e.mzyfz.com/paper',
    'http://epaper.sxrb.com',
    'https://news.183read.cc',
    'https://shrb.qlwb.com.cn/shrb',
    'http://epaper.cmnpnews.com/index.Asp?Nid=366',
    'http://paper.gjnews.cn',
    'https://hzdaily.hangzhou.com.cn/mrsb',
    'https://epaper.xxsb.com',
    'https://epaper.nfncb.cn',
    'https://zqb.cyol.com',
    'http://jnrb.e23.cn/jnrb',
    'http://www.ylkqbs.com',
    'https://strb.dahuawang.com',
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
