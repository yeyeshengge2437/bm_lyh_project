# -*- coding: utf-8 -*-
import time

import requests

refresh_token1 = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTczOTM0NTcyOSwiaWF0IjoxNzMxNTY5NzI5LCJqdGkiOiJjc3FxZ2dibXZxOGtnYW5yN285ZyIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiY3NxcWdnYm12cThrZ2FucjdvOGciLCJzcGFjZV9pZCI6ImNzcXFnZ2JtdnE4a2dhbnI3bzgwIiwiYWJzdHJhY3RfdXNlcl9pZCI6ImNzcXFnZ2JtdnE4a2dhbnI3bzdnIiwic3NpZCI6IjE3MzEwOTMwOTcwNTAwNTU0MzMiLCJkZXZpY2VfaWQiOiI3Mzk0MzMxNjA1MDc2NDIxMTIxIn0.UBO4s9gGZ1yKsBNtzoTFDtOvHvxzpE2Mvg-PWrCwK8NopsowHn2yp-spv8PDmcCBiP3lxpRbYqOuOPDroVuJgQ'
refresh_token2 = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTczOTM0NjI5OCwiaWF0IjoxNzMxNTcwMjk4LCJqdGkiOiJjc3Fxa3VoMWpmZGVyb3BlaDgyMCIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiY3NxcWt1aDFqZmRlcm9wZWg4MTAiLCJzcGFjZV9pZCI6ImNzcXFrdWgxamZkZXJvcGVoODAwIiwiYWJzdHJhY3RfdXNlcl9pZCI6ImNzcXFrdWgxamZkZXJvcGVoN3ZnIiwic3NpZCI6IjE3MzEwNzMzMDU4MzYwMjE0NDYiLCJkZXZpY2VfaWQiOiI3Mzk0MzMxNjA1MDc2NDIxMTIxIn0.yXa_3aS8h7CsSkARL-MWw6KbqId9nwTUs9Fq5Lc35cRcBdm9o6jmFMzKH74vOz4S44ms0lEJWB3RtXry45kLrQ'
refresh_token3 = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTczOTM0NzA2OSwiaWF0IjoxNzMxNTcxMDY5LCJqdGkiOiJjc3FxcXY5MWpmZGVyb3BxZ3NmMCIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiY3NxcXF2OTFqZmRlcm9wcWdzZDAiLCJzcGFjZV9pZCI6ImNzcXFxdjkxamZkZXJvcHFnc2MwIiwiYWJzdHJhY3RfdXNlcl9pZCI6ImNzcXFxdjkxamZkZXJvcHFnc2JnIiwic3NpZCI6IjE3MzEwOTA4OTgwMjAyNzk1MjIiLCJkZXZpY2VfaWQiOiI3Mzk0MzMxNjA1MDc2NDIxMTIxIn0.qKp0ODeJmly-UvcC1_7nOqKl7AcUHvggH9Ge6EQQ2Ca9kjeiRmg9z-WJINiRGaW7uUtMouW3oV9ueomQ-2IrRA'
refresh_token4 = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTczOTM1MTA3NywiaWF0IjoxNzMxNTc1MDc3LCJqdGkiOiJjc3FycTlmZDBwODBpaG5tYWNsZyIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiY3NxcnE5ZmQwcDgwaWhubWFja2ciLCJzcGFjZV9pZCI6ImNzcXJxOWZkMHA4MGlobm1hY2swIiwiYWJzdHJhY3RfdXNlcl9pZCI6ImNzcXJxOWZkMHA4MGlobm1hY2pnIiwic3NpZCI6IjE3MzEwNzMzMDU4MzYxMzMyMTAiLCJkZXZpY2VfaWQiOiI3NDM3MDU3NjAwNDM0MzE1NTI2In0.9u10fiKGbJHL_YtIsMXcstBK8luuO0mpWOePsDjA4i9OodJ0drpY-EolqjcoNFy34G3_IwAH1-s7oITtUBC3-Q'
refresh_token5 = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTczOTM1MTk4NCwiaWF0IjoxNzMxNTc1OTg0LCJqdGkiOiJjc3FzMWM3ZDBwODBpaGc0b3ZjMCIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiY3NuaWh2dWdpM3B0bTZwOWZmZjAiLCJzcGFjZV9pZCI6ImNzbmlodnVnaTNwdG02cDlmZmVnIiwiYWJzdHJhY3RfdXNlcl9pZCI6ImNzbmlodnVnaTNwdG02cDlmZmUwIiwic3NpZCI6IjE3MzEwNzMzMDU4MzYxMzMyMTAiLCJkZXZpY2VfaWQiOiI3NDM3MDU3NjAwNDM0MzE1NTI2In0.1DEOFtot8gfbiKhMUR5VlU7pou_22JTQnCIzAsNYsHE3jdT_Z30dgJpB0k9M8-vDwqqoeO0VPxb3Ijx10nYlbA'

api_url = 'https://kimi-free-api-vy08.onrender.com/v1/chat/completions'

headers = {
    'Authorization': f'Bearer {refresh_token1}, {refresh_token2}, {refresh_token3}, {refresh_token4}, {refresh_token5}',
    'Content-Type': 'application/json'
}


def get_response_from_api(user_input):
    data = {

        "model": "kimi",
        # "conversation_id": "cnndivilnl96vah411dg",
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ],
        "use_search": False,
        "stream": False
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()


def get_response_from_api_free(img_file_url, user_input):
    data = {
        "model": "kimi",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "file",
                        "file_url": {
                            "url": img_file_url
                        }
                    },
                    {
                        "type": "text",
                        "text": user_input
                    }
                ]
            }
        ],
        "use_search": False
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()


def kimitext_free(chat_text):
    response = get_response_from_api(chat_text)
    input_token_num = response['usage']['completion_tokens']
    output_token_num = response['usage']['prompt_tokens']
    output_text = response['choices'][0]['message']['content']
    time.sleep(10)
    return input_token_num, output_token_num, output_text


def kimifile_free(img_file_url, chat_text):
    response = get_response_from_api_free(img_file_url, chat_text)
    input_token_num = response['usage']['completion_tokens']
    output_token_num = response['usage']['prompt_tokens']
    output_text = response['choices'][0]['message']['content']
    time.sleep(10)
    return input_token_num, output_token_num, output_text


def api_alive():
    url = 'https://kimi-free-api-vy08.onrender.com/ping'
    response = requests.get(url)
    return response.status_code


