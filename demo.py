import requests

cookies = {
    'Hm_lvt_1aac8492a1c45f4949e13dc855f617ee': '1740019778',
    'HMACCOUNT': 'FDD970C8B3C27398',
    'Hm_lvt_c4f40a0013c2cb0ccb4ad6cf20361123': '1740019817',
    'Hm_lpvt_c4f40a0013c2cb0ccb4ad6cf20361123': '1740638630',
    'Hm_lpvt_1aac8492a1c45f4949e13dc855f617ee': '1740638630',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://www.csuaee.com.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://www.csuaee.com.cn/searchItem.html?keyword=%E5%80%BA%E6%9D%83',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'language': 'zh-cn',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'Hm_lvt_1aac8492a1c45f4949e13dc855f617ee=1740019778; HMACCOUNT=FDD970C8B3C27398; Hm_lvt_c4f40a0013c2cb0ccb4ad6cf20361123=1740019817; Hm_lpvt_c4f40a0013c2cb0ccb4ad6cf20361123=1740638630; Hm_lpvt_1aac8492a1c45f4949e13dc855f617ee=1740638630',
}

json_data = {
    'pageIndex': 1,
    'pageSize': 450,
    'categoryId': '',
    'price': '',
    'area': '',
    'status': '',
    'handType': '',
    'keyword': '',
    'keyword1': '债权',
    'isOrg': '',
}

response = requests.post(
    'https://www.csuaee.com.cn/api/article/web/getItemsList',
    headers=headers,
    json=json_data,
)
print(response.json())

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"pageIndex":2,"pageSize":10,"categoryId":"","price":"","area":"","status":"","handType":"","keyword":"","keyword1":"债权","isOrg":""}'.encode()
#response = requests.post('https://www.csuaee.com.cn/api/article/web/getItemsList', cookies=cookies, headers=headers, data=data)