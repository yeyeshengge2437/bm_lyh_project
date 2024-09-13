import re


text = """云南省资产管理有限公司拥有云南明磊实业有限公司等143户不良金融债权，截止基准日债权本金
2,108,931,921.74
元，具体债权利息、罚息、复利、违约金金额以相关合同或司法裁判为准。现公告要求公告清单中所列包括但不限于借款人、担保人及其清算义务人等其他相关当事人，从公告之日起7日内向云南省资产管理有限公司履行主债权合同及担保合间约定的还本付息义务或相应的担保责任（若借款人、担保人因各种原因发生更名、改制、歇业、吊销营业执照或丧失民事主体资格等情形，请相关承债主体、清算主体代为履行义务或承担清算责任），逾期未清偿的，我公司将依法对上述债权进行处置，现予以公告。
 一、债权资产情况
 债权资产情况请登陆云南省资产管理有限公司网站（http://www.yndamc.com/）&rarr;找到“资产信息”栏目&rarr;点击“债权处置公告”即可查询。（详见下表）
 二、交易条件及交易对象要求
 对交易条件的要求：要求买受人信誉良好，原则上一次性支付转让价款，资金来源合法并可承担购买债权所带来的风险。
对交易对象的要求为：具有完全民事行为能力、支付能力的法人、组织或自然人。下列人员不得受让该资产：对应债权的债务人、担保人，国家公务员、金融监管机构工作人员、政法干警、资产管理公司工作人员、国有企业债务人管理层人员以及参与资产处置工作的律师、会计师、评估师等中介机构人员等关联人。
 三、处置方式及公告期
整体组包、部分组包或单户处置，具体情况投资者可登陆云南省资产管理有限公司网站（http://www.yndamc.com/）或与资产公司有关部门接洽查询。
 处置公告期限自本公告发布之日起一年内有效。
 公告期内受理上述资产处置有关异议和咨询。
 四、联系方式
 受理公示事项联系人：李女士，联系电话：
0871-67129813
 受理排斥、阻挠征询或异议联系人：董女士，联系电话：0871-65376159
 特别说明：本公告内容如有错漏，以借款人、担保人等原已签署的交易合同及相关法律文件约定为准。
 
    云南省资产管理有限公司
    2023年9月11日
.b1{white-space-collapsing:preserve;}
.b2{margin: 1.0in 1.25in 1.0in 1.25in;}
.s1{color:#333333;}
.s2{color:#262626;}
.s3{font-size:14pt;color:#262626;}
.p1{text-align:center;hyphenate:auto;font-family:方正小标宋简体;font-size:22pt;}
.p2{text-indent:0.44444445in;text-align:start;hyphenate:auto;font-family:方正仿宋简体;font-size:16pt;}
.p3{text-indent:0.44444445in;text-align:start;hyphenate:auto;font-family:方正黑体简体;font-size:16pt;}
.p4{text-indent:0.44444445in;text-align:end;hyphenate:auto;font-family:方正仿宋简体;font-size:16pt;}
.p5{text-indent:0.44444445in;text-align:justify;hyphenate:auto;font-family:方正仿宋简体;font-size:16pt;}"""

pattern = r'\.*[^{]*\{.*?\}'

# 使用 re.sub() 替换匹配的内容为空字符串
cleaned_text = re.sub(r'\.[bsp][^{]*\{.*?\}', '', text, flags=re.MULTILINE)

print(cleaned_text)