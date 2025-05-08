import requests

cookies = {
    'NOh8RTWx6K2dS': '60G2EKq5u8dYr2gNLRXxIkGuFGRhBjGaBVqv0BucwQavcDmV4eK1l7uQOAGhkWHYWEBIFwU0Utob_1K9HQD6Vr0a',
    'WEB': '20111132',
    '.AspNetCore.Antiforgery.VJ9V3gR6RkM': 'CfDJ8IsxmZmItZ9GiKs4EcN_vHFZHrJkrvC7wBsvjdbnwNIzG52zzpS-xkp2g44iu3BAjw3ovp3IbInvQetNZLXJwjpjW8o_UJtUphwnaafaHAx3tgY-cC57FtY4j1jJ4KQjUQhq2dAA45t-ygY58dZyirc',
    'NOh8RTWx6K2dT': '0vDdhp2vGMO7rXn8EVuvAmBu_Cwu7WspYWpPxcPp4rcJyI799e5iG1Dv4q.xah0cB3V.PgD0zR1eM0mbiPl67uQF6ndW9JXP5fAhfo9EihzTHzbSJgRx4Hvl.jMekzb.qFNg5qBtW9XWXjPOwUjAtuWHGLtyMXmM8KRK0x5djxtN8y3TF2bvAgcr1co9TJIQw0X9bX.ym2_.DGzV.iip8ytSA2q_cHKtObvTyz.Ic3AxWlFMgrX6ZD2YcBmdLITd.GhcTvJ.sdk_SSWU.TVWFSDLFpgGRQ5Xu3VHv15OZeE5qvCfWzO2ZwRQ.4WWPli0OPbYqbhbry53290AGb43LXOFbnewAB5XfJUC975JHH76vF6J_9Gjpc5K0N3oYaZGX1eMJOVbTPplz_FpkKRIoILdLoo6U7IIvhBJCFczpqdpTqKbFMXLXrN_3VYO6Zksd',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://epub.cnipa.gov.cn',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://epub.cnipa.gov.cn/Dxb/IndexQuery',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    # 'Cookie': 'NOh8RTWx6K2dS=60G2EKq5u8dYr2gNLRXxIkGuFGRhBjGaBVqv0BucwQavcDmV4eK1l7uQOAGhkWHYWEBIFwU0Utob_1K9HQD6Vr0a; WEB=20111132; .AspNetCore.Antiforgery.VJ9V3gR6RkM=CfDJ8IsxmZmItZ9GiKs4EcN_vHFZHrJkrvC7wBsvjdbnwNIzG52zzpS-xkp2g44iu3BAjw3ovp3IbInvQetNZLXJwjpjW8o_UJtUphwnaafaHAx3tgY-cC57FtY4j1jJ4KQjUQhq2dAA45t-ygY58dZyirc; NOh8RTWx6K2dT=0vDdhp2vGMO7rXn8EVuvAmBu_Cwu7WspYWpPxcPp4rcJyI799e5iG1Dv4q.xah0cB3V.PgD0zR1eM0mbiPl67uQF6ndW9JXP5fAhfo9EihzTHzbSJgRx4Hvl.jMekzb.qFNg5qBtW9XWXjPOwUjAtuWHGLtyMXmM8KRK0x5djxtN8y3TF2bvAgcr1co9TJIQw0X9bX.ym2_.DGzV.iip8ytSA2q_cHKtObvTyz.Ic3AxWlFMgrX6ZD2YcBmdLITd.GhcTvJ.sdk_SSWU.TVWFSDLFpgGRQ5Xu3VHv15OZeE5qvCfWzO2ZwRQ.4WWPli0OPbYqbhbry53290AGb43LXOFbnewAB5XfJUC975JHH76vF6J_9Gjpc5K0N3oYaZGX1eMJOVbTPplz_FpkKRIoILdLoo6U7IIvhBJCFczpqdpTqKbFMXLXrN_3VYO6Zksd',
}

params = {
    'OWNRL2Cu': '0MzYbSqlqEqTH9zgNx.jWlaJ0PaexFfIt0uTgOwUBrzD_vIrxxsIYEHOZHQARA5yqh7XEJzqlstswKbtMnXxwME.YIeiitu2i',
}

data = {
    'searchCatalogInfo.Pubtype': '1',
    'searchCatalogInfo.Ggr_Begin': '',
    'searchCatalogInfo.Ggr_End': '',
    'searchCatalogInfo.Pd_Begin': '',
    'searchCatalogInfo.Pd_End': '',
    'searchCatalogInfo.An': '',
    'searchCatalogInfo.Pn': '',
    'searchCatalogInfo.Ad_Begin': '',
    'searchCatalogInfo.Ad_End': '',
    'searchCatalogInfo.E71_73': '小米科技有限责任公司',
    'searchCatalogInfo.E72': '小米科技有限责任公司',
    'searchCatalogInfo.Edz': '小米科技有限责任公司',
    'searchCatalogInfo.E51': '',
    'searchCatalogInfo.Ti': '小米科技有限责任公司',
    'searchCatalogInfo.Abs': '小米科技有限责任公司',
    'searchCatalogInfo.Edl': '小米科技有限责任公司',
    'searchCatalogInfo.E74': '小米科技有限责任公司',
    'searchCatalogInfo.E30': '',
    'searchCatalogInfo.E66': '',
    'searchCatalogInfo.E62': '',
    'searchCatalogInfo.E83': '',
    'searchCatalogInfo.E85': '',
    'searchCatalogInfo.E86': '',
    'searchCatalogInfo.E87': '',
    'pageModel.pageNum': '2',
    'pageModel.pageSize': '10',
    'sortFiled': 'ggr_desc',
    'searchAfter': '20200915;2020107294779',
    'showModel': '2',
    'isOr': 'True',
    '__RequestVerificationToken': 'CfDJ8IsxmZmItZ9GiKs4EcN_vHEoP8hT7zY7vSDAiJ_yWCD5P_71OKBuyE-V5YAELUUeT0AYM-PTUdvfdBwp-TTMAidSpoqCyPMkiFrzHd0i6LMsGArN-mP3tJVjY2-q-4djPF8B50-YVMQN72DgNIFLkLw',
}

response = requests.post(
    'http://epub.cnipa.gov.cn/Dxb/PageQuery',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
    verify=False,
)

print(response.content.decode('utf-8'))
