import requests

cookies = {
    '__jdu': '17219744346561554622123',
    'mba_muid': '17219744346561554622123',
    'shshshfpa': '90cc9c0e-20a8-2ac9-50fd-bff89d16535a-1730357570',
    'shshshfpx': '90cc9c0e-20a8-2ac9-50fd-bff89d16535a-1730357570',
    'light_key': 'AASBKE7rOxgWQziEhC_QY6yaB3PQ6pVpcy9uYd_PD0N1ReA0e-l3oBNJnSJd3xypi9G1dQ3H',
    'pin': 'qwertyuiop2437',
    'unick': 'nty47n2qtsb0ac',
    'TrackID': '1XApSoDl49V6MFvfHdLb-v1mjxgdjA_vFF7jJh1jU97Jm8vz4rjO9x1nHnGMMR0C9i6PK-n2uG17cNBI7ZbQ0WcBipZDtqz2esLSm7LfTGK0|||GoDjOYOhdgEboMHtDlun2Q',
    'pinId': 'GoDjOYOhdgEboMHtDlun2Q',
    'wxa_level': '1',
    '__jdv': '96383255|baidu|-|organic|notset|1741655240850',
    'thor': '3E3E32A0C01B60F435A883D377C20D80264DBCE3015914B307D923C88BD7075C69EE104E9C799EDD0B8C8DA2E5681EE148B7EA7CB81EB8826A710023295296E3C0D839F169C03A6477EB71E696945D74AEC7B72B9F9385D58884D7E6DC1F94A98D6C77718C1E51715CA66238FE0D8358C1E50880230F889584D6A69398FD568A92DC0FD11C860C9B3B30DC96724F9A87',
    'joyya': '1741655840.1741655842.23.0w4jtju',
    'shshshfpb': 'BApXS3IjPgfBAOjIe0u_EfeI01o8m0OKABnJ0cl9o9xJ1Mv8SPoG2',
    '__jda': '150982071.17219744346561554622123.1721974435.1741655241.1741661414.19',
    '__jdc': '150982071',
    '3AB9D23F7A4B3CSS': 'jdd03V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPIAAAAMVQMWEIQAAAAAACJLLZEVJJ345QUX',
    '3AB9D23F7A4B3C9B': 'V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPI',
    'flash': '3_-sWiEUgiaEnRtJuj7SfdhxRQYbPLMLGC3SOBVl3OqL99PuR0ju1yU_ZbXT23aL0HVuk-zE5skjpBwcOKFwxkKhxyVOKggTRP-nxLqqrlZAuUjVJ_QlxVHkJwdKQYeaKpERWrrgSdMmiupPYvdmru5PEyWQ_GpYV8tdvqICRtlNSSPHM*',
    'sdtoken': 'AAbEsBpEIOVjqTAKCQtvQu17Tud5WnafMhtobdioRagSrCJi-nZUl_fPfDjf3AURcyT0VeuJ2-kAyXY6KefeXsZHjqR2A_MvR9CMOrKAOOQIsEp_4qZHXAa0YPx009MueWzlt6nBTXXvTnw52KCM',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://pmsearch.jd.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://pmsearch.jd.com/',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'x-referer-page': 'https://pmsearch.jd.com/',
    'x-rp-client': 'h5_1.0.0',
    # 'cookie': '__jdu=17219744346561554622123; mba_muid=17219744346561554622123; shshshfpa=90cc9c0e-20a8-2ac9-50fd-bff89d16535a-1730357570; shshshfpx=90cc9c0e-20a8-2ac9-50fd-bff89d16535a-1730357570; light_key=AASBKE7rOxgWQziEhC_QY6yaB3PQ6pVpcy9uYd_PD0N1ReA0e-l3oBNJnSJd3xypi9G1dQ3H; pin=qwertyuiop2437; unick=nty47n2qtsb0ac; TrackID=1XApSoDl49V6MFvfHdLb-v1mjxgdjA_vFF7jJh1jU97Jm8vz4rjO9x1nHnGMMR0C9i6PK-n2uG17cNBI7ZbQ0WcBipZDtqz2esLSm7LfTGK0|||GoDjOYOhdgEboMHtDlun2Q; pinId=GoDjOYOhdgEboMHtDlun2Q; wxa_level=1; __jdv=96383255|baidu|-|organic|notset|1741655240850; thor=3E3E32A0C01B60F435A883D377C20D80264DBCE3015914B307D923C88BD7075C69EE104E9C799EDD0B8C8DA2E5681EE148B7EA7CB81EB8826A710023295296E3C0D839F169C03A6477EB71E696945D74AEC7B72B9F9385D58884D7E6DC1F94A98D6C77718C1E51715CA66238FE0D8358C1E50880230F889584D6A69398FD568A92DC0FD11C860C9B3B30DC96724F9A87; joyya=1741655840.1741655842.23.0w4jtju; shshshfpb=BApXS3IjPgfBAOjIe0u_EfeI01o8m0OKABnJ0cl9o9xJ1Mv8SPoG2; __jda=150982071.17219744346561554622123.1721974435.1741655241.1741661414.19; __jdc=150982071; 3AB9D23F7A4B3CSS=jdd03V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPIAAAAMVQMWEIQAAAAAACJLLZEVJJ345QUX; 3AB9D23F7A4B3C9B=V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPI; flash=3_-sWiEUgiaEnRtJuj7SfdhxRQYbPLMLGC3SOBVl3OqL99PuR0ju1yU_ZbXT23aL0HVuk-zE5skjpBwcOKFwxkKhxyVOKggTRP-nxLqqrlZAuUjVJ_QlxVHkJwdKQYeaKpERWrrgSdMmiupPYvdmru5PEyWQ_GpYV8tdvqICRtlNSSPHM*; sdtoken=AAbEsBpEIOVjqTAKCQtvQu17Tud5WnafMhtobdioRagSrCJi-nZUl_fPfDjf3AURcyT0VeuJ2-kAyXY6KefeXsZHjqR2A_MvR9CMOrKAOOQIsEp_4qZHXAa0YPx009MueWzlt6nBTXXvTnw52KCM',
}

