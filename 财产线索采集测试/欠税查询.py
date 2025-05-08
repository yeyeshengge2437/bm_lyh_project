import requests

cookies = {
    'yfx_c_g_u_id_10000001': '_ck24111509403115894178548512377',
    'yfx_f_l_v_t_10000001': 'f_t_1731634831587__r_t_1732260468330__v_t_1732260468330__r_c_1',
    '_yfxkpy_ssid_10003709': '%7B%22_yfxkpy_firsttime%22%3A%221737422831701%22%2C%22_yfxkpy_lasttime%22%3A%221737422831701%22%2C%22_yfxkpy_visittime%22%3A%221737422831701%22%2C%22_yfxkpy_cookie%22%3A%2220250121092711702174652306922481%22%7D',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22196a57444d71105-00d3c548f8e80cf-26011c51-1296000-196a57444d82383%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk2YTU3NDQ0ZDcxMTA1LTAwZDNjNTQ4ZjhlODBjZi0yNjAxMWM1MS0xMjk2MDAwLTE5NmE1NzQ0NGQ4MjM4MyJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22196a57444d71105-00d3c548f8e80cf-26011c51-1296000-196a57444d82383%22%7D',
    'je_ZDJWEB_yata': 'cXTzj3v4+795526792-j24o0i58pJnFIw55VB_AsIfOXW6KUP1lihQCaKKtVcAO5KBzw2MnCimvldq33A7TTDxP.iQYxyRYgBrMC5cjfFUuV2H4azvZtFuhMpbtVL73aa2f5mSE9HaUBJ4Ha2hhYwPWQmq5xyAs8SKNhKjb0nTb5QesucieU9acFpgKY0Sa0vq45v8b.lFq2Mz1A9XXmGnq9mkLNnZKKHnfyGVPPQs4jI67QkfitqkBI4bbGgQwcu13DbHbVq30zeXd6C67CeEbCDAHbrkTeZba5SJeWa',
    'tfstk': 'ghHnIXtw_XPQXa8T6AwBiEc2w4O9bJw7s4B8y8Uy_Pzs9TdCef4oR2VJAzdC4f0q5_FyR03GAA0ce9LBO0Wue88vkKpxAke7UEdawhulRuElUk788GyQ2LG9DSvxADsauWPhEKIk9-zLUzuzT5raAPrFakuzQRr079rPLu7wjPaNz_PUTdzaDu6UU8urbhq77zyzT4oZCVSaJ4uIQFtwe-3uQglUxW4qYyoKvAyNkrmUSTWz-kVhjDzGUTkiZ85a3yRfXzwLRDZnPK6QL7crpRke7LyqGVDug-AJA-kI4jGrfwxu8c3InJkD-9ETZycZL5jPUD2sT7ho-efQ8X3gGlPNqKZtkPoILfx57DuY-Jra6K-mb7ltdSMp792qGDeKaq8O9yl04guh_srifTZw2A55NWr_jrUDo4DQ4M16mhxGgjNUfkJvjhf5NWr_jrKMjs8bTlZeH',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://etax.jiangsu.chinatax.gov.cn:8443',
    'Pragma': 'no-cache',
    'Referer': 'https://etax.jiangsu.chinatax.gov.cn:8443/xxbg/view/zhsffw/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'X-B3-Sampled': '1',
    'X-B3-SpanId': '332afcdd0c924146',
    'X-B3-TraceId': '332afcdd0c924146',
    'X-Tsf-Client-Timestamp': '1746625261156',
    'djxh': 'undefined',
    'requestId': '1746625261156',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'yfx_c_g_u_id_10000001=_ck24111509403115894178548512377; yfx_f_l_v_t_10000001=f_t_1731634831587__r_t_1732260468330__v_t_1732260468330__r_c_1; _yfxkpy_ssid_10003709=%7B%22_yfxkpy_firsttime%22%3A%221737422831701%22%2C%22_yfxkpy_lasttime%22%3A%221737422831701%22%2C%22_yfxkpy_visittime%22%3A%221737422831701%22%2C%22_yfxkpy_cookie%22%3A%2220250121092711702174652306922481%22%7D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22196a57444d71105-00d3c548f8e80cf-26011c51-1296000-196a57444d82383%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk2YTU3NDQ0ZDcxMTA1LTAwZDNjNTQ4ZjhlODBjZi0yNjAxMWM1MS0xMjk2MDAwLTE5NmE1NzQ0NGQ4MjM4MyJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22196a57444d71105-00d3c548f8e80cf-26011c51-1296000-196a57444d82383%22%7D; je_ZDJWEB_yata=cXTzj3v4+795526792-j24o0i58pJnFIw55VB_AsIfOXW6KUP1lihQCaKKtVcAO5KBzw2MnCimvldq33A7TTDxP.iQYxyRYgBrMC5cjfFUuV2H4azvZtFuhMpbtVL73aa2f5mSE9HaUBJ4Ha2hhYwPWQmq5xyAs8SKNhKjb0nTb5QesucieU9acFpgKY0Sa0vq45v8b.lFq2Mz1A9XXmGnq9mkLNnZKKHnfyGVPPQs4jI67QkfitqkBI4bbGgQwcu13DbHbVq30zeXd6C67CeEbCDAHbrkTeZba5SJeWa; tfstk=ghHnIXtw_XPQXa8T6AwBiEc2w4O9bJw7s4B8y8Uy_Pzs9TdCef4oR2VJAzdC4f0q5_FyR03GAA0ce9LBO0Wue88vkKpxAke7UEdawhulRuElUk788GyQ2LG9DSvxADsauWPhEKIk9-zLUzuzT5raAPrFakuzQRr079rPLu7wjPaNz_PUTdzaDu6UU8urbhq77zyzT4oZCVSaJ4uIQFtwe-3uQglUxW4qYyoKvAyNkrmUSTWz-kVhjDzGUTkiZ85a3yRfXzwLRDZnPK6QL7crpRke7LyqGVDug-AJA-kI4jGrfwxu8c3InJkD-9ETZycZL5jPUD2sT7ho-efQ8X3gGlPNqKZtkPoILfx57DuY-Jra6K-mb7ltdSMp792qGDeKaq8O9yl04guh_srifTZw2A55NWr_jrUDo4DQ4M16mhxGgjNUfkJvjhf5NWr_jrKMjs8bTlZeH',
}

params = {
    'djxh': '',
    '_': '1746625261156',
}

json_data = {
    'Id': 'Captcha_a95e4450-1a16-4b9f-aff8-9906d981db19',
    'Xzqh': '320000',
    'Nsrmc': '丹阳浩远电子有限公司',
    'Code': 'qchg',
    'Ggrqq': '2024-05-08',
    'Ggrqz': '2025-05-07',
}

response = requests.post(
    'https://etax.jiangsu.chinatax.gov.cn:8443/xxbg/api/zhsffw/ggcx/qscx/queryQcxxList',
    params=params,
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"Id":"Captcha_a95e4450-1a16-4b9f-aff8-9906d981db19","Xzqh":"320000","Nsrmc":"丹阳浩远电子有限公司","Code":"qchg","Ggrqq":"2024-05-08","Ggrqz":"2025-05-07"}'.encode()
#response = requests.post(
#    'https://etax.jiangsu.chinatax.gov.cn:8443/xxbg/api/zhsffw/ggcx/qscx/queryQcxxList',
#    params=params,
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)
print(response.content.decode('utf-8'))