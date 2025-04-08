import requests

cookies = {
    'qcc_did': 'aa80c299-a44e-4b99-bd8f-846f1f237214',
    'UM_distinctid': '1958f8111659a6-0b87471533570c-26011a51-13c680-1958f8111662530',
    'QCCSESSID': 'b6126e18d64429e5e9530fa51a',
    'tfstk': 'gKMIsj9R2wbIxV_ixeKac7_L5PwWN494PgZ-m0BF2JedyanY7kke-0USPVziP7x3zzUSz0hebKJqxD2ueTT23K5laTSodzQzeJ2ODqk24KJqxDFyJS2k3vWd2czQy8FLw5FTSoQL24FKXlUgquQL29KsXP4OeaUdpRUT2oq8e83-XhZuWzH1N9ZwAPmBx_zx7SjJ8Dz1eTH_XU4xAcZgjAZQOrFL5TnICkNQkDH3yrALXAk_g5Sy5Rnm_2E_hp_0AfnbpuMkD_a7Nv2_VfYCTqg32cFs835ufbi-nJ2f2pn_dyNxBWvWmqns2jPsQnp0dJUKaJmPceosd2onC0SR6JwE1SMQHKbLzfojFuMkrdgj2mc81Y_C4c64lBCdNi9OFla2fh1lZQfplTZhwm2L9lqwzht1g0VLjla2fh1lZWEgb0-6fsol.',
    'acw_tc': '0a47308c17440809705287476e004aee8ff6eb8bd339aed5aad279b59c19c0',
    'CNZZDATA1254842228': '1515781789-1725958102-https%253A%252F%252Fwww.zsamc.com%252F%7C1744081061',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.qcc.com/web/search?key=%E6%B1%9F%E8%8B%8F%E5%90%8D%E9%93%B8%E5%9B%BD%E9%99%85%E8%B4%B8%E6%98%93%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'qcc_did=aa80c299-a44e-4b99-bd8f-846f1f237214; UM_distinctid=1958f8111659a6-0b87471533570c-26011a51-13c680-1958f8111662530; QCCSESSID=b6126e18d64429e5e9530fa51a; tfstk=gKMIsj9R2wbIxV_ixeKac7_L5PwWN494PgZ-m0BF2JedyanY7kke-0USPVziP7x3zzUSz0hebKJqxD2ueTT23K5laTSodzQzeJ2ODqk24KJqxDFyJS2k3vWd2czQy8FLw5FTSoQL24FKXlUgquQL29KsXP4OeaUdpRUT2oq8e83-XhZuWzH1N9ZwAPmBx_zx7SjJ8Dz1eTH_XU4xAcZgjAZQOrFL5TnICkNQkDH3yrALXAk_g5Sy5Rnm_2E_hp_0AfnbpuMkD_a7Nv2_VfYCTqg32cFs835ufbi-nJ2f2pn_dyNxBWvWmqns2jPsQnp0dJUKaJmPceosd2onC0SR6JwE1SMQHKbLzfojFuMkrdgj2mc81Y_C4c64lBCdNi9OFla2fh1lZQfplTZhwm2L9lqwzht1g0VLjla2fh1lZWEgb0-6fsol.; acw_tc=0a47308c17440809705287476e004aee8ff6eb8bd339aed5aad279b59c19c0; CNZZDATA1254842228=1515781789-1725958102-https%253A%252F%252Fwww.zsamc.com%252F%7C1744081061',
}

response = requests.get('https://www.qcc.com/firm/4991a538ca014e2a5eb5f1d93d9c6fc9.html', cookies=cookies, headers=headers)
print(response.text)