params = {
    'appid': 'paimai',
    'functionId': 'paimai_unifiedSearch',
    'body': '{"investmentType":"","apiType":12,"page":2,"pageSize":40,"keyword":"","provinceId":"","cityId":"","countyId":"","multiPaimaiStatus":"","multiDisplayStatus":"","multiPaimaiTimes":"","childrenCateId":"109","currentPriceRangeStart":"","currentPriceRangeEnd":"","timeRangeTime":"endTime","timeRangeStart":"","timeRangeEnd":"","loan":"","purchaseRestriction":"","orgId":"","orgType":"","sortField":8,"projectType":1,"reqSource":0,"labelSet":"1033","publishSource":"","publishSourceStr":["0","9"],"defaultLabelSet":""}',
    'clientVersion': 'paimai-h5-1.0.0',
    'client': 'paimai-h5',
    't': '1741671559475',
    'h5st': '20250311133921480;z9xiiaapwwh3w3w6;106e8;tk03w7bfc1ab218njLX6aYbVw9G2nBpIqDMbbSuP6bRIDPIlTI_BR8hS8b29U73oATIL-WMAKOErYKh3e7meeMLDGoER;e4bb6b4b772ca831e6fcd93726abe5428ff4cb6b934fb945fd16ba4268b424a6;5.1;1741671559480;ri_uxFOm4S3i3hrU3RnSNpYUFNXg0lsm0msSIlsmOGuj_mrm0mMTLhImOuMsCmsg4WIhKlLh1e4i5SLi3qriLhYV4uLV3iIVJdbWJpoVLlsm0msSo94VMZ4RMusmk_MmIl4h9WbhNh7i7eoiMlLW3qLW4mIW9mbV1qbiIRLWItLmOGLm7pIRAp4WMusmk_ciBuMgMebRMlsmOGujMuLj92ch4xZVCJIVPZrUMuMgMWHmOuMsCm8ZqJXW7unR92YVFVXZMuMgM64TK1YW8lsmOGujMm7iAJ4ZMuMgMWoSMusmk_cPOuMs9uMgMqbi5lImOusmOGuj2uMgMubi5lImOusmOGuj26sm0mMi9aHWMusmOuMsCmMSBRoZ96cZEl6TMuMgM64TK1YW8lsmOusmk_siOGLm2aHWMusmOuMsCurm0m8h5lImOusmOGuj9erm0mMh5lImOusmOGuj_uMgMabRMlsmOusmk_siOGLm6aHWMusmOuMsCObhOGLm7aHWMusmOuMsCmshAqLj_msm0mci5lImOusmOGuj_uMgMC4RMusmOuMsCarm0m8SClsmOusmk_siOGLmClsmOusmk_siOGLmKRHmOusmOG_QOGLmK1YV6NXVMusmk_cPOuMsMS7i6mrS-JYR1dHSJRXSMuMgMmrSMusmOuMsztMgMunSMusmk_Mm6WrQOCrh42YUXt8g_2si9usZgt8S3xoVAJ4ZMuMgMqYR7lsmOG_Q;b046307118b1b488130e2f9da52cc4e8646eb42846ce4cce22ff22d58331031a',
    'x-api-eid-token': 'jdd03V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPIAAAAMVQMOCIVQAAAAAD62I3MLU4Z4DHIX',
}

json_data = None

response = requests.post('https://api.m.jd.com/api', params=params, cookies=cookies, headers=headers, json=json_data)
print(response.json())