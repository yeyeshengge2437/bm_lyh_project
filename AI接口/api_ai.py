import re

import requests


def img_url_to_fail(image_url):
    # 图片的URL
    image_url = image_url
    image_url = re.sub(r'\?.*', '', image_url)
    # 请求头部，有些网站可能需要User-Agent来模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 发送GET请求
    response = requests.get(image_url, headers=headers)

    # 确保请求成功
    if response.status_code == 200:
        # 图片的文件名
        filename = image_url.split('/')[-1]

        # 打开一个文件来写入图片数据
        with open(filename, 'wb') as f:
            # 写入请求回来的图片数据
            f.write(response.content)

        return filename
    else:
        raise Exception('下载图像失败')

# img_url_to_fail('https://res.debtop.com/manage/live/paper/202410/24/20241024110628f369258f291548b9.png?x-oss-process=image/resize,m_fixed,w_64/quality,Q_5')