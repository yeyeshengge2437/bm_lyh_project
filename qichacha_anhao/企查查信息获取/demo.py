import requests

cookies = {
    'qcc_did': 'aa80c299-a44e-4b99-bd8f-846f1f237214',
    'UM_distinctid': '191db1e9c1327b0-0fff366dedf7e-26001151-13c680-191db1e9c14297d',
    'tfstk': 'fPcn_NTwQvyBDkWgSdPBU4PJGZvTpwN730C827EyQlr1vMCKz7ro4lhLv2FFRAixu6hpd7CuO7NyDndvMy3QN78VqQ5CA5zuouR8Uk7FEiOJDndv6WQcsf-xvXMfON47byzza98g7yU7ayPz4Fqarr6PY0or7F4brT7FakRa_r47auozaF0ZaLbav0oI_HnnTn87veGa-JqlwlfoQf5YdouUj_-Ssyxz02rGa_rCKRQoS2KhGVFIMm4xvC5nm4ujURclbnqSsVlEUVsH4PMrv5rLgp7g9XgE38l2VTo0t02qTRbPg2gUf54ZgUBbXfqK4X2wks28_je4TAp6v8F3o0lIxafr0V3xORGkmGrSprNarbTVEu2P41BN3P01NSrhhT67LPagD91bdE9O3pAkSFXqhJz_8ILMST67LPagDFYG3nwU5yRA.',
    'QCCSESSID': 'f72a6883f0c42798c91732b09b',
    'acw_tc': '1a0c380b17328586027971643e0109758580926588e82fc284d63ae18382bc',
    'CNZZDATA1254842228': '1515781789-1725958102-https%253A%252F%252Fwww.zsamc.com%252F%7C1732858679',
}

headers = {
    '9b462154155e0c2b0b4a': '57dce1945b47fadc05627bfd85aa5ff1bbc0eb3c69c855aac269f45b77f3b00f65fd5b286544356d451c1475659fe51b915a41819fa813d2f1862d4339cd7591',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'qcc_did=aa80c299-a44e-4b99-bd8f-846f1f237214; UM_distinctid=191db1e9c1327b0-0fff366dedf7e-26001151-13c680-191db1e9c14297d; tfstk=fPcn_NTwQvyBDkWgSdPBU4PJGZvTpwN730C827EyQlr1vMCKz7ro4lhLv2FFRAixu6hpd7CuO7NyDndvMy3QN78VqQ5CA5zuouR8Uk7FEiOJDndv6WQcsf-xvXMfON47byzza98g7yU7ayPz4Fqarr6PY0or7F4brT7FakRa_r47auozaF0ZaLbav0oI_HnnTn87veGa-JqlwlfoQf5YdouUj_-Ssyxz02rGa_rCKRQoS2KhGVFIMm4xvC5nm4ujURclbnqSsVlEUVsH4PMrv5rLgp7g9XgE38l2VTo0t02qTRbPg2gUf54ZgUBbXfqK4X2wks28_je4TAp6v8F3o0lIxafr0V3xORGkmGrSprNarbTVEu2P41BN3P01NSrhhT67LPagD91bdE9O3pAkSFXqhJz_8ILMST67LPagDFYG3nwU5yRA.; QCCSESSID=f72a6883f0c42798c91732b09b; acw_tc=1a0c380b17328586027971643e0109758580926588e82fc284d63ae18382bc; CNZZDATA1254842228=1515781789-1725958102-https%253A%252F%252Fwww.zsamc.com%252F%7C1732858679',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.qcc.com/firm/6a6a2bdfcfec0102221e27582488b71f.html',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-pid': '867e0c3be7b30c808b832d7ce77aa583',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'isNewAgg': 'true',
    'keyNo': '6a6a2bdfcfec0102221e27582488b71f',
    'pageIndex': '3',
}

response = requests.get('https://www.qcc.com/api/datalist/hismainmember', params=params, cookies=cookies, headers=headers)
print(response.text)