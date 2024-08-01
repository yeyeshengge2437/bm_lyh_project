import re


ignore_str = "(法\\s*院\\s*公\\s*告|减\\s*资\\s*公\\s*告|注\\s*销\\s*公\\s*告|清\\s*算\\s*公\\s*告|合\\s*并\\s*公\\s*告" \
             "|出\\s*让\\s*公\\s*告|重\\s*组\\s*公\\s*告|调\\s*查\\s*公\\s*告|分\\s*立\\s*公\\s*告|重\\s*整\\s*公\\s*告" \
             "|悬\\s*赏\\s*公\\s*告|注\\s*销\\s*登\\s*记\\s*公\\s*告)"


# 移除空字符
def remove_empty(content):
    if content is None:
        return ""
    return re.sub("[\\s]*", "", content)


# 移除html标签
def remove_html(content):
    return re.sub("<[^>]*>", "", content)


# 判断是否为日期
def check_day(content):
    if re.search("^\\d{4}-\\d{2}-\\d{2}$", content) is not None:
        return True
    return False


# 公告或声明数量
def notice_num(content):
    _list = re.findall("(公\\s*告|通\\s*知|通\\s*知\\s*书|告\\s*知\\s*书|声\\s*明)(\\n|\\s{3})", content)
    return len(_list)


# 判断是否为债权公告
def title_check_notice(content):
    if re.search("(债\\s*权|转\\s*让|受\\s*让|处\\s*置|招\\s*商|营\\s*销|信\\s*息|联\\s*合|催\\s*收|催\\s*讨)\\s*的?"
                 "(公\\s*告|通\\s*知|通\\s*知\\s*书|告\\s*知\\s*书|通\\s*知\\s*公\\s*告|登\\s*报\\s*公\\s*告"
                 "|补\\s*登\\s*公\\s*告|补\\s*充\\s*公\\s*告|拍\\s*卖\\s*公\\s*告)", content) is not None:
        return True
    return False


# 判断是否为债权公告
def check_notice2(content):
    if re.search("债\\s*权|债\\s*务|借\\s*款|催\\s*收", content) is None:
        return False
    if re.search("公\\s*告|通\\s*知", content) is None:
        return False
    return True


# 判断标题是否属于需要忽略的公告
def title_check_ignore_notice(title):
    if re.search(ignore_str,
                 title) is not None:
        return True
    return False


# # 判断是否为债权公告
# def check_notice_by_content(content):
#     if re.search("(债\\s*权|转\\s*让|处\\s*置|招\\s*商|营\\s*销|信\\s*息|联\\s*合|催\\s*收|催\\s*讨|补\\s*充)\\s*的?"
#                  "(公\\s*告|通\\s*知|通\\s*知\\s*书|通\\s*知\\s*公\\s*告)", content) is not None:
#         return True
#     return False


# 判断是否可能债权公告
def may_notice_by_title(title):
    if title_check_ignore_notice(title):
        return False
    if re.search("(公\\s*告|无\\s*标\\s*题|广\\s*告)", title) is not None:
        return True
    return False


# 判断内容是否包含公告类标题
def content_check_title(content):
    if re.search("(公\\s*告|通\\s*知|通\\s*知\\s*书|通\\s*知\\s*函|声\\s*明)(\\n|\\s{3})", content) is not None:
        return True
    return False


# 判断内容是否包含需要忽略的公告标题
def content_check_ignore_notice(content):
    if re.search(ignore_str + "(\\n|\\s{3})", content) is not None:
        return True
    return False


def generate_url(url, href, with_param=False):
    if href is None or href == "":
        return ""
    if href.startswith("http://") or href.startswith("https://"):
        return href
    if url is None or url == "":
        return ""
    href_param = ""
    if url.startswith("http://"):
        pre = "http://"
    elif url.startswith("https://"):
        pre = "https://"
    else:
        return ""
    url = url.replace(pre, "", 1)
    if url.find("?") >= 0:
        url = url[0: url.find("?")]
    if url.find("#") >= 0:
        url = url[0: url.find("#")]
    if href.startswith("./"):
        href = href.replace("./", "", 1)
    if href.startswith("/"):
        if url.find("/") > 0:
            url = url[0: url.find("/")]
        return pre + url + href

    if href.find("?") >= 0:
        href_param = href[href.find("?"): len(href)]
        href = href[0: href.find("?")]
    if href.startswith("/"):
        if url.find("/") > 0:
            url = url[0: url.find("/")]
        result = pre + url + href
        if with_param:
            result = result + href_param
        return result

    if url.rfind("/") >= 0:
        url = url[0: url.rfind("/")]
    while href.startswith("../"):
        if url.rfind("/") >= 0:
            url = url[0: url.rfind("/")]
        href = href.replace("../", "", 1)
    result = pre + url + "/" + href
    if with_param:
        result = result + href_param
    return result



