import requests

cookies = {
    '_trs_uv': 'm1n0z125_4878_bybu',
    'HMF_CI': 'b51b612efcab0fb27c3cf129d01b6f57f9cc81ed33b9e6109db3dd05c0a07d30e57329e9b0f4965e6d33684674687b90b710359f359d7da20742fef2e71ca0f8ae',
    'HMY_JC': 'd91b61a45f651d66acb10be91f0c6e65e2e99075b6ee85196ecbc046654f38da00,',
    '_trs_ua_s_1': 'm28fwbwj_4878_6sqg',
    'HBB_HC': '24964091dfe18dabe54402bab839e0f6c0a6b8e5854e5b34841f6e5df2adaa9d9486714f935fc352c27a327bd9008a7fe5',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '_trs_uv=m1n0z125_4878_bybu; HMF_CI=b51b612efcab0fb27c3cf129d01b6f57f9cc81ed33b9e6109db3dd05c0a07d30e57329e9b0f4965e6d33684674687b90b710359f359d7da20742fef2e71ca0f8ae; HMY_JC=d91b61a45f651d66acb10be91f0c6e65e2e99075b6ee85196ecbc046654f38da00,; _trs_ua_s_1=m28fwbwj_4878_6sqg; HBB_HC=24964091dfe18dabe54402bab839e0f6c0a6b8e5854e5b34841f6e5df2adaa9d9486714f935fc352c27a327bd9008a7fe5',
    'Origin': 'https://jjjcb.ccdi.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://jjjcb.ccdi.gov.cn/epaper/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'docPubTime': '20241014',
}

response = requests.post('https://jjjcb.ccdi.gov.cn/reader/layout/findBmMenu.do', cookies=cookies, headers=headers, data=data)
print(response.text)