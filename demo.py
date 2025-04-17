import requests

cookies = {
    'qcc_did': 'be2c322f-3bf8-468a-95e9-af9180b3ec36',
    'UM_distinctid': '1961d6869e7172-034b4fe1988468-26011d51-13c680-1961d6869e8aa6',
    'QCCSESSID': '612aa48e12b4abb0119ecf9515',
    'tfstk': 'gS2ZTxmKfOBNFA2NoDD2am02O6ktaAbW3-gjmoqmfV0MCdT0ToaYCjbtC-zEBJN6hV_t3o4S3a_5FTZTXbHcPaZst-mSEcommEGiK2Dj0eNfysZTXxKKbzq8klL2vyd7mx4mKXmmcxvDIqjEKmnxndcDIBYnJmDmnjvMKDmt0IvinfjUx2nmnq4mnAH4E-LEcfjbCcoZMUtns4qi8Kvy2clGQlOXFLwqbc2uj2oZbJoZ_4cp1Uc3IyZ0CRhd9BMYA7z4izbB1VVr4yl7_aJazPn08AwlD1hKi-yqvWQ2g4P0f7FmTGXgYAuZiJaHVBHaiPeq65-A2kDgJ73-s6QKYRwSg4he-NqQYVczgP_pnVNzxyl7de9SE7UU3bDl4BLxxf47H58DgfmKY4sFYlFAN7UH0ynHMIhOXDu5jfAvMfmKY4sFYIdx6PnEPGcG.',
    'acw_tc': '0a47318717447103012972598e0063a824fa2c0103b95a802017125a57a6eb',
    'CNZZDATA1254842228': '30391861-1744250104-%7C1744710616',
}

headers = {
    'a3e253822b7f0ab88583': '83c088918e0e986a57c78b02d72fccd0529247fbce29d4940c28a162319670ccb42219d5b8e811f5223ef3e05baa0971a03c8598f2b3eb276e4745e306e81f6b',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.qcc.com/crun/2516980a529613fad86ea2bd4092ed53.html',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-pid': '848521241e70b52955eb6dbad30f5e95',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'qcc_did=be2c322f-3bf8-468a-95e9-af9180b3ec36; UM_distinctid=1961d6869e7172-034b4fe1988468-26011d51-13c680-1961d6869e8aa6; QCCSESSID=612aa48e12b4abb0119ecf9515; tfstk=gS2ZTxmKfOBNFA2NoDD2am02O6ktaAbW3-gjmoqmfV0MCdT0ToaYCjbtC-zEBJN6hV_t3o4S3a_5FTZTXbHcPaZst-mSEcommEGiK2Dj0eNfysZTXxKKbzq8klL2vyd7mx4mKXmmcxvDIqjEKmnxndcDIBYnJmDmnjvMKDmt0IvinfjUx2nmnq4mnAH4E-LEcfjbCcoZMUtns4qi8Kvy2clGQlOXFLwqbc2uj2oZbJoZ_4cp1Uc3IyZ0CRhd9BMYA7z4izbB1VVr4yl7_aJazPn08AwlD1hKi-yqvWQ2g4P0f7FmTGXgYAuZiJaHVBHaiPeq65-A2kDgJ73-s6QKYRwSg4he-NqQYVczgP_pnVNzxyl7de9SE7UU3bDl4BLxxf47H58DgfmKY4sFYlFAN7UH0ynHMIhOXDu5jfAvMfmKY4sFYIdx6PnEPGcG.; acw_tc=0a47318717447103012972598e0063a824fa2c0103b95a802017125a57a6eb; CNZZDATA1254842228=30391861-1744250104-%7C1744710616',
}

params = {
    'keyNo': '2516980a529613fad86ea2bd4092ed53',
    'type': 'tc',
}

response = requests.get('https://www.qcc.com/api/riskDetail/creditratelist', params=params, cookies=cookies, headers=headers)
print(response.json())