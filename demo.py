import requests

cookies = {
    '__jsluid_s': '7d23da733017326098a296c6ea999193',
    '6BVIhF5m7wQjO': '60YFGNFEvWpCS6B_SHPsMG4b3aIAkX7KGjtM52buMh_ctKkxaGuIToqw2uss0Y09Rq2AHr6IER9bFqdn.M0Y6TRG',
    'cookienum': '0.32873498329278794',
    'Hm_lvt_0076fef7e919d8d7b24383dc8f1c852a': '1736936661,1736997404,1737344002,1737361986',
    'HMACCOUNT': 'FDD970C8B3C27398',
    'SESSION': '40684c84-0bde-4a1b-87da-d739736fa499',
    'Hm_lpvt_0076fef7e919d8d7b24383dc8f1c852a': '1737362621',
    'insert_cookie': '35833434',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': '__jsluid_s=7d23da733017326098a296c6ea999193; 6BVIhF5m7wQjO=60YFGNFEvWpCS6B_SHPsMG4b3aIAkX7KGjtM52buMh_ctKkxaGuIToqw2uss0Y09Rq2AHr6IER9bFqdn.M0Y6TRG; cookienum=0.32873498329278794; Hm_lvt_0076fef7e919d8d7b24383dc8f1c852a=1736936661,1736997404,1737344002,1737361986; HMACCOUNT=FDD970C8B3C27398; SESSION=40684c84-0bde-4a1b-87da-d739736fa499; Hm_lpvt_0076fef7e919d8d7b24383dc8f1c852a=1737362621; insert_cookie=35833434',
    'Origin': 'https://www.creditchina.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://www.creditchina.gov.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'rcwCQitg': '0MCfs.GlqEDxJQdpVz2nQI3zwNcOv07Up3PJSDM9W_gDbr10pC_OkGbkrXxJ5K26_p5cat3tne1VtbYVnRUO9kM3QtLbwN9dvlY.Vp4b2vLEcp5dBg3AK0GTwZIWnCBWl2HYFMu9WHNPuoX73pVMUBKsm8cCGRZaBgnExhkA7yKPGKyve3zSJw_By5Z5P.SRztCEKavGjNyJlIhzRse9nM2wcM05YBUoL_mJDioMG8Ikf7hu36OIZuO7kfRJm.LBB9SgzdvW5tc4O3T9f1Zkld6yd5zPff5vdDQDNQMICgkVbAHhE43tFJ.hPf8zIy2pmwN134fQMKzWbj0eTu6XduFiHzUvaOjHB_DisTvA7afh3Si9glmoB7w25u_Ts_tboPZXADo1Q.etRbpjni9rN0.WAlwxbs4qfr.TrRnB6BSD0Ledv86AXe6cIk8ZxHgfecNUSxQa4CE3rK8NeYamDu7c95kJ79BhDMTLsPumB_KOQE45_wr3jcfxMS_KWhWa6kUKsXxXh3Rncpa9FLdmNUPQTYXDnKDSx3sqk6AxRXK0hOhskgANvGLdcfOjHSKKcyAiFxBjEuYv24W7OKuvDIB2ChLgU1_FHtmGNN6ZkvMMCPby4T1bhasKuItPgS92X95o54mTNK2H.RPCZNmaOmci5_BFuXAXx9thjAFkQk.f7ZMbDyeZOQnax5zkXox3OL_MkiAJsaqBlr17HSXdxoqNAFV0DqS6m5S3n0dNrAdDgoUQPUXHBDA4MJVJW5Pn2XPuCJaQeuUmE39t4wqlGhP.n5TY8LiIjvjGcqo5ymUSeO7bQyOtl_bJjh9kgEr52Cj9om9mamCUpAnNAOe2cXOlHztQ27mnK4G',
}

response = requests.get(
    'https://public.creditchina.gov.cn/private-api/catalogSearchHome',
    params=params,
    cookies=cookies,
    headers=headers,
)
print(response.text)