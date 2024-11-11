import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "民主与法制时报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'Hm_lvt_ed99d6775c7b858980121339c3b0e9b2=1724382404; wdcid=3575e079127b923b; acw_tc=1a0c385017284615524802696e010fe95aa5ba806c4316eda00235e195882a; ASPSESSIONIDSCTQTTAR=JPNHNJBDJDAJMHBFCPNCHKGO; Hm_lvt_3e597a6899c3536f12f0b7645abb597b=1728461553; Hm_lpvt_3e597a6899c3536f12f0b7645abb597b=1728461553; HMACCOUNT=FDD970C8B3C27398',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

date_dict = {'2024-10-09': 'http://e.mzyfz.com/paper/index_2300.html', '2024-10-01': 'http://e.mzyfz.com/paper/index_2301.html', '2024-09-27': 'http://e.mzyfz.com/paper/index_2299.html', '2024-09-26': 'http://e.mzyfz.com/paper/index_2298.html', '2024-09-25': 'http://e.mzyfz.com/paper/index_2297.html', '2024-09-24': 'http://e.mzyfz.com/paper/index_2296.html', '2024-09-20': 'http://e.mzyfz.com/paper/index_2295.html', '2024-09-19': 'http://e.mzyfz.com/paper/index_2294.html', '2024-09-13': 'http://e.mzyfz.com/paper/index_2293.html', '2024-09-12': 'http://e.mzyfz.com/paper/index_2292.html', '2024-09-11': 'http://e.mzyfz.com/paper/index_2291.html', '2024-09-10': 'http://e.mzyfz.com/paper/index_2290.html', '2024-09-06': 'http://e.mzyfz.com/paper/index_2289.html', '2024-09-05': 'http://e.mzyfz.com/paper/index_2288.html', '2024-09-04': 'http://e.mzyfz.com/paper/index_2287.html', '2024-09-03': 'http://e.mzyfz.com/paper/index_2286.html', '2024-08-30': 'http://e.mzyfz.com/paper/index_2285.html', '2024-08-29': 'http://e.mzyfz.com/paper/index_2284.html', '2024-08-28': 'http://e.mzyfz.com/paper/index_2283.html', '2024-08-27': 'http://e.mzyfz.com/paper/index_2282.html', '2024-08-23': 'http://e.mzyfz.com/paper/index_2281.html', '2024-08-22': 'http://e.mzyfz.com/paper/index_2280.html', '2024-08-21': 'http://e.mzyfz.com/paper/index_2279.html', '2024-08-20': 'http://e.mzyfz.com/paper/index_2278.html', '2024-08-16': 'http://e.mzyfz.com/paper/index_2277.html', '2024-08-15': 'http://e.mzyfz.com/paper/index_2276.html', '2024-08-14': 'http://e.mzyfz.com/paper/index_2275.html', '2024-08-13': 'http://e.mzyfz.com/paper/index_2274.html', '2024-08-09': 'http://e.mzyfz.com/paper/index_2273.html', '2024-08-08': 'http://e.mzyfz.com/paper/index_2272.html', '2024-08-07': 'http://e.mzyfz.com/paper/index_2271.html', '2024-08-06': 'http://e.mzyfz.com/paper/index_2270.html', '2024-08-02': 'http://e.mzyfz.com/paper/index_2269.html', '2024-08-01': 'http://e.mzyfz.com/paper/index_2268.html', '2024-07-31': 'http://e.mzyfz.com/paper/index_2267.html', '2024-07-30': 'http://e.mzyfz.com/paper/index_2266.html', '2024-07-26': 'http://e.mzyfz.com/paper/index_2265.html', '2024-07-25': 'http://e.mzyfz.com/paper/index_2264.html', '2024-07-24': 'http://e.mzyfz.com/paper/index_2263.html', '2024-07-23': 'http://e.mzyfz.com/paper/index_2262.html', '2024-07-19': 'http://e.mzyfz.com/paper/index_2261.html', '2024-07-18': 'http://e.mzyfz.com/paper/index_2260.html', '2024-07-17': 'http://e.mzyfz.com/paper/index_2259.html', '2024-07-16': 'http://e.mzyfz.com/paper/index_2258.html', '2024-07-12': 'http://e.mzyfz.com/paper/index_2257.html', '2024-07-11': 'http://e.mzyfz.com/paper/index_2256.html', '2024-07-10': 'http://e.mzyfz.com/paper/index_2255.html', '2024-07-09': 'http://e.mzyfz.com/paper/index_2254.html', '2024-07-05': 'http://e.mzyfz.com/paper/index_2253.html', '2024-07-04': 'http://e.mzyfz.com/paper/index_2252.html', '2024-07-03': 'http://e.mzyfz.com/paper/index_2251.html', '2024-07-02': 'http://e.mzyfz.com/paper/index_2250.html', '2024-06-28': 'http://e.mzyfz.com/paper/index_2249.html', '2024-06-27': 'http://e.mzyfz.com/paper/index_2248.html', '2024-06-26': 'http://e.mzyfz.com/paper/index_2247.html', '2024-06-25': 'http://e.mzyfz.com/paper/index_2246.html', '2024-06-21': 'http://e.mzyfz.com/paper/index_2245.html', '2024-06-20': 'http://e.mzyfz.com/paper/index_2244.html', '2024-06-19': 'http://e.mzyfz.com/paper/index_2243.html', '2024-06-18': 'http://e.mzyfz.com/paper/index_2242.html', '2024-06-14': 'http://e.mzyfz.com/paper/index_2241.html', '2024-06-13': 'http://e.mzyfz.com/paper/index_2240.html', '2024-06-12': 'http://e.mzyfz.com/paper/index_2239.html', '2024-06-07': 'http://e.mzyfz.com/paper/index_2238.html', '2024-06-06': 'http://e.mzyfz.com/paper/index_2237.html', '2024-06-05': 'http://e.mzyfz.com/paper/index_2236.html', '2024-06-04': 'http://e.mzyfz.com/paper/index_2235.html', '2024-05-31': 'http://e.mzyfz.com/paper/index_2234.html', '2024-05-30': 'http://e.mzyfz.com/paper/index_2233.html', '2024-05-29': 'http://e.mzyfz.com/paper/index_2232.html', '2024-05-28': 'http://e.mzyfz.com/paper/index_2231.html', '2024-05-24': 'http://e.mzyfz.com/paper/index_2230.html', '2024-05-23': 'http://e.mzyfz.com/paper/index_2229.html', '2024-05-22': 'http://e.mzyfz.com/paper/index_2228.html', '2024-05-21': 'http://e.mzyfz.com/paper/index_2227.html', '2024-05-17': 'http://e.mzyfz.com/paper/index_2226.html', '2024-05-16': 'http://e.mzyfz.com/paper/index_2225.html', '2024-05-15': 'http://e.mzyfz.com/paper/index_2224.html', '2024-05-14': 'http://e.mzyfz.com/paper/index_2223.html', '2024-05-10': 'http://e.mzyfz.com/paper/index_2222.html', '2024-05-09': 'http://e.mzyfz.com/paper/index_2221.html', '2024-05-08': 'http://e.mzyfz.com/paper/index_2220.html', '2024-05-07': 'http://e.mzyfz.com/paper/index_2219.html', '2024-04-30': 'http://e.mzyfz.com/paper/index_2218.html', '2024-04-26': 'http://e.mzyfz.com/paper/index_2217.html', '2024-04-25': 'http://e.mzyfz.com/paper/index_2216.html', '2024-04-24': 'http://e.mzyfz.com/paper/index_2215.html', '2024-04-23': 'http://e.mzyfz.com/paper/index_2214.html', '2024-04-19': 'http://e.mzyfz.com/paper/index_2213.html', '2024-04-18': 'http://e.mzyfz.com/paper/index_2212.html', '2024-04-17': 'http://e.mzyfz.com/paper/index_2211.html', '2024-04-16': 'http://e.mzyfz.com/paper/index_2210.html', '2024-04-12': 'http://e.mzyfz.com/paper/index_2209.html', '2024-04-11': 'http://e.mzyfz.com/paper/index_2208.html', '2024-04-10': 'http://e.mzyfz.com/paper/index_2207.html', '2024-04-09': 'http://e.mzyfz.com/paper/index_2206.html', '2024-04-04': 'http://e.mzyfz.com/paper/index_2205.html', '2024-04-03': 'http://e.mzyfz.com/paper/index_2204.html', '2024-04-02': 'http://e.mzyfz.com/paper/index_2203.html', '2024-03-29': 'http://e.mzyfz.com/paper/index_2202.html', '2024-03-28': 'http://e.mzyfz.com/paper/index_2201.html', '2024-03-27': 'http://e.mzyfz.com/paper/index_2200.html', '2024-03-26': 'http://e.mzyfz.com/paper/index_2199.html', '2024-03-22': 'http://e.mzyfz.com/paper/index_2198.html', '2024-03-21': 'http://e.mzyfz.com/paper/index_2197.html', '2024-03-20': 'http://e.mzyfz.com/paper/index_2196.html', '2024-03-19': 'http://e.mzyfz.com/paper/index_2195.html', '2024-03-15': 'http://e.mzyfz.com/paper/index_2194.html', '2024-03-14': 'http://e.mzyfz.com/paper/index_2193.html', '2024-03-13': 'http://e.mzyfz.com/paper/index_2192.html', '2024-03-12': 'http://e.mzyfz.com/paper/index_2191.html', '2024-03-08': 'http://e.mzyfz.com/paper/index_2190.html', '2024-03-07': 'http://e.mzyfz.com/paper/index_2189.html', '2024-03-06': 'http://e.mzyfz.com/paper/index_2188.html', '2024-03-05': 'http://e.mzyfz.com/paper/index_2187.html', '2024-03-01': 'http://e.mzyfz.com/paper/index_2186.html', '2024-02-29': 'http://e.mzyfz.com/paper/index_2185.html', '2024-02-28': 'http://e.mzyfz.com/paper/index_2184.html', '2024-02-27': 'http://e.mzyfz.com/paper/index_2183.html', '2024-02-23': 'http://e.mzyfz.com/paper/index_2182.html', '2024-02-22': 'http://e.mzyfz.com/paper/index_2181.html', '2024-02-21': 'http://e.mzyfz.com/paper/index_2180.html', '2024-02-20': 'http://e.mzyfz.com/paper/index_2179.html', '2024-02-08': 'http://e.mzyfz.com/paper/index_2178.html', '2024-02-07': 'http://e.mzyfz.com/paper/index_2177.html', '2024-02-06': 'http://e.mzyfz.com/paper/index_2176.html', '2024-02-02': 'http://e.mzyfz.com/paper/index_2175.html', '2024-02-01': 'http://e.mzyfz.com/paper/index_2174.html', '2024-01-31': 'http://e.mzyfz.com/paper/index_2173.html', '2024-01-30': 'http://e.mzyfz.com/paper/index_2172.html', '2024-01-26': 'http://e.mzyfz.com/paper/index_2171.html', '2024-01-25': 'http://e.mzyfz.com/paper/index_2170.html', '2024-01-24': 'http://e.mzyfz.com/paper/index_2169.html', '2024-01-23': 'http://e.mzyfz.com/paper/index_2168.html', '2024-01-19': 'http://e.mzyfz.com/paper/index_2167.html', '2024-01-18': 'http://e.mzyfz.com/paper/index_2166.html', '2024-01-17': 'http://e.mzyfz.com/paper/index_2165.html', '2024-01-16': 'http://e.mzyfz.com/paper/index_2164.html', '2024-01-12': 'http://e.mzyfz.com/paper/index_2163.html', '2024-01-11': 'http://e.mzyfz.com/paper/index_2162.html', '2024-01-10': 'http://e.mzyfz.com/paper/index_2161.html', '2024-01-09': 'http://e.mzyfz.com/paper/index_2160.html', '2024-01-05': 'http://e.mzyfz.com/paper/index_2159.html', '2024-01-04': 'http://e.mzyfz.com/paper/index_2158.html', '2024-01-03': 'http://e.mzyfz.com/paper/index_2157.html', '2023-12-29': 'http://e.mzyfz.com/paper/index_2156.html', '2023-12-28': 'http://e.mzyfz.com/paper/index_2155.html', '2023-12-27': 'http://e.mzyfz.com/paper/index_2154.html', '2023-12-26': 'http://e.mzyfz.com/paper/index_2153.html', '2023-12-22': 'http://e.mzyfz.com/paper/index_2152.html', '2023-12-21': 'http://e.mzyfz.com/paper/index_2151.html', '2023-12-20': 'http://e.mzyfz.com/paper/index_2150.html', '2023-12-19': 'http://e.mzyfz.com/paper/index_2149.html', '2023-12-15': 'http://e.mzyfz.com/paper/index_2148.html', '2023-12-14': 'http://e.mzyfz.com/paper/index_2147.html', '2023-12-13': 'http://e.mzyfz.com/paper/index_2146.html', '2023-12-12': 'http://e.mzyfz.com/paper/index_2145.html', '2023-12-08': 'http://e.mzyfz.com/paper/index_2144.html', '2023-12-07': 'http://e.mzyfz.com/paper/index_2143.html', '2023-12-06': 'http://e.mzyfz.com/paper/index_2142.html', '2023-12-05': 'http://e.mzyfz.com/paper/index_2141.html', '2023-12-01': 'http://e.mzyfz.com/paper/index_2140.html', '2023-11-30': 'http://e.mzyfz.com/paper/index_2139.html', '2023-11-29': 'http://e.mzyfz.com/paper/index_2138.html', '2023-11-28': 'http://e.mzyfz.com/paper/index_2137.html', '2023-11-24': 'http://e.mzyfz.com/paper/index_2136.html', '2023-11-23': 'http://e.mzyfz.com/paper/index_2135.html', '2023-11-22': 'http://e.mzyfz.com/paper/index_2134.html', '2023-11-21': 'http://e.mzyfz.com/paper/index_2133.html', '2023-11-17': 'http://e.mzyfz.com/paper/index_2132.html', '2023-11-16': 'http://e.mzyfz.com/paper/index_2131.html', '2023-11-15': 'http://e.mzyfz.com/paper/index_2130.html', '2023-11-14': 'http://e.mzyfz.com/paper/index_2129.html', '2023-11-10': 'http://e.mzyfz.com/paper/index_2128.html', '2023-11-09': 'http://e.mzyfz.com/paper/index_2127.html', '2023-11-08': 'http://e.mzyfz.com/paper/index_2126.html', '2023-11-07': 'http://e.mzyfz.com/paper/index_2125.html', '2023-11-03': 'http://e.mzyfz.com/paper/index_2124.html', '2023-11-02': 'http://e.mzyfz.com/paper/index_2123.html', '2023-11-01': 'http://e.mzyfz.com/paper/index_2122.html', '2023-10-31': 'http://e.mzyfz.com/paper/index_2121.html', '2023-10-27': 'http://e.mzyfz.com/paper/index_2120.html', '2023-10-26': 'http://e.mzyfz.com/paper/index_2119.html', '2023-10-25': 'http://e.mzyfz.com/paper/index_2118.html', '2023-10-24': 'http://e.mzyfz.com/paper/index_2117.html', '2023-10-20': 'http://e.mzyfz.com/paper/index_2116.html', '2023-10-19': 'http://e.mzyfz.com/paper/index_2115.html', '2023-10-18': 'http://e.mzyfz.com/paper/index_2114.html', '2023-10-17': 'http://e.mzyfz.com/paper/index_2113.html', '2023-10-13': 'http://e.mzyfz.com/paper/index_2112.html', '2023-10-12': 'http://e.mzyfz.com/paper/index_2111.html', '2023-10-11': 'http://e.mzyfz.com/paper/index_2110.html', '2023-10-10': 'http://e.mzyfz.com/paper/index_2109.html', '2023-09-28': 'http://e.mzyfz.com/paper/index_2108.html', '2023-09-27': 'http://e.mzyfz.com/paper/index_2107.html', '2023-09-26': 'http://e.mzyfz.com/paper/index_2106.html', '2023-09-22': 'http://e.mzyfz.com/paper/index_2105.html', '2023-09-21': 'http://e.mzyfz.com/paper/index_2104.html', '2023-09-20': 'http://e.mzyfz.com/paper/index_2103.html', '2023-09-19': 'http://e.mzyfz.com/paper/index_2102.html', '2023-09-15': 'http://e.mzyfz.com/paper/index_2101.html', '2023-09-14': 'http://e.mzyfz.com/paper/index_2100.html', '2023-09-13': 'http://e.mzyfz.com/paper/index_2099.html', '2023-09-12': 'http://e.mzyfz.com/paper/index_2098.html', '2023-09-08': 'http://e.mzyfz.com/paper/index_2097.html', '2023-09-07': 'http://e.mzyfz.com/paper/index_2096.html', '2023-09-06': 'http://e.mzyfz.com/paper/index_2095.html', '2023-09-05': 'http://e.mzyfz.com/paper/index_2094.html', '2023-09-01': 'http://e.mzyfz.com/paper/index_2093.html', '2023-08-31': 'http://e.mzyfz.com/paper/index_2092.html', '2023-08-30': 'http://e.mzyfz.com/paper/index_2091.html', '2023-08-29': 'http://e.mzyfz.com/paper/index_2090.html', '2023-08-25': 'http://e.mzyfz.com/paper/index_2089.html', '2023-08-24': 'http://e.mzyfz.com/paper/index_2088.html', '2023-08-23': 'http://e.mzyfz.com/paper/index_2087.html', '2023-08-22': 'http://e.mzyfz.com/paper/index_2086.html', '2023-08-18': 'http://e.mzyfz.com/paper/index_2085.html', '2023-08-17': 'http://e.mzyfz.com/paper/index_2084.html', '2023-08-16': 'http://e.mzyfz.com/paper/index_2083.html', '2023-08-15': 'http://e.mzyfz.com/paper/index_2082.html', '2023-08-11': 'http://e.mzyfz.com/paper/index_2081.html', '2023-08-10': 'http://e.mzyfz.com/paper/index_2080.html', '2023-08-09': 'http://e.mzyfz.com/paper/index_2079.html', '2023-08-08': 'http://e.mzyfz.com/paper/index_2078.html', '2023-08-04': 'http://e.mzyfz.com/paper/index_2077.html', '2023-08-03': 'http://e.mzyfz.com/paper/index_2076.html', '2023-08-02': 'http://e.mzyfz.com/paper/index_2075.html', '2023-08-01': 'http://e.mzyfz.com/paper/index_2074.html', '2023-07-28': 'http://e.mzyfz.com/paper/index_2073.html', '2023-07-27': 'http://e.mzyfz.com/paper/index_2072.html', '2023-07-26': 'http://e.mzyfz.com/paper/index_2071.html', '2023-07-25': 'http://e.mzyfz.com/paper/index_2070.html', '2023-07-21': 'http://e.mzyfz.com/paper/index_2069.html', '2023-07-20': 'http://e.mzyfz.com/paper/index_2068.html', '2023-07-19': 'http://e.mzyfz.com/paper/index_2067.html', '2023-07-18': 'http://e.mzyfz.com/paper/index_2066.html', '2023-07-14': 'http://e.mzyfz.com/paper/index_2065.html', '2023-07-13': 'http://e.mzyfz.com/paper/index_2064.html', '2023-07-12': 'http://e.mzyfz.com/paper/index_2063.html', '2023-07-11': 'http://e.mzyfz.com/paper/index_2062.html'}

