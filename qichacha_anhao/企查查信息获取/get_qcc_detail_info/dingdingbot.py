import requests


def dd_program_abnormal(title=None, msg=None):
    """
    向钉钉群中发送程序异常信息
    :param title: 标题
    :param msg: 错误内容
    :return:
    """
    headers = {
        'Content-Type': 'application/json',
    }
    params = {
        'access_token': 'e6d8a6d0abf1119ad2eaad5ba06ef461ab609ca2594b969a8a1a4bc619d56329',
    }
    json_data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "程序异常",
            "text": f"### 🚨 程序异常告警 \n\n\n**▎程序名称** \n\n{title}\n\n**▎错误原因** \n\n{msg}"
        },
        "at": {
            "atMobiles": [
                "15938554242"
            ],
            "isAtAll": False
        },
    }
    response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data)
    return response.json()


def dd_ip_address_error(title=None, msg=None):
    """
    向钉钉群中发送ip异常信息
    :param title:标题
    :param msg:
    :return:
    """
    headers = {
        'Content-Type': 'application/json',
    }
    params = {
        'access_token': 'e6d8a6d0abf1119ad2eaad5ba06ef461ab609ca2594b969a8a1a4bc619d56329',
    }
    json_data = {
        'msgtype': 'text',
        'text': {
            'content': f"### 🚨 ip地址错误 \n\n\n**▎程序名称** \n\n{title}\n\n",
        },
        "at": {
            "atMobiles": [
            ],
            "isAtAll": False
        },
    }
    response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data)
    return response.json()


def dd_access_overrun(title=None, msg=None):
    """
    向钉钉中发送访问超频信息
    :param title: 标题
    :param msg: 错误信息
    :return:
    """
    headers = {
        'Content-Type': 'application/json',
    }
    params = {
        'access_token': 'e6d8a6d0abf1119ad2eaad5ba06ef461ab609ca2594b969a8a1a4bc619d56329',
    }
    json_data = {
        'msgtype': 'text',
        'text': {
            'content': f"### 🚨 访问超限 \n\n\n**▎程序名称** \n\n{title}\n\n**▎错误原因** \n\n{msg}",
        },
        "at": {
            "atMobiles": [
                "15938554242"
            ],
            "isAtAll": False
        },
    }
    response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data)
    return response.json()



