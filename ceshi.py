import requests

cookies = {
    'zycna': 'CBuEnko+IykBAbeApvyz0wcQ',
    'HKIIUU9O618PPTHK': '2015be9f8fe7c26a9139029a4aec544c7e64952',
    'HKIIUU9O618PPTHP': 'MTczMTA0zMTExMjI5RFVyazFranBrVDRHa28xZDBEbTBsRDF5YzMxZj3h3MENqR0U0d21oMzV5czg2MzNqbjdLMXAIzMlMwNVk0b2jdyMHdaMzVm2U0g783WMDBzTTMx2SzZBRa21nNnZuNWNEM0M1ZzFmdHIyZzUzNjJ3Y3ZTajgzMWJnNjF4Zm4yMkE1Zzk3N0t3Sm1xOWw2bzNoemtaRzFuWXBrM2dmbjNsb2loODUwcG03OGtIMzQzbGd1S1kxa2gyU253MTExMEZZMTExbTUweXdIMGJIdDExMTY1YWtuU0EwbEFtNWc1MTExcGZnMEFZbTMyam9sQTZoZXlKdGIzVnpaWGdpT2lJeE1EQXdNQ0lzSW0xdmRYTmxlU0k2SWpFd01EQXdJaXdpYzJOeVpXVnVkeUk2SWpFd01EQXdJaXdpYzJOeVpXVnVhQ0k2SWpFd01EQXdJaXdpYm05b1pXRmtaWElpT2lKdWJ5SXNJbTV2YldGc0lqb2llV1Z6SWl3aVlXcGhlQ0k2SW1GaFlXRmhJaXdpYm05M1gzVnVhWEYxWlNJNklqSXdNVFZpWlRsbU9HWmxOMk15Tm1FNU1UTTVNREk1WVRSaFpXTTFORFJqTjJVMk5EazFNaUlzSW5Ob1pXSmxhU0k2SWxkbFlpSXNJbTVoZG1sbllYUnZjaUk2SWlJc0luVjFhV1JmWm1seGRYSmxJam9pT0RobU4yVTRaRGRpWVdZM1pHWXlOekV5TkRFeU9UQXlOVEJsWXpCbFpUVWlmUT09',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'zycna=CBuEnko+IykBAbeApvyz0wcQ; HKIIUU9O618PPTHK=2015be9f8fe7c26a9139029a4aec544c7e64952; HKIIUU9O618PPTHP=MTczMTA0zMTExMjI5RFVyazFranBrVDRHa28xZDBEbTBsRDF5YzMxZj3h3MENqR0U0d21oMzV5czg2MzNqbjdLMXAIzMlMwNVk0b2jdyMHdaMzVm2U0g783WMDBzTTMx2SzZBRa21nNnZuNWNEM0M1ZzFmdHIyZzUzNjJ3Y3ZTajgzMWJnNjF4Zm4yMkE1Zzk3N0t3Sm1xOWw2bzNoemtaRzFuWXBrM2dmbjNsb2loODUwcG03OGtIMzQzbGd1S1kxa2gyU253MTExMEZZMTExbTUweXdIMGJIdDExMTY1YWtuU0EwbEFtNWc1MTExcGZnMEFZbTMyam9sQTZoZXlKdGIzVnpaWGdpT2lJeE1EQXdNQ0lzSW0xdmRYTmxlU0k2SWpFd01EQXdJaXdpYzJOeVpXVnVkeUk2SWpFd01EQXdJaXdpYzJOeVpXVnVhQ0k2SWpFd01EQXdJaXdpYm05b1pXRmtaWElpT2lKdWJ5SXNJbTV2YldGc0lqb2llV1Z6SWl3aVlXcGhlQ0k2SW1GaFlXRmhJaXdpYm05M1gzVnVhWEYxWlNJNklqSXdNVFZpWlRsbU9HWmxOMk15Tm1FNU1UTTVNREk1WVRSaFpXTTFORFJqTjJVMk5EazFNaUlzSW5Ob1pXSmxhU0k2SWxkbFlpSXNJbTVoZG1sbllYUnZjaUk2SWlJc0luVjFhV1JmWm1seGRYSmxJam9pT0RobU4yVTRaRGRpWVdZM1pHWXlOekV5TkRFeU9UQXlOVEJsWXpCbFpUVWlmUT09',
    'Pragma': 'no-cache',
    'Referer': 'http://epaper.legaldaily.com.cn/fzrb/content/20230530/Page12TB.htm',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

response = requests.get(
    'http://epaper.legaldaily.com.cn/fzrb/content/20230530/Page12TB.htm',
    cookies=cookies,
    headers=headers,
    verify=False,
)
print(response.text)