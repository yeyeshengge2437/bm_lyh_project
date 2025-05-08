import requests
from ai_api_mid import ai_parse_next, ai_parse_success, ai_parse_fail
# Authorization: Bearer M3JPM98-JMP46MY-HEF0H3P-CAQED8E


def res_ai():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer M3JPM98-JMP46MY-HEF0H3P-CAQED8E',
    }

    json_data = {
      "message": "介绍一下你自己",
      "mode": "chat"
    }

    response = requests.post('http://10.20.151.182:3001/api/v1/workspace/ds-32b/chat', headers=headers, json=json_data, timeout=(10, 600))
    res_value = response.json()
    tokens_num = res_value["metrics"]["total_tokens"]
    answer_str = res_value["textResponse"]
    return answer_str, tokens_num

while True:
    res_value = ai_parse_next()


