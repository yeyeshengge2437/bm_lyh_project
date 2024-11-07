# 非流式模式
import requests
import revTongYi.qianwen as qwen
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co = co.set_paths(local_port=9260)
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错


def get_paper_url_cookies(url):
    cookie_dict = {}
    page = ChromiumPage(co)
    page.get(url)
    value_cookies = page.cookies()
    for key in value_cookies:
        cookie_dict[key['name']] = key['value']
    page.close()
    return cookie_dict


# question = "人工智能将对人类社会发展产生什么影响？"

chatbot = qwen.Chatbot(
    cookies={
        't': 'e0acaebb166d9505f6a7ee139e4b5bee',
        'tongyi_guest_ticket': 'zCajvWmFjGRmu6RQ53c2yDcQuUoyW8m8_7$ESqoH_Wg2OME_a8NE70ngPgOukbJ10SAVvzpwqLOf0',
        'cna': 'pFZ6HzCgYhkCAXPBuY12ZCZW',
        'login_aliyunid_pk': '1470918197645622',
        'login_current_pk': '1470918197645622',
        'aliyun_lang': 'zh',
        'currentRegionId': 'cn-hangzhou',
        'yunpk': '1470918197645622',
        'tongyi_sso_ticket': 'ggywxDKTdSsxMgJm2FHs2YXjpz7K_1vawU*obaGzpf8Gz1g_BynogsOH1apRX0qcdzyjCz$o1Bq30',
        '_samesite_flag_': 'true',
        'login_aliyunid': '"aliyun991744****"',
        'login_aliyunid_ticket': 'pof_BNTwUhTOoNC1ZBeeMfKJzxdnb95hYssNIZor6q7SCxRtgmGCbifG2Cd4ZWazmBdHI6sgXZqg4XFWQfyKpeu*0vCmV8s*MT5tJl3_1$$wSXWL5uW5ewJqixe2WUYw03YgaUx0iM*J9igVGFEZNQ4_0',
        'login_aliyunid_csrf': '_csrf_tk_1719330864285109',
        'hssid': '87267cc5-0a62-4fd6-93cc-5ae3ad6732a2',
        'hsite': '6',
        'aliyun_country': 'CN',
        'aliyun_site': 'CN',
        'sca': '2564fa69',
        'XSRF-TOKEN': '2bcbef9b-98ed-4e29-bdf2-da156f1b50a0',
        'cnaui': '1729148518832318489',
        'aui': '1729148518832318489',
        'cookie2': '1e96af10fbda726869eaf2adb4e2450a',
        '_tb_token_': '5aebb3856ba59',
        'atpsida': 'b6ad89de239fed61d14d1c55_1730970882_1',
        'tfstk': 'fsQ-3YDIA-2kCFlxDDZDK4k_qzN0SwCzGT5s-pvoAtBA_t-hE0jlk66hT4vHrHACD9XfZbAltipdhtp5KuRHJMBh3HjkP9XKpTXDFeYlryIpHTgHqwCEJB1CL7J3aofPae8QIRvLS_5yi4qxf-YQOss_x_FzSPfPNe8QIR4GrS3e7n9BR3tCGs92tDTIV99XcCOiFe6BRSCX3BTBd9TINgZvL09iJMbSmy-VnK3IJfRJVdawH2gCkQHMC_ZZR2_vw3Q3KAG-G3jC_h7lty32r1IXlBQU1DppXM_klawb5n-CAGxdmYNlC9CfLUbbO091qTYfPGhIRsLJHHAJ4YevCa5f7Et055CfuTfPk6cQRIXMh_7WJPNwyU9WkI73349dcM_k4ek7pp7AGasd4w7GWfqEIE9r2SFxYD-WgOwOgownTSkHMdVDZDoeDoRvISFxYD-WgIpgiYmEYnEV.',
        'isg': 'BPr6EfReSVmlmsTD_VRl-UtXSyAcq36FqawwygTzpg1Y95ox7DvOlcAVRYMr_PYd',
    }

)


# print(chatbot.ask(prompt="人工智能将对人类社会发展产生什么影响？"))

count = 0
def qwen_file_free_chart(img_file, chat_text, count=count):
    image_bytes = requests.get(img_file).content

    value = chatbot.ask(
        prompt=f"{chat_text}",
        image=image_bytes  # 传入图片的二进制数据，会自动上传给千问
    )
    output_text = value['contents'][0]['content']
    if output_text == '抱歉，系统超时，请稍后重试。':
        count += 1
        if count > 10:
            return 0, 0, '抱歉，系统超时，请稍后重试。'
        try:
            qwen_file_free_chart(img_file, chat_text)
        except:
            count -= 1

    return 0, 0, output_text


print(qwen_file_free_chart(
    'https://res.debtop.com/manage/live/paper/202410/24/20241024001845a058b9867f544a9f.png',
    '提取图片文字'))
# print(kimi_file_chat_free('https://res.debtop.com/manage/live/paper/202410/24/20241024001845a058b9867f544a9f.png',
# '提取图片文字'))
