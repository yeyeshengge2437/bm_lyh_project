import requests


def verify_slider(base_64_data):
    """
    :param base_64_data: 图片的base64信息
    :return:
    """
    data = {
        "token": "2ika9NoqfOHBDPiYyFLISqQSi1HFrw49IBYYC5uWTm8",
        "type": "22222",
        "image": base_64_data,
        "extra": '',
    }
    url = "http://api.jfbym.com/api/YmServer/customApi"
    _headers = {
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=_headers, json=data).json()
    return response


def verify_tap(base_64_data):
    data = {
        "token": "2ika9NoqfOHBDPiYyFLISqQSi1HFrw49IBYYC5uWTm8",
        "type": "30009",
        "image": base_64_data,
    }
    url = "http://api.jfbym.com/api/YmServer/customApi"
    _headers = {
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=_headers, json=data).json()
    return response
