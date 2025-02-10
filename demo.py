import requests

cookies = {
    'qcc_did': 'aa80c299-a44e-4b99-bd8f-846f1f237214',
    'UM_distinctid': '191db1e9c1327b0-0fff366dedf7e-26001151-13c680-191db1e9c14297d',
    'acw_tc': '1a0c384a17390845504854690e012caba6b11c537fbe937d66cbf753ee8d16',
    'QCCSESSID': '256acdafd4bcb3138feb7a3896',
    'tfstk': 'g9PIsj1JyHxQ-ltg-MQZcRul7nG7Vu1qVUg8ozdeyXhp23Uxb2PFxzn7VlogVYbn40n74zeF7s54-ycowQsVgs8Jc-wzO0KrwXc9koPVzs54-yHPvxclgW8jbYiI2bHKefUtjqKpJud-XNg-zHpJ9uUO5c0ryBHp9P3tPquKwbE8WNgoX0hz7BgNRc4CRDssFdYQmyn6wQFdZvibqLRJw5gId7UKfyaQ12MIDAR6iYPLbzFUtAXMQb4ahuw8DGJEv-gbfxyCcBZbx4EsTSQlKAD8N7ggIg9Sc8UUn8H1J6UsODM8_lL2IXw8x7M3dUb0WXEgnmDdIG0_TSkSmAtOvPzsvxw7YGA-Y-aTfxPwbIlYnlNSHjIrSIofpppWl1dS5m715LvuY6WJZ2v8oXHKSVSP5N94rv3i5m715LvopV0azN_63zf..',
    'CNZZDATA1254842228': '1515781789-1725958102-https%253A%252F%252Fwww.zsamc.com%252F%7C1739084759',
}

headers = {
    '1f57f2117d2ff9e98527': 'eed8b8826e3133f71dddaae08d7bf9fe48cff0fb671db4265bcacc9eda6ed7b92184c06478ea8f117d716f21a02f5fa4cd1d7cdecefcd8b4e40db1921ed0d48f',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'qcc_did=aa80c299-a44e-4b99-bd8f-846f1f237214; UM_distinctid=191db1e9c1327b0-0fff366dedf7e-26001151-13c680-191db1e9c14297d; acw_tc=1a0c384a17390845504854690e012caba6b11c537fbe937d66cbf753ee8d16; QCCSESSID=256acdafd4bcb3138feb7a3896; tfstk=g9PIsj1JyHxQ-ltg-MQZcRul7nG7Vu1qVUg8ozdeyXhp23Uxb2PFxzn7VlogVYbn40n74zeF7s54-ycowQsVgs8Jc-wzO0KrwXc9koPVzs54-yHPvxclgW8jbYiI2bHKefUtjqKpJud-XNg-zHpJ9uUO5c0ryBHp9P3tPquKwbE8WNgoX0hz7BgNRc4CRDssFdYQmyn6wQFdZvibqLRJw5gId7UKfyaQ12MIDAR6iYPLbzFUtAXMQb4ahuw8DGJEv-gbfxyCcBZbx4EsTSQlKAD8N7ggIg9Sc8UUn8H1J6UsODM8_lL2IXw8x7M3dUb0WXEgnmDdIG0_TSkSmAtOvPzsvxw7YGA-Y-aTfxPwbIlYnlNSHjIrSIofpppWl1dS5m715LvuY6WJZ2v8oXHKSVSP5N94rv3i5m715LvopV0azN_63zf..; CNZZDATA1254842228=1515781789-1725958102-https%253A%252F%252Fwww.zsamc.com%252F%7C1739084759',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.qcc.com/csusong/aee58eada8653b42219d5a49a0579668.html',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'x-pid': 'a1a3c22f9acfbc26dde95473e9b5ffd8',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'isNewAgg': 'true',
    'keyNo': 'aee58eada8653b42219d5a49a0579668',
    'KeyNo': 'aee58eada8653b42219d5a49a0579668',
    'pageIndex': '1',
}

response = requests.get('https://www.qcc.com/api/datalist/noticelist', params=params, cookies=cookies, headers=headers)
print(response.text)