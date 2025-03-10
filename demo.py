import requests


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ga=GA1.1.1606555070.1740029608; Hm_lvt_7de38d8594a7cf1a574241f30c33446b=1740536797; _ga_ERPNN1LEDY=deleted; _ga_ERPNN1LEDY=deleted; cart=; qimoClientId=6181641741573012907; EJY-JSESSIONID=MjAyMmQ5ZTctYzQwOC00OTlkLTg1NDAtOWExZTY5MTM1ODQ1; qimo_seosource_0=%E7%AB%99%E5%86%85; qimo_seokeywords_0=; uuid_49a6c050-3b8b-11eb-a27b-59d93a528836=855ed560-42a1-42a1-863d-7ca53f661f28; Hm_lvt_575182d134dee4d26e03124da592d030=1740029607,1740723217,1741161561,1741573016; HMACCOUNT=FDD970C8B3C27398; sessionId=2022d9e7-c408-499d-8540-9a1e69135845; qimo_seosource_49a6c050-3b8b-11eb-a27b-59d93a528836=%E7%AB%99%E5%86%85; qimo_seokeywords_49a6c050-3b8b-11eb-a27b-59d93a528836=; qimo_xstKeywords_49a6c050-3b8b-11eb-a27b-59d93a528836=; href=https%3A%2F%2Fwww.ejy365.com%2Fjygg_more%3Fproject_type%3DZQ; accessId=49a6c050-3b8b-11eb-a27b-59d93a528836; Hm_lpvt_575182d134dee4d26e03124da592d030=1741573118; pageViewNum=3; _ga_ERPNN1LEDY=GS1.1.1741573016.23.1.1741573218.0.0.0',
}

params = {
    'project_type': 'ZQ',
}

response = requests.get('https://www.ejy365.com/jygg_more', params=params, headers=headers)
print(response.text)
