import requests

cookies = {
    'BDUSS': 'DQ3Q0ZNTTVsRzI2S2dzYWJNWHdKWU9NaktvZWZ5b3FhNFhCV3BwT0NHNWw1VXhvSVFBQUFBJCQAAAAAAAAAAAEAAADEMa0a1~PT0srWxcTFxGJpbgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGVYJWhlWCVoM',
}

headers = {
    # 'Cookie': 'BDUSS=DQ3Q0ZNTTVsRzI2S2dzYWJNWHdKWU9NaktvZWZ5b3FhNFhCV3BwT0NHNWw1VXhvSVFBQUFBJCQAAAAAAAAAAAEAAADEMa0a1~PT0srWxcTFxGJpbgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGVYJWhlWCVoM',
    'User-Agent': 'pan.baidu.com',
}

params = {
    'fid': '824085106-250528-171846634029238',
    'rt': 'pr',
    'sign': 'FDtAERK-DCb740ccc5511e5e8fedcff06b081203-5ltcQRtlwRwR3wb8ABalLmbpp4Y=',
    'expires': '8h',
    'chkbd': '0',
    'chkv': '0',
    'dp-logid': '4255205232210533127',
    'dp-callid': '0',
    'dstime': '1747278188',
    'r': '662398695',
    'vuk': '824085106',
    'origin_appid': '15195230',
    'file_type': '0',
    'access_token': '123.ae2997e979d6f8afe3b5908ef33d48f6.YHQuDBMEUJhX4Tw4LssnHL63zeLwPZAtPgM4jWL.bE2ZaQ',
}

response = requests.get(
    'https://d.pcs.baidu.com/file/3bd2d1fb1needbab82cd5a15991f7bd0',
    params=params,
    cookies=cookies,
    headers=headers,
)

with open('中国裁判文书网.rar', 'wb') as f:
    f.write(response.content)