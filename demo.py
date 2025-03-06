import requests

cookies = {
    'JSESSIONID': '49B045CF0B2DF12E9630B8A885E54C26',
    'Hm_lvt_6eda7fc02dd514d4aa276037c947668f': '1739963032,1740040980',
    'HWWAFSESID': '629717395942b88b17',
    'HWWAFSESTIME': '1741223999066',
    'Hm_lvt_865d7b41bbb886391b9a558ea304692d': '1739963069,1740990818,1741224051',
    'HMACCOUNT': 'FDD970C8B3C27398',
    'Hm_lpvt_865d7b41bbb886391b9a558ea304692d': '1741227792',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    # 'Cookie': 'JSESSIONID=49B045CF0B2DF12E9630B8A885E54C26; Hm_lvt_6eda7fc02dd514d4aa276037c947668f=1739963032,1740040980; HWWAFSESID=629717395942b88b17; HWWAFSESTIME=1741223999066; Hm_lvt_865d7b41bbb886391b9a558ea304692d=1739963069,1740990818,1741224051; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_865d7b41bbb886391b9a558ea304692d=1741227792',
}

params = {
                        'to': 'proAtta',
                        'proId': f'c9d38976854b4344a68e9b00f65e2c03',
                        'packId': '',
                    }

ann_res = requests.post('http://gz.gemas.com.cn/portal/page', params=params,
                         headers=headers, verify=False)
ann_html = ann_res.text
print(ann_html)