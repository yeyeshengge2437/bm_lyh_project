from a_mysql_connection_pool import get_ban_data, del_ban_data
from qcc_api_res import get_response, post_response
webpage = 1234
sql_data = get_ban_data(webpage)
for ban_id, url, data_key, res_type, json_data, key_no, webpage_id in sql_data:
    print(ban_id, url, data_key, res_type, json_data, key_no, webpage_id)
    if res_type == 'post':
        value_ban = post_response(url, key_no, pid, tid, cookies, json_data=json_data)
        if value_ban:
            for data_value in value_ban['data']:
                if data_key in ['business_info', 'credit_eval', 'trade_credit']:
                    data_md5 = generate_md5(str(data_value))
                    data_status = "current"
                    data_json = json.dumps(data_value, ensure_ascii=False)
                    up_qcc_data(key_no, data_key, data_status, data_md5, data_json, from_queue, webpage_id)

                else:
                    if 'his_' in data_key:
                        # 历史信息，增加标识
                        data_status = 'history'
                        for up_data in data_value:
                            if up_data:
                                data_key = data_key.replace('his_', '')
                                data_json = json.dumps(up_data, ensure_ascii=False)
                                data_md5 = generate_md5(str(up_data))
                                up_qcc_data(key_no, data_key, data_status, data_md5, data_json, from_queue,
                                            webpage_id)
                    else:
                        for up_data in data_value:
                            if up_data:
                                data_status = "current"
                                data_json = json.dumps(up_data, ensure_ascii=False)
                                data_md5 = generate_md5(str(up_data))
                                up_qcc_data(key_no, data_key, data_status, data_md5, data_json, from_queue,
                                            webpage_id)

