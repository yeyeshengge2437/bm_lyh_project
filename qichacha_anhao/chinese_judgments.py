import re
import time
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions
keywords = {'合同(16597031)': 'j3_1_anchor', '利息(12711172)': 'j3_2_anchor', '利率(8555720)': 'j3_3_anchor', '合同约定(6034126)': 'j3_4_anchor', '民间借贷(5229861)': 'j3_5_anchor', '违约金(5085610)': 'j3_6_anchor', '强制性规定(5081365)': 'j3_7_anchor', '贷款(4684733)': 'j3_8_anchor', '驳回(4678366)': 'j3_9_anchor', '返还(4427705)': 'j3_10_anchor', '债权(4313797)': 'j3_11_anchor', '清偿(3839530)': 'j3_12_anchor', '交通事故(3760444)': 'j3_13_anchor', '担保(3635440)': 'j3_14_anchor', '借款合同(3521069)': 'j3_15_anchor', '鉴定(3307974)': 'j3_16_anchor', '处分(3289859)': 'j3_17_anchor', '给付(3259319)': 'j3_18_anchor', '交付(3020619)': 'j3_19_anchor', '违约责任(3003848)': 'j3_20_anchor', '合(2936891)': 'j3_21_anchor', '误工费(2646884)': 'j3_22_anchor', '人身损害赔偿(2644991)': 'j3_23_anchor', '保证(2596050)': 'j3_24_anchor', '买卖合同(2519359)': 'j3_25_anchor', '传票(2441219)': 'j3_26_anchor', '传唤(2304810)': 'j3_27_anchor', '赔偿责任(2259919)': 'j3_28_anchor', '缺席判决(2093009)': 'j3_29_anchor', '第三人(1977966)': 'j3_30_anchor', '变更(1960648)': 'j3_31_anchor', '债务人(1931448)': 'j3_32_anchor', '减刑(1926228)': 'j3_33_anchor', '程序合法(1880352)': 'j3_34_anchor', '查封(1839532)': 'j3_35_anchor'}
brief = {'刑事案由(11121958)': '1_anchor', '民事案由(97741866)': '9000_anchor', '执行案由(29521896)': '3200_anchor', '国家赔偿案由(41912)': '2100_anchor', '行政案由(3149009)': 'xzay_anchor'}
court_level = {'最高法院(131001)': 'j7_1_anchor', '高级法院(1538386)': 'j7_2_anchor', '中级法院(17171593)': 'j7_3_anchor', '基层法院(132009266)': 'j7_4_anchor'}
territory_courts = {'最高人民法院(131001)': '0_anchor', '北京市(4378567)': '100_anchor', '天津市(2155885)': '200_anchor', '河北省(5792873)': '300_anchor', '山西省(2354491)': '400_anchor', '内蒙古自治区(3216589)': '500_anchor', '辽宁省(7451122)': '600_anchor', '吉林省(4133188)': '700_anchor', '黑龙江省(3765646)': '800_anchor', '上海市(4995994)': '900_anchor', '江苏省(9153267)': 'A00_anchor', '浙江省(9958904)': 'B00_anchor', '安徽省(6929140)': 'C00_anchor', '福建省(4795121)': 'D00_anchor', '江西省(3340943)': 'E00_anchor', '山东省(11559713)': 'F00_anchor', '河南省(10114862)': 'G00_anchor', '湖北省(4877621)': 'H00_anchor', '湖南省(6711947)': 'I00_anchor', '广东省(10468876)': 'J00_anchor', '广西壮族自治区(3730525)': 'K00_anchor', '海南省(510805)': 'L00_anchor', '重庆市(4104263)': 'M00_anchor', '四川省(7645584)': 'N00_anchor', '贵州省(2789377)': 'O00_anchor', '云南省(4312593)': 'P00_anchor', '西藏自治区(131041)': 'Q00_anchor', '陕西省(5193976)': 'R00_anchor', '甘肃省(2135679)': 'S00_anchor', '青海省(718374)': 'T00_anchor', '宁夏回族自治区(1130907)': 'U00_anchor', '新疆维吾尔自治区(1914520)': 'V00_anchor', '新疆维吾尔自治区高级人民法院生产建设兵团分院(246813)': 'X00_anchor'}
year_of_referee = {'2024(4206219)': 'j9_1_anchor', '2023(6561053)': 'j9_2_anchor', '2022(9462612)': 'j9_3_anchor', '2021(16797948)': 'j9_4_anchor', '2020(23365657)': 'j9_5_anchor', '2019(23036417)': 'j9_6_anchor', '2018(19335829)': 'j9_7_anchor', '2017(16722493)': 'j9_8_anchor', '2016(12536219)': 'j9_9_anchor', '2015(9727312)': 'j9_10_anchor', '2014(6919678)': 'j9_11_anchor', '2013(1423451)': 'j9_12_anchor', '2012(412326)': 'j9_13_anchor', '2011(219333)': 'j9_14_anchor', '2010(197100)': 'j9_15_anchor', '2009(97415)': 'j9_16_anchor', '2008(27484)': 'j9_17_anchor', '2007(14871)': 'j9_18_anchor', '2006(7649)': 'j9_19_anchor', '2005(5780)': 'j9_20_anchor', '2004(4517)': 'j9_21_anchor', '2003(2678)': 'j9_22_anchor', '2002(3476)': 'j9_23_anchor', '2001(1332)': 'j9_24_anchor', '2000(407)': 'j9_25_anchor', '1998(100)': 'j9_26_anchor', '1997(90)': 'j9_27_anchor'}
adjudication_procedure = {'管辖案件(733754)': '01_anchor', '刑事案件(10365047)': '02_anchor', '民事案件(92711178)': '03_anchor', '行政案件(3142754)': '04_anchor', '国家赔偿与司法救助案件(142921)': '05_anchor', '区际司法协助案件(94)': '06_anchor', '国际司法协助案件(622)': '07_anchor', '司法制裁案件(10055)': '08_anchor', '非诉保全审查案件(464189)': '09_anchor', '执行案件(43422942)': '10_anchor', '强制清算与破产案件(122413)': '11_anchor', '其他案件(35010)': '99_anchor'}
type_of_instrument = {'判决书(50521089)': 'j4_1_anchor', '裁定书(75798536)': 'j4_2_anchor', '调解书(12608788)': 'j4_3_anchor', '决定书(788555)': 'j4_4_anchor', '通知书(8326370)': 'j4_5_anchor', '令(331575)': 'j4_6_anchor', '其他(2778701)': 'j4_7_anchor'}


