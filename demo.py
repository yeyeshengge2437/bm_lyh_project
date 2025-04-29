import requests

cookies = {
    'qcc_did': 'aa80c299-a44e-4b99-bd8f-846f1f237214',
    'UM_distinctid': '1958f8111659a6-0b87471533570c-26011a51-13c680-1958f8111662530',
    'QCCSESSID': '2e4a8c2af4435ba139438b4b5a',
    'tfstk': 'g17Itna-wvDCtOMGtJFwG0rN5h87dTa2FbORi_3EweLKeYCvQB7UK_p5FOJGF3VHULp5U_IU_rzVt6Yky4w4urzr29eFdvdJ27d9wQPw9VPoR3Yky-ywAZI0sUXpVK5hv1F6aQupwTp-BdpMNLHRepKtBIODyLBReC39MIoKeBdpX5OkBLLJyTCtBYgB_W9GOWVEeTpYy-5eC43R5CekG6aqPC7pOH9A9N0-yjdBAKCpC-7V8AKOZ3_oZ4tP9iXkM9HLFLb16wIAHRoepiO5gg6YaDAwVwY6ewUmGdQCNNthbvnpGe9BDwKIgSfH2G_68weom156pnTNbl2e4e6CmKxLjRX51pWRRhHQQLSV_wK1HRu1E3sR8FQLBrsPkqJbvDnSGP3W1KP_10muy5Vl7BmRieKpsCyz15iVZHdM1KP_10mkvCANa5Ns0_f..',
    'acw_tc': '0a472f4a17459087014437971e0071c2f7a00a6da32e6d5bf69b22a9dbe16f',
    'CNZZDATA1254842228': '1515781789-1725958102-https%253A%252F%252Fwww.zsamc.com%252F%7C1745908703',
}

headers = {
    '4442da9fec36b8cc785d': 'c9771bff79509906e6970081a882964cbf2464b68f65bb23cf6df556c710b19e39700df993fa5803f8c5a8e31841765215fa54489bebeb73290578ccba0084cc',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.qcc.com/csusong/4991a538ca014e2a5eb5f1d93d9c6fc9.html',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-pid': '5b0c4292faa95d62923e8f8ced224b0c',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'qcc_did=aa80c299-a44e-4b99-bd8f-846f1f237214; UM_distinctid=1958f8111659a6-0b87471533570c-26011a51-13c680-1958f8111662530; QCCSESSID=2e4a8c2af4435ba139438b4b5a; tfstk=g17Itna-wvDCtOMGtJFwG0rN5h87dTa2FbORi_3EweLKeYCvQB7UK_p5FOJGF3VHULp5U_IU_rzVt6Yky4w4urzr29eFdvdJ27d9wQPw9VPoR3Yky-ywAZI0sUXpVK5hv1F6aQupwTp-BdpMNLHRepKtBIODyLBReC39MIoKeBdpX5OkBLLJyTCtBYgB_W9GOWVEeTpYy-5eC43R5CekG6aqPC7pOH9A9N0-yjdBAKCpC-7V8AKOZ3_oZ4tP9iXkM9HLFLb16wIAHRoepiO5gg6YaDAwVwY6ewUmGdQCNNthbvnpGe9BDwKIgSfH2G_68weom156pnTNbl2e4e6CmKxLjRX51pWRRhHQQLSV_wK1HRu1E3sR8FQLBrsPkqJbvDnSGP3W1KP_10muy5Vl7BmRieKpsCyz15iVZHdM1KP_10mkvCANa5Ns0_f..; acw_tc=0a472f4a17459087014437971e0071c2f7a00a6da32e6d5bf69b22a9dbe16f; CNZZDATA1254842228=1515781789-1725958102-https%253A%252F%252Fwww.zsamc.com%252F%7C1745908703',
}

params = {
    'isNewAgg': 'true',
    'keyNo': '4991a538ca014e2a5eb5f1d93d9c6fc9',
    'pageIndex': '2',
    # 'pageSize': '10',
}

response = requests.get('https://www.qcc.com/api/datalist/lianlist', params=params, cookies=cookies, headers=headers)
print(response.json())


# pageSize