def get_date():
    for i in range(1, 2 + 1):
        data = {
            'page': f'{i}',
        }

        response = requests.post('http://e.mzyfz.com/paper/review.html', headers=headers, data=data,
                                 verify=False)
        if response.status_code == 200:
            content = response.content.decode('gbk')
            html_1 = etree.HTML(content)
            dates = html_1.xpath("//div[@class='review_list']/ul/li")
            for date in dates:
                date_url = "http://e.mzyfz.com/paper/" + "".join(date.xpath("./p/a/@href")).strip()
                date_str = "".join(date.xpath("./span/a/text()")).strip()
                date_time = re.findall(r'\d{4}-\d{1,2}-\d{1,2}', date_str)[0]
                if date_time not in date_dict:
                    date_dict[date_time] = date_url
    return date_dict

def get_minzhuyufazhi_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    get_date()
    if date_dict.get(paper_time) is None:
        raise Exception(f'该日期没有报纸')
    url = date_dict[paper_time]
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        content = response.content.decode('gbk')
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//div[@id='index_f_list']/ul/li")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./a/text()")).strip()
            # 版面链接
            bm_url = 'http://e.mzyfz.com' + ''.join(bm.xpath("./a/@href"))
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            bm_content = bm_response.content.decode('gbk')
            bm_html = etree.HTML(bm_content)
            # 版面的pdf
            bm_pdf = None

            # 获取所有文章的链接
            all_article = bm_html.xpath("//div[@id='index_a_list']/ul/li/a")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = 'http://e.mzyfz.com' + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./text()")).strip()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                article_content = article_response.content.decode('gbk')
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//div[@id='Zoom']/p/text()")).strip()
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                cursor_test = conn_test.cursor()
                # print(bm_name, article_name, article_url, bm_pdf, content)
                if judging_criteria(article_name, content):
                    # 将报纸url上传
                    up_pdf = None
                    pdf_set.add(bm_pdf)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if judging_criteria(article_name, content):
                # if 1:

                    # print(content)
                    # return

                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                cursor_test.close()
                conn_test.close()


        success_data = {
            'id': queue_id,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)

    else:
        raise Exception(f'该日期没有报纸')


# get_minzhuyufazhi_paper('2024-10-09', 111, 1111)
