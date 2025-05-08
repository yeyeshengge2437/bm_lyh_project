import requests

cookies = {
    'hebp.session.id': '5ec6594dc4db42679bc5f2cf6a6c3929',
    'm5TEkyPGTubaO': '60zhRxFvVYeLifG4ow5PFiHqtYVAPTdLkYcPaZFNll9BNls5m7HADSIRhwiJcXup2IWcRTNJfGXQbs3pp4EHVkFG',
    'm5TEkyPGTubaS': '60Y6osFu_g1CMoPEXeetmjN.xzuhM_uXwAG4W0YijXaCWSpyGNJTW4r0Vpart5jzqPJ5g_8LkK5luOMbmH0s.KAG',
    'm5TEkyPGTubaT': '05zcVHyVVw30mSo.sPxG_WqdyqrddWiNTXaiANNIaSPt3r3TGZbQLagi.wHMWN7Kk5wskvVqpHTepWWMMV_DcucL7xJCatwc0bWi5yYz4sqO39yaYFvIMfISAeT_NoQ4gxW6Tsy_p8bQZeYMOnxVjYF.BpDFaOz2I3WDWY79idUiUsq4gcTH8RCXdFsmHrzcrQwkUUEBf83rUaYLbkxXSzSDF_Y1VPwIfRbOEDOiuOxKQaXSNyRvV6fK1h2Yu7paQY5_dHlovso2r3xGCIRCvxMWhY2.hO.8xVVJA1_WH6kYAki7o_mVybk2wF4u60GilKt80IqsQFVL0CYuGxB4UMCkzTUi.8JI4ruq9ggbbzYq6xY1UqeGXHJkyfmTi6Phij0wbWicg98yQsHJSIgq0usoHgoH8CF8Jac.rRTVVIDZUji2eJo8.jtN2ry.jMDD.oKR2w_t4s.iNfPgTNIIn0A',
    'pageNo': '1',
    'pageSize': '20',
    'm5TEkyPGTubaP': '0L4sFkQOdG7A8xYuj2f57Goh7CtIz9aXQFvgHGsonehlxcw7fSY0jdm2Fn9iecA4esurHldQIalaYqHbb3kViTy1bJITHmfGhqQaAWtuyt.9hSATkA9jEK4RtynBpPQTjAQfcKaMR8xlxxC788MaEy8wwwlyNNgsGtPHlDrTOEfJg24McqDnrRXKWWLgRNMKWQRldOW8Tv4Dx9E1hOiPVv72ZD0YLsKfaPEtRDyuQtFUOxDQd4DEKAzHW.34obLRK_GeN1Ib_BVAuhLjWJSEEYd0ecavaBJx5o01laV3FMIep20DKZJWAn0h3Wsv7pcv8DZcaC4ucXI3Oia8elzR1rlQ104cJem93FlrvwnGjVrIMMxl4JykaHaVC81JBH9LUsj9LNXB.xdkbAcHavY2oVP7hGLIpfuveCFVHGuZRIWQ',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://xypt.china-eia.com',
    'Pragma': 'no-cache',
    'Referer': 'https://xypt.china-eia.com/XYPT/unit/dataList?objectType=1&recordType=3',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'hebp.session.id=5ec6594dc4db42679bc5f2cf6a6c3929; m5TEkyPGTubaO=60zhRxFvVYeLifG4ow5PFiHqtYVAPTdLkYcPaZFNll9BNls5m7HADSIRhwiJcXup2IWcRTNJfGXQbs3pp4EHVkFG; m5TEkyPGTubaS=60Y6osFu_g1CMoPEXeetmjN.xzuhM_uXwAG4W0YijXaCWSpyGNJTW4r0Vpart5jzqPJ5g_8LkK5luOMbmH0s.KAG; m5TEkyPGTubaT=05zcVHyVVw30mSo.sPxG_WqdyqrddWiNTXaiANNIaSPt3r3TGZbQLagi.wHMWN7Kk5wskvVqpHTepWWMMV_DcucL7xJCatwc0bWi5yYz4sqO39yaYFvIMfISAeT_NoQ4gxW6Tsy_p8bQZeYMOnxVjYF.BpDFaOz2I3WDWY79idUiUsq4gcTH8RCXdFsmHrzcrQwkUUEBf83rUaYLbkxXSzSDF_Y1VPwIfRbOEDOiuOxKQaXSNyRvV6fK1h2Yu7paQY5_dHlovso2r3xGCIRCvxMWhY2.hO.8xVVJA1_WH6kYAki7o_mVybk2wF4u60GilKt80IqsQFVL0CYuGxB4UMCkzTUi.8JI4ruq9ggbbzYq6xY1UqeGXHJkyfmTi6Phij0wbWicg98yQsHJSIgq0usoHgoH8CF8Jac.rRTVVIDZUji2eJo8.jtN2ry.jMDD.oKR2w_t4s.iNfPgTNIIn0A; pageNo=1; pageSize=20; m5TEkyPGTubaP=0L4sFkQOdG7A8xYuj2f57Goh7CtIz9aXQFvgHGsonehlxcw7fSY0jdm2Fn9iecA4esurHldQIalaYqHbb3kViTy1bJITHmfGhqQaAWtuyt.9hSATkA9jEK4RtynBpPQTjAQfcKaMR8xlxxC788MaEy8wwwlyNNgsGtPHlDrTOEfJg24McqDnrRXKWWLgRNMKWQRldOW8Tv4Dx9E1hOiPVv72ZD0YLsKfaPEtRDyuQtFUOxDQd4DEKAzHW.34obLRK_GeN1Ib_BVAuhLjWJSEEYd0ecavaBJx5o01laV3FMIep20DKZJWAn0h3Wsv7pcv8DZcaC4ucXI3Oia8elzR1rlQ104cJem93FlrvwnGjVrIMMxl4JykaHaVC81JBH9LUsj9LNXB.xdkbAcHavY2oVP7hGLIpfuveCFVHGuZRIWQ',
}

data = {
    'pageNo': '1',
    'pageSize': '20',
    'objectType': '1',
    'recordType': '3',
    'unitName': '江西中能工程咨询有限公司',
    'socialCode': '',
    'provinceNum': '',
    'cityNum': '',
    'countyNum': '',
}

response = requests.post('https://xypt.china-eia.com/XYPT/unit/dataList', cookies=cookies, headers=headers, data=data)
print(response.content.decode('utf-8'))
