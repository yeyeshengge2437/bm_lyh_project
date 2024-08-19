import requests
from lxml import etree
import textwrap
from PIL import Image, ImageDraw, ImageFont


def main():
    url = "https://www.163.com/dy/media/T1603594732083.html"
    rsp = requests.get(url)
    html = etree.HTML(rsp.text)
    today_url = html.xpath("//h2[@class='media_article_title']/a/@href")[0]
    rsp = requests.get(today_url)
    html = etree.HTML(rsp.text)
    news_list = html.xpath("//div[@class='post_body']/p[2]//text()")
    news_list = news_list[1:]
    date = news_list[0]
    f = open(date + ".txt", "w")
    for news in news_list:
        # print(news)
        f.write(news + '\n')
    f.close()
    news_wrap = []  # 准备一个数组来装我们的结果集
    for line in news_list:  # 循环遍历数组中的每行文字，line是临时变量，指代当前所循环到的文字
        if len(line) < 25:  # 若字数大于4个且小于25个
            news_wrap.append(line)  # 添加到数组中
        else:  # 若字数大于25个字
            wrap = textwrap.wrap(line, 25)  # 按每行25个字分割成数组
            news_wrap = news_wrap + wrap  # 拼到结果数组中
    # print(news_wrap) # 分割后的数组打印出来看看

    IMG_SIZE = (900, len(news_wrap) * 44)  # 图片尺寸 900x新闻行数x每行行高
    img_1 = Image.new('RGB', IMG_SIZE, (255, 255, 255))  # 建一张新图，颜色用RGB，，底色三个255表示纯白
    draw = ImageDraw.Draw(img_1)  # 创建一个画笔

    header_position = (60, 30)  # 标题的横纵坐标位置
    header_font = ImageFont.truetype('simkai.ttf', 55)  # 标题的字体楷体，字号55
    draw.multiline_text(header_position, '互联网日报', '#726053', header_font)  # 入参分别是坐标，文字内容，文字色号，文字字体

    current_height = 80
    for line in news_wrap:
        if line.startswith('2022'):
            news_font = ImageFont.truetype('simkai.ttf', 35)  # 标题的字体楷体，字号50
            draw.text((60, current_height + 25), line, '#726053', news_font)
            current_height += 80
        else:
            news_font = ImageFont.truetype('simkai.ttf', 30)  # 新闻字体30
            draw.text((60, current_height), line, '#726053', news_font)
            current_height += 40

    img_1.show()  # 弹框展示图片
    img_1.save(date + '.jpg')  # 保存成文件


if __name__ == "__main__":
    main()

# 一个学生物的编程爱好者！
