import requests

cookies = {
    'JSESSIONID': '5A82742D73A3D5B6CD0EF59BFD19275A',
    'paiwu80_cookie': '45380249',
    'JSESSIONID9002C': 'CDDDEEB25180581FFDBC32071E89002C',
    'es.echatsoft.com_12555_encryptVID': '6za1%2F1xZ8Ea9Yf5iU65HdA%3D%3D',
    'es.echatsoft.com_12555_chatVisitorId': '4282295558',
    'echat_firsturl': '--1',
    'echat_firsttitle': '--1',
    'echat_referrer_timer': 'echat_referrer_timeout',
    'echat_referrer': '--1',
    'echat_referrer_pre': '',
    'ECHAT_12555_web4282295558_miniHide': '0',
    'insert_cookie': '58842404',
    'ariauseGraymode': 'false',
    'Hm_lvt_0f50400dd25408cef4f1afb556ccb34f': '1737422561',
    'Hm_lpvt_0f50400dd25408cef4f1afb556ccb34f': '1737422561',
    'HMACCOUNT': 'FDD970C8B3C27398',
    'arialoadData': 'true',
    'ariawapChangeViewPort': 'false',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'JSESSIONID=5A82742D73A3D5B6CD0EF59BFD19275A; paiwu80_cookie=45380249; JSESSIONID9002C=CDDDEEB25180581FFDBC32071E89002C; es.echatsoft.com_12555_encryptVID=6za1%2F1xZ8Ea9Yf5iU65HdA%3D%3D; es.echatsoft.com_12555_chatVisitorId=4282295558; echat_firsturl=--1; echat_firsttitle=--1; echat_referrer_timer=echat_referrer_timeout; echat_referrer=--1; echat_referrer_pre=; ECHAT_12555_web4282295558_miniHide=0; insert_cookie=58842404; ariauseGraymode=false; Hm_lvt_0f50400dd25408cef4f1afb556ccb34f=1737422561; Hm_lpvt_0f50400dd25408cef4f1afb556ccb34f=1737422561; HMACCOUNT=FDD970C8B3C27398; arialoadData=true; ariawapChangeViewPort=false',
    'Origin': 'https://permit.mee.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'page.pageNo': '1',
    'page.orderBy': '',
    'page.order': '',
    'tempReportKey': '34772c1fae2f4e2189ba658ee4cd6822',
    'province': '',
    'city': '',
    'registerentername': '宁城县易通塑料制品有限公司',
    'xkznum': '',
    'treadname': '',
    'treadcode': '',
    'publishtime': '',
}

response = requests.post(
    'https://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action',
    cookies=cookies,
    headers=headers,
    data=data,
)

print(response.text)