co = ChromiumOptions()
co = co.set_user_data_path(r'D:\chome_data\data_one')
co.set_paths(local_port=9136)

page = ChromiumPage()
tab = page.get_tab()
# 访问网页
tab.get('https://account.court.gov.cn/app?back_url=https%3A%2F%2Faccount.court.gov.cn%2Foauth%2Fauthorize%3Fresponse_type%3Dcode%26client_id%3Dzgcpwsw%26redirect_uri%3Dhttps%253A%252F%252Fwenshu.court.gov.cn%252FCallBackController%252FauthorizeCallBack%26state%3D421fc4a4-5cc2-4ecd-bb44-257b1a17ee98%26timestamp%3D1732779592364%26signature%3DA4C212AFA550EFA5E27D9A3E094A741A7A14BCE6873A632A4CF587CF76474838%26scope%3Duserinfo#/login')
# print(tab.html)
time.sleep(3)

login = tab.ele("@class=phone-number-input",).input('15938554242', by_js=True)
time.sleep(2)
# login.click(by_js=True)
# login
password = tab.ele("@class=password",).input('Liyongheng10!', by_js=True)
time.sleep(2)
# password.click(by_js=True)
# password
tab.ele("@class=button button-primary").click(by_js=True)
time.sleep(8)
tab.refresh()
tab.ele("@class=search-rightBtn search-click").click(by_js=True)
time.sleep(2)
tab.ele("@class=search-rightBtn search-click").click(by_js=True)
tab.ele("@id=j3_1_anchor").click(by_js=True)
time.sleep(2)
num = tab.ele('xpath=//*[@id="_view_1545184311000"]/div[1]/div[2]/span').text
print(num)

input()
page.quit()




