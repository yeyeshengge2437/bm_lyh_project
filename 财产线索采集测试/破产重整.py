import requests

cookies = {
    'JSESSIONID': '4A5B1F19FEBC99635779B10A3CF6CC92',
    'UM_distinctid': '196a44d46a6125c-0d52038f44898c8-26011c51-13c680-196a44d46a7962',
    'wzws_sessionid': 'gDExNy44OS4yLjc5gTMzZDBmMoJkMTBiY2WgaBnFnQ==',
    'pcxxw': '3f2933c7742b2f13f4c18d3d0e7756f6',
    'tfstk': 'gjmsp7xAH1fsIX1nICpUFYKczeqXLjty1twxExINHlETHnGIZGl2IxuQGXH73ikxbj_YOj4VHNFYpWFLXr0ag5PbcxcWLQ-y4ADgmzdya38ARQZ_XRFAXPpY9-evLRChqGRQmodyTwSYS3Zm6nZmSmHpd-yVXihYkWpQh-rAXrIOJ6F3HoEYkGQKp8216NeYWpMLt-EADjExBPs_LdNnCdcFZFAWrfkTOiIxXn4_NENLKJoCkPFSBDSR2Le_57HTOCp8cuzKnricniaqB4c0efC9GSmIpc3-wB7a64wjUqGJ3N2UlcqQMcKlFWnshDai81QTFlN_ycU1ULDgk2iQbcdcrvkQ6zZE8eAaulGsr749-Bcjd5lxfyC6TSurLcUIwBSIirgxbkn993sPggPWWNQfdzjbd7JBdZbDDpvmYUcA8JUTKJR2dp_rnPe3d7JBdZb0WJ2E3p9Czxf..',
    'JSESSIONID': 'AAAFE71087DE8BAA8436608A20C8C958',
}

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://pccz.court.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://pccz.court.gov.cn/pcajxxw/gkaj/gkaj?lx=999',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'JSESSIONID=4A5B1F19FEBC99635779B10A3CF6CC92; UM_distinctid=196a44d46a6125c-0d52038f44898c8-26011c51-13c680-196a44d46a7962; wzws_sessionid=gDExNy44OS4yLjc5gTMzZDBmMoJkMTBiY2WgaBnFnQ==; pcxxw=3f2933c7742b2f13f4c18d3d0e7756f6; tfstk=gjmsp7xAH1fsIX1nICpUFYKczeqXLjty1twxExINHlETHnGIZGl2IxuQGXH73ikxbj_YOj4VHNFYpWFLXr0ag5PbcxcWLQ-y4ADgmzdya38ARQZ_XRFAXPpY9-evLRChqGRQmodyTwSYS3Zm6nZmSmHpd-yVXihYkWpQh-rAXrIOJ6F3HoEYkGQKp8216NeYWpMLt-EADjExBPs_LdNnCdcFZFAWrfkTOiIxXn4_NENLKJoCkPFSBDSR2Le_57HTOCp8cuzKnricniaqB4c0efC9GSmIpc3-wB7a64wjUqGJ3N2UlcqQMcKlFWnshDai81QTFlN_ycU1ULDgk2iQbcdcrvkQ6zZE8eAaulGsr749-Bcjd5lxfyC6TSurLcUIwBSIirgxbkn993sPggPWWNQfdzjbd7JBdZbDDpvmYUcA8JUTKJR2dp_rnPe3d7JBdZb0WJ2E3p9Czxf..; JSESSIONID=AAAFE71087DE8BAA8436608A20C8C958',
}

data = {
    'start': '',
    'end': '',
    'cbt': '海南世知旅游有限公司',
    'lx': '999',
    'pageNum': '1',
}

response = requests.post('https://pccz.court.gov.cn/pcajxxw/gkaj/gkajlb', headers=headers, data=data)
print(response.text)
