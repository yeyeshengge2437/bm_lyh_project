import json
import re
import requests
import mysql.connector

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False

produce_url = "http://118.31.45.18:29810"


def img_url_to_file(image_url):
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


def ai_parse_next(data=None):
    headers = {
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    data_str = json.dumps(data, ensure_ascii=False)
    url = produce_url + "/inner-api/paper-deal/tell-queue/next"
    response = s.post(url, headers=headers, data=data_str)
    result = response.json()
    print(result)
    return result.get("value")


# 实例
"""
data = {
    'tell_tool_list': [
                       "kimi_8k-kimi文本理解",
                       "kimi_32k-kimi图片理解",
                       "glm_4_air-智谱文本理解",
                       "glm_4v_plus-智谱图片理解"
                       ]
}
"""


def ai_parse_success(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = produce_url + "/inner-api/paper-deal/tell-queue/success"
    data_str = json.dumps(data, ensure_ascii=False)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result


# 实例
"""
data = {
    'id' : '1',
    'remark' : '哪个AI',
    'input_token_num' : '输入token数',
    'output_token_num' : '输出token数',
    'output_text' : '输出',
    }
"""


def ai_parse_fail(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = produce_url + "/inner-api/paper-deal/tell-queue/fail"
    data_str = json.dumps(data, ensure_ascii=False)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result


# 实例
"""
data = {
    'id' : '1',
    'remark' : '识别失败'
    }
"""


def str_to_list(value):
    value = value.replace("'", '"')
    value = json.loads(value)
    return value


def list_is_resaved():
    """
    将数据库中为列表的依次插入
    :return:
    """
    conn_test = mysql.connector.connect(
        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col",
    )
    cursor_test = conn_test.cursor()
    cursor_test.execute(
        "select id, name, former_name, gender, id_num, address, role, company, office, relationship, asset, is_died, other, create_time, from_id, paper_id, input_key from col_paper_people")
    rows = cursor_test.fetchall()
    for id, name, former_name, gender, id_num, address, role, company, office, relationship, asset, is_died, other, create_time, from_id, paper_id, input_key in rows:
        # print(name, type(name))
        name = name.replace("'", '"')
        # print(name, type(name))
        try:
            name = json.loads(name)
            if isinstance(name, list):
                former_name = str_to_list(former_name)
                gender = str_to_list(gender)
                id_num = str_to_list(id_num)
                address = str_to_list(address)
                role = str_to_list(role)
                company = str_to_list(company)
                office = str_to_list(office)
                relationship = str_to_list(relationship)
                asset = str_to_list(asset)
                is_died = str_to_list(is_died)
                other = str_to_list(other)
                # 将所有变量放入一个列表中
                variables = [name, former_name, gender, id_num, address, role, company, office, relationship, asset,
                             is_died, other]

                # 获取第一个变量的长度
                first_length = len(variables[0])

                # 检查所有变量的长度是否与第一个变量的长度相等
                all_lengths_equal = all(len(var) == first_length for var in variables)

                if all_lengths_equal:
                    for i in range(first_length):
                        # 遍历到每个列表的值
                        insert_sql = "INSERT INTO col_paper_people (name, former_name, gender, id_num, address, role, company, office, relationship, asset, is_died, other,create_time, from_id, paper_id, input_key) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        cursor_test.execute(insert_sql, (name[i], former_name[i], gender[i], id_num[i], address[i], role[i], company[i], office[i], relationship[i], asset[i], is_died[i], other[i], create_time, from_id, paper_id, input_key))
                    conn_test.commit()
                    # 删除原数据
                    delete_sql = "DELETE FROM col_paper_people WHERE id = %s"
                    cursor_test.execute(delete_sql, (id,))
                    conn_test.commit()
                else:
                    print("至少有一个变量的长度不相等")

        except:
            pass

    cursor_test.close()
    conn_test.close()


# list_is_resaved()
