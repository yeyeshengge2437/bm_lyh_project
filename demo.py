import requests

cookies = {
    'cart': '',
    'Hm_lvt_575182d134dee4d26e03124da592d030': '1740029607',
    'HMACCOUNT': 'FDD970C8B3C27398',
    '_ga': 'GA1.1.1606555070.1740029608',
    'ASP.NET_SessionId': 'lonhiiavhb4f3lfvyisrtkso',
    'Hm_lvt_6c6f927bbff1cfe5d356339000013a45': '1740051217',
    'sessionId': 'd5c6ecb4-46e4-4c37-89ae-b808c089fef8',
    'Hm_lpvt_575182d134dee4d26e03124da592d030': '1740387824',
    '_ga_ERPNN1LEDY': 'GS1.1.1740387199.3.1.1740387886.0.0.0',
    'Hm_lpvt_6c6f927bbff1cfe5d356339000013a45': '1740388143',
}

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
    # 'Cookie': 'cart=; Hm_lvt_575182d134dee4d26e03124da592d030=1740029607; HMACCOUNT=FDD970C8B3C27398; _ga=GA1.1.1606555070.1740029608; ASP.NET_SessionId=lonhiiavhb4f3lfvyisrtkso; Hm_lvt_6c6f927bbff1cfe5d356339000013a45=1740051217; sessionId=d5c6ecb4-46e4-4c37-89ae-b808c089fef8; Hm_lpvt_575182d134dee4d26e03124da592d030=1740387824; _ga_ERPNN1LEDY=GS1.1.1740387199.3.1.1740387886.0.0.0; Hm_lpvt_6c6f927bbff1cfe5d356339000013a45=1740388143',
}

response = requests.get(
    'https://xjcqjy.ejy365.com//ejy/EDetail?infoId=N0125ZQ240014&bmStatus=%E5%B7%B2%E6%88%90%E4%BA%A4&ggType=JYGG&title=%e4%b8%ad%e6%96%b0%e5%bb%ba%e6%8b%9b%e5%95%86%e8%82%a1%e6%9d%83%e6%8a%95%e8%b5%84%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8%e8%bd%ac%e8%ae%a9%e6%8c%81%e6%9c%89%e6%96%b0%e7%96%86%e6%b5%a6%e6%9b%8c%e7%a7%91%e6%8a%80%e5%8f%91%e5%b1%95%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8%e4%b8%8d%e8%89%af%e5%80%ba%e6%9d%83(%e5%9b%bd%e8%b5%84%e7%9b%91%e6%b5%8b%e7%bc%96%e5%8f%b7GR2024XJ1001476)&infokey=ejy228070',
    headers=headers,
)