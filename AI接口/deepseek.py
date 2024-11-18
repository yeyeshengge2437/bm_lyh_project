# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="sk-9a76d51f714449d8b6ff81c74c02a5d0", base_url="https://api.deepseek.com/beta")


def deepseek_chat(chat_text):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "您是个乐于助人的助手"},
            {"role": "user", "content": f"{chat_text}"},
        ],
        max_tokens=8192,
        stream=False
    )

    input_token_num = response.usage.completion_tokens
    output_token_num = response.usage.prompt_tokens
    output_text = response.choices[0].message.content
    return input_token_num, output_token_num, output_text


# print(deepseek_chat("""你好，介绍一下你自己"""))

def deepseek_people(chat_text):
    system_prompt = """
    用户将提供一些文本。请解析并严格用以下形式的 JSON 格式输出并确保JSON格式严格正确。

    EXAMPLE INPUT: 
    潘静如

    角色：担保人
    
    关联公司：揭阳市榕城区合润化工经营部
    
    陈小卫
    
    角色：担保人
    
    关联公司：揭阳市榕城区合润化工经营部
    
    黄智景
    
    角色：担保人
    
    关联公司：广东大地创辉贸易有限公司

    EXAMPLE JSON OUTPUT:
    [{"姓名": "潘静如","曾用名": "潘静","性别": "女","身份证号": "440106197908020026","住址": "广州市天河区珠江新城华夏路","角色": "担保人","关联公司": "揭阳市榕城区合润化工经营部","职务": "法人","人物关系": "系潘婷之女","名下资产": "2000万","是否去世": "否","其他": "无"}, {"姓名": "陈小卫","曾用名": "陈肖卫","性别": "男","身份证号": "440106197908020026","住址": "广州市天河区珠江新城华夏路","角色": "担保人","关联公司": "揭阳市榕城区合润化工经营部","职务": "法人","人物关系": "系潘婷之子","名下资产": "2000万","是否去世": "否","其他": "无"}, ....]
    """

    user_prompt = chat_text + "请提取文中所有的人名，注意不包含文末联系人。识别个人信息包括：姓名（不要重复输出同一个人名），曾用名，性别，身份证号，住址，角色（该人此公告中的角色），关联公司（与该人有关联的公司，不得为空）， 职务，人物关系，名下资产，是否去世，其他（与该人有关的信息）。缺失值用''表示。注意：不要将多个人名放在同一个列表，不要将公司名称存为个人姓名，姓名字符串长度不得大于5。"

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        max_tokens=4096,
        response_format={
            'type': 'json_object'
        }
    )

    input_token_num = response.usage.completion_tokens
    output_token_num = response.usage.prompt_tokens
    output_text = response.choices[0].message.content
    return input_token_num, output_token_num, output_text

