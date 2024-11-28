import requests

cookies = {
    'Hm_lvt_c528b72a72ecbef34604f03874c7f501': '1732672999',
    'HMACCOUNT': 'FDD970C8B3C27398',
    'mediav': "%7B%22eid%22%3A%22770295%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22ErF.Kx*%23B%2F%3Dx'Hv%25'%2Fe%60%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22ErF.Kx*%23B%2F%3Dx'Hv%25'%2Fe%60%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A0%7D",
    'sid': 'f4a1d0c3-d37c-43bd-9753-b3fa314191b1',
    'Qs_lvt_470704': '1732673000%2C1732673503%2C1732692225',
    'Hm_lpvt_c528b72a72ecbef34604f03874c7f501': '1732694435',
    'Qs_pv_470704': '3542253232534243000%2C4253660448197438500%2C4300927729351529000%2C2691320980668482600%2C375662314404364860',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryQjNEbGnSM5zI5S36',
    # 'Cookie': "Hm_lvt_c528b72a72ecbef34604f03874c7f501=1732672999; HMACCOUNT=FDD970C8B3C27398; mediav=%7B%22eid%22%3A%22770295%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22ErF.Kx*%23B%2F%3Dx'Hv%25'%2Fe%60%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22ErF.Kx*%23B%2F%3Dx'Hv%25'%2Fe%60%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A0%7D; sid=f4a1d0c3-d37c-43bd-9753-b3fa314191b1; Qs_lvt_470704=1732673000%2C1732673503%2C1732692225; Hm_lpvt_c528b72a72ecbef34604f03874c7f501=1732694435; Qs_pv_470704=3542253232534243000%2C4253660448197438500%2C4300927729351529000%2C2691320980668482600%2C375662314404364860",
    'Origin': 'https://www.etoplive.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.etoplive.com/products/bankflow.do',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

files = {
    'appKey': (None, 'bankflow'),
    'catalogId': (None, ''),
    'token': (None, ''),
    'files': ('page3_image1.jpeg', '', 'image/jpeg'),
    '_files': (None, 'page3_image1.jpeg'),
}

response = requests.post(
    'https://www.etoplive.com/trial/recognizePage.srvc?fileapi17326944358085',
    cookies=cookies,
    headers=headers,
    files=files,
)
print(response.text)