import requests

cookies = {
    '_trs_uv': 'm607j1fd_4693_vbp',
    'FECW': '9cdb15212413ab67bc8b477a911fc4e45e8f605a376d73b6c91e938485f8646b98131b40cd9f9033caaba804985d7309ea1da4369fdfaf91c1774cdb5c189ee8e8b07291b948dd2ccc74e62ee3d8d474cb',
    'Hm_lvt_9b6808db613ab359882c1b06397459f7': '1746538470',
    'Hm_lpvt_9b6808db613ab359882c1b06397459f7': '1746605070',
    'HMACCOUNT': 'FDD970C8B3C27398',
    'TMYHSBMErr4s': 'A3B5FDCF3406E5DFBA71F5353B8D6DF8',
    'TGC': 'TGT-4123546-JX781cIKQli94gnIAOiS2fMyTqg25-KWG-kqOEliLSV7RSotfsDY1rTbtrJ2mKx7EKIcas-server01',
    'Admin-Token': 'eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjZmNTNiOTczLTY3NDItNDM1NS1iNGRmLTg3NTRiODBhNzhlMCJ9.w93u0HY-7wamEjHXW0yAX7rbAs0QmiSXtgu5IIxAh7mXBTHRqLnRW0d_-oh2fuoB0EqKzwlvC0yEadskspJHUA',
    'wc_userid': 'ec4ffe34ebd74d6f1dcd52169882d5877c273f75fb902755b0aea762097d1f87',
    'JSESSIONID': '00007SC0wYEJINbu36dhNDZZUI7:1cd1t78gt',
    'wsgs_cookie': '11696049',
    'FECA': 'ffsDchJ25VWFbSjzkS3wEme4Up2Yy9wrBaKtmklih4GB2q0fWA+sSbu/unC1DnGVZ17oLyvImyFWLpVp/bs/U4za9WnXp8oroE2H7c9F7l6vBlLuldkEMIDYsU56VV02RbsNjnBBzHq9tPAVN2hpaw7z2UvEy3mrdTfG5weGyQYy06yF9ZPs+9h++FV0hRrW4f',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://wsgs.sbj.cnipa.gov.cn:9443',
    'Pragma': 'no-cache',
    'Referer': 'https://wsgs.sbj.cnipa.gov.cn:9443/tmpu/yycw/getMain.html',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_trs_uv=m607j1fd_4693_vbp; FECW=9cdb15212413ab67bc8b477a911fc4e45e8f605a376d73b6c91e938485f8646b98131b40cd9f9033caaba804985d7309ea1da4369fdfaf91c1774cdb5c189ee8e8b07291b948dd2ccc74e62ee3d8d474cb; Hm_lvt_9b6808db613ab359882c1b06397459f7=1746538470; Hm_lpvt_9b6808db613ab359882c1b06397459f7=1746605070; HMACCOUNT=FDD970C8B3C27398; TMYHSBMErr4s=A3B5FDCF3406E5DFBA71F5353B8D6DF8; TGC=TGT-4123546-JX781cIKQli94gnIAOiS2fMyTqg25-KWG-kqOEliLSV7RSotfsDY1rTbtrJ2mKx7EKIcas-server01; Admin-Token=eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjZmNTNiOTczLTY3NDItNDM1NS1iNGRmLTg3NTRiODBhNzhlMCJ9.w93u0HY-7wamEjHXW0yAX7rbAs0QmiSXtgu5IIxAh7mXBTHRqLnRW0d_-oh2fuoB0EqKzwlvC0yEadskspJHUA; wc_userid=ec4ffe34ebd74d6f1dcd52169882d5877c273f75fb902755b0aea762097d1f87; JSESSIONID=00007SC0wYEJINbu36dhNDZZUI7:1cd1t78gt; wsgs_cookie=11696049; FECA=ffsDchJ25VWFbSjzkS3wEme4Up2Yy9wrBaKtmklih4GB2q0fWA+sSbu/unC1DnGVZ17oLyvImyFWLpVp/bs/U4za9WnXp8oroE2H7c9F7l6vBlLuldkEMIDYsU56VV02RbsNjnBBzHq9tPAVN2hpaw7z2UvEy3mrdTfG5weGyQYy06yF9ZPs+9h++FV0hRrW4f',
}

data = {
    'regNum': '',
    'tmName': '',
    'appCnName': '小米科技有限责任公司',
    'agentName': '',
    'objAppCnName': '',
    'objAgentName': '',
    'startDate': '',
    'endDate': '',
    'pagenum': '1',
    'pagesize': '30',
    'sum': '4731',
    'countpage': '158',
    'gopage': '1',
}

response = requests.post('https://wsgs.sbj.cnipa.gov.cn:9443/tmpu/yycw/getMain.html', cookies=cookies, headers=headers, data=data)
print(response.content.decode('utf-8'))