import requests

cookies = {
    'UM_distinctid': '196a44d46a6125c-0d52038f44898c8-26011c51-13c680-196a44d46a7962',
    'tfstk': 'gjmsp7xAH1fsIX1nICpUFYKczeqXLjty1twxExINHlETHnGIZGl2IxuQGXH73ikxbj_YOj4VHNFYpWFLXr0ag5PbcxcWLQ-y4ADgmzdya38ARQZ_XRFAXPpY9-evLRChqGRQmodyTwSYS3Zm6nZmSmHpd-yVXihYkWpQh-rAXrIOJ6F3HoEYkGQKp8216NeYWpMLt-EADjExBPs_LdNnCdcFZFAWrfkTOiIxXn4_NENLKJoCkPFSBDSR2Le_57HTOCp8cuzKnricniaqB4c0efC9GSmIpc3-wB7a64wjUqGJ3N2UlcqQMcKlFWnshDai81QTFlN_ycU1ULDgk2iQbcdcrvkQ6zZE8eAaulGsr749-Bcjd5lxfyC6TSurLcUIwBSIirgxbkn993sPggPWWNQfdzjbd7JBdZbDDpvmYUcA8JUTKJR2dp_rnPe3d7JBdZb0WJ2E3p9Czxf..',
    'tgw_l7_route': 'c1e8cd038df3df705f7434c129439e7f',
    'JSESSIONID': 'A63AC5D06D9798B99A83A1E0C4125CAD.jvm2',
    'LFR_SESSION_STATE_20158': '1746689307847',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://rmfygg.court.gov.cn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?content=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'UM_distinctid=196a44d46a6125c-0d52038f44898c8-26011c51-13c680-196a44d46a7962; tfstk=gjmsp7xAH1fsIX1nICpUFYKczeqXLjty1twxExINHlETHnGIZGl2IxuQGXH73ikxbj_YOj4VHNFYpWFLXr0ag5PbcxcWLQ-y4ADgmzdya38ARQZ_XRFAXPpY9-evLRChqGRQmodyTwSYS3Zm6nZmSmHpd-yVXihYkWpQh-rAXrIOJ6F3HoEYkGQKp8216NeYWpMLt-EADjExBPs_LdNnCdcFZFAWrfkTOiIxXn4_NENLKJoCkPFSBDSR2Le_57HTOCp8cuzKnricniaqB4c0efC9GSmIpc3-wB7a64wjUqGJ3N2UlcqQMcKlFWnshDai81QTFlN_ycU1ULDgk2iQbcdcrvkQ6zZE8eAaulGsr749-Bcjd5lxfyC6TSurLcUIwBSIirgxbkn993sPggPWWNQfdzjbd7JBdZbDDpvmYUcA8JUTKJR2dp_rnPe3d7JBdZb0WJ2E3p9Czxf..; tgw_l7_route=c1e8cd038df3df705f7434c129439e7f; JSESSIONID=A63AC5D06D9798B99A83A1E0C4125CAD.jvm2; LFR_SESSION_STATE_20158=1746689307847',
}

params = {
    'p_p_id': 'noticelist_WAR_rmfynoticeListportlet',
    'p_p_lifecycle': '2',
    'p_p_state': 'normal',
    'p_p_mode': 'view',
    'p_p_resource_id': 'initNoticeList',
    'p_p_cacheability': 'cacheLevelPage',
    'p_p_col_id': 'column-1',
    'p_p_col_count': '1',
}

data = {
    '_noticelist_WAR_rmfynoticeListportlet_content': '',
    '_noticelist_WAR_rmfynoticeListportlet_searchContent': '小米科技有限责任公司',
    '_noticelist_WAR_rmfynoticeListportlet_courtParam': '',
    '_noticelist_WAR_rmfynoticeListportlet_IEVersion': 'ie',
    '_noticelist_WAR_rmfynoticeListportlet_flag': 'click',
    '_noticelist_WAR_rmfynoticeListportlet_noticeTypeVal': '全部',
    '_noticelist_WAR_rmfynoticeListportlet_sourceTypeVal': '全部',
    '_noticelist_WAR_rmfynoticeListportlet_aoData': '[{"name":"sEcho","value":1},{"name":"iColumns","value":6},{"name":"sColumns","value":",,,,,"},{"name":"iDisplayStart","value":0},{"name":"iDisplayLength","value":15},{"name":"mDataProp_0","value":null},{"name":"mDataProp_1","value":null},{"name":"mDataProp_2","value":null},{"name":"mDataProp_3","value":null},{"name":"mDataProp_4","value":null},{"name":"mDataProp_5","value":null}]',
}

response = requests.post(
    'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo',
    params=params,
    # cookies=cookies,
    headers=headers,
    data=data,
)

print(response.json())
