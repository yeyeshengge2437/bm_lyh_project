import json
import re

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import os
from api_ai import img_url_to_file, ai_parse_next, ai_parse_success, ai_parse_fail
from KIMI import kimi_single_chat, kimi_file_chat
from 智谱 import zhipu_single_chat, zhipu_file_chat, zhipu_file_free_chat
from 跃问 import yuewen_chat, yuewen_file_chat, yuewen_freechat
from chatgpt_4mini import gpt_freechat
from deepseek import deepseek_chat
from quark_text import quark_text
from figure_shibie_formal import deepseek_identify_people, gpt_identify_company, save_database_people, \
    save_database_company
from kuake_table_url import quark
from character_classificatio_flask import identify_guarantee, identify_mortgagor, identify_collateral, deepseek_item_guarantee_2, deepseek_item_mortgagor_2


app = Flask(__name__)
@app.route("/test", methods=["GET"])
def test():
    value = {
        "success": 1,
        "remark": "测试成功"
    }
    return jsonify(value)


@app.route('/get_ai_response', methods=['POST'])
def get_ai_response():
    # 获取post请求的json数据
    data = request.get_data()
    data = data.decode('utf-8')
    data = json.loads(data)
    # 判断传入的工具列表
    id = data.get('id')
    name = data.get('name')
    paper_id = data.get('paper_id')
    tell_type = data.get('tell_type')
    tell_tool = data.get('tell_tool')
    files = data.get('files')
    if files:
        files = json.loads(files)
        files = files[0]
    input_text = data.get('input_text')
    input_key = data.get('input_key')
    if tell_tool == "kimi_8k":
        try:
            input_token_num, output_token_num, output_text = kimi_single_chat(input_text)
            value = {
                "id": id,
                "remark": "",
                "input_token_num": input_token_num,
                "output_token_num": output_token_num,
                "output_text": output_text,
                "success": 1
            }
            # 返回json数据
            return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    elif tell_tool == "kimi_32k":
        try:
            input_token_num, output_token_num, output_text = kimi_file_chat(files, input_text)
            value = {
                "id": id,
                "remark": "",
                "input_token_num": input_token_num,
                "output_token_num": output_token_num,
                "output_text": output_text,
                "success": 1
            }
            # 返回json数据
            return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    elif tell_tool == "glm_4_air":
        try:
            input_token_num, output_token_num, output_text = zhipu_single_chat(input_text)
            value = {
                "id": id,
                "remark": "",
                "input_token_num": input_token_num,
                "output_token_num": output_token_num,
                "output_text": output_text,
                "success": 1
            }
            # 返回json数据
            return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    elif tell_tool == "glm_4v_plus":
        try:
            input_token_num, output_token_num, output_text = zhipu_file_chat(files, input_text)
            value = {
                "id": id,
                "remark": "",
                "input_token_num": input_token_num,
                "output_token_num": output_token_num,
                "output_text": output_text,
                "success": 1
            }
            # 返回json数据
            return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    elif tell_tool == "step_1_8k":
        try:
            input_token_num, output_token_num, output_text = yuewen_chat(input_text)
            value = {
                "id": id,
                "remark": "",
                "input_token_num": input_token_num,
                "output_token_num": output_token_num,
                "output_text": output_text,
                "success": 1
            }
            # 返回json数据
            return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    elif tell_tool == "step_1v_8k":
        try:
            input_token_num, output_token_num, output_text = yuewen_file_chat(files, input_text)
            value = {
                "id": id,
                "remark": "",
                "input_token_num": input_token_num,
                "output_token_num": output_token_num,
                "output_text": output_text,
                "success": 1
            }
            # 返回json数据
            return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    elif tell_tool == "deepseek_chat":
        try:
            input_token_num, output_token_num, output_text = deepseek_chat(input_text)
            value = {
                "id": id,
                "remark": "",
                "input_token_num": input_token_num,
                "output_token_num": output_token_num,
                "output_text": output_text,
                "success": 1
            }
            # 返回json数据
            return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    elif tell_tool == "quark_text":
        # 夸克识别文字
        try:
            input_token_num, output_token_num, output_text = quark_text(files)
            value = {
                "id": id,
                "remark": "",
                "input_token_num": input_token_num,
                "output_token_num": output_token_num,
                "output_text": output_text,
                "success": 1
            }
            # 返回json数据
            return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    elif tell_tool == "gpt_freechat":
        # 免费gpt
        try:
            input_token_num, output_token_num, output_text = gpt_freechat(input_text)
            value = {
                "id": id,
                "remark": "",
                "input_token_num": input_token_num,
                "output_token_num": output_token_num,
                "output_text": output_text,
                "success": 1
            }
            # 返回json数据
            return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    # elif tell_tool == "pdf_content_except_table":
    #     # 识别pdf除表格以外的文章
    #     pass
    elif tell_tool == "paper_subject_tell":
        # 识别人物
        try:
            # 深度求索识别人的信息
            people_companies = deepseek_identify_people(input_text)
            # 深度求索识别公司的信息
            company_companies = gpt_identify_company(input_text)

            for company in people_companies:
                save_database_people(company, id, paper_id, input_key)
            for company in company_companies:
                save_database_company(company, id, paper_id, input_key)

            success_data = {
                'id': id,
                'remark': '成功',
                "success": 1
            }
            return jsonify(success_data)
        except Exception as e:
            fail_data = {
                'id': id,
                'remark': f'{e}',
                "success": 0
            }
            ai_parse_fail(data=fail_data)
    elif tell_tool == "quark_img_table_tell":
        # print(files)
        # 夸克识别表格
        try:
            output_text = quark(files)
            code = output_text.get("code")
            if code == "00000":
                value = {
                    "id": id,
                    "remark": "",
                    "output_text": output_text,
                    "success": 1
                }
                # 返回json数据
                return jsonify(value)
            else:
                value = {
                    "id": id,
                    "remark": output_text.get("message"),
                    "success": 0
                }
                return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    elif tell_tool == "identify_guarantee":
        try:
            input_token_num, output_token_num, guarantor, prompt = identify_guarantee(input_text)
            value = {
                'id': id,
                'remark': name,
                'input_token_num': input_token_num,
                'output_token_num': output_token_num,
                'output_text': guarantor,
                'prompt': prompt,
                'success': 1
            }
            return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    elif tell_tool == "deepseek_item_guarantee_2":
        try:
            input_token_num, output_token_num, guarantor, prompt = deepseek_item_guarantee_2(input_text)
            value = {
                'id': id,
                'remark': name,
                'input_token_num': input_token_num,
                'output_token_num': output_token_num,
                'output_text': guarantor,
                'prompt': prompt,
                'success': 1
            }
            return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    elif tell_tool == "identify_mortgagor":
        try:
            input_token_num, output_token_num, mortgagor, prompt = identify_mortgagor(input_text)
            value = {
                'id': id,
                'remark': name,
                'input_token_num': input_token_num,
                'output_token_num': output_token_num,
                'output_text': mortgagor,
                'prompt': prompt,
                'success': 1
            }
            return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    elif tell_tool == "identify_collateral":
        try:
            input_token_num, output_token_num, collateral, prompt = identify_collateral(input_text)
            value = {
                'id': id,
                'remark': name,
                'input_token_num': input_token_num,
                'output_token_num': output_token_num,
                'output_text': collateral,
                'prompt': prompt,
                'success': 1
            }
            return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    elif tell_tool == "deepseek_item_mortgagor_2":
        try:
            input_token_num, output_token_num, mortgagor, prompt = deepseek_item_mortgagor_2(input_text)
            value = {
                'id': id,
                'remark': name,
                'input_token_num': input_token_num,
                'output_token_num': output_token_num,
                'output_text': mortgagor,
                'prompt': prompt,
                'success': 1
            }
            return jsonify(value)
        except Exception as e:
            value = {
                "id": id,
                "remark": str(e),
                "success": 0
            }
            return jsonify(value)
    else:
        return jsonify({"success": 0, "id": id, "remark": "未知的工具名称"})


if __name__ == '__main__':
    # 开启调试调试模式（开发阶段）
    # app.run(debug=True)
    # 更改端口信息，让所有主机都可访问
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
