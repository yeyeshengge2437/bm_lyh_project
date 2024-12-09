import re
from deepseek import deepseek_chat

model_name = deepseek_chat


def identify_guarantee(content):
    prompt = "\n\n从文中提取保证人(担保人默认为保证人)主体，单个主体以,分割，不要输出其他无关字段（去重）,没有保证人返回'空'。"
    a, b, guarantor = model_name(
        content + prompt)
    guarantor = re.sub(r'保证人：', '', guarantor)
    guarantor = re.sub(r'保证人:', '', guarantor)
    guarantor = re.sub(r';', ',', guarantor)
    guarantor = re.sub(r'；', ',', guarantor)
    guarantor = re.sub(r'，', ',', guarantor)
    guarantor = re.sub(r"、", ',', guarantor)

    if guarantor[-1] == ',':
        guarantor = guarantor[:-1]
    if not guarantor:
        guarantor = "空"
    if guarantor == "某某有限公司,李某某,王某某":
        guarantor = "空"
    if guarantor == "空":
        guarantor = ''
    guarantor = re.sub(r'\n', '', guarantor)
    # print(guarantor)
    return a, b, guarantor, prompt


def deepseek_item_guarantee_2(content):
    prompt = "\n\n从文中提取保证人(担保人默认为保证人)主体，单个主体以,分割，不要输出其他无关字段（去重）,没有保证人返回'空'。"
    a, b, guarantor = model_name(
        content + prompt)
    guarantor = re.sub(r'保证人：', '', guarantor)
    guarantor = re.sub(r'保证人:', '', guarantor)
    guarantor = re.sub(r';', ',', guarantor)
    guarantor = re.sub(r'；', ',', guarantor)
    guarantor = re.sub(r'，', ',', guarantor)
    guarantor = re.sub(r"、", ',', guarantor)

    if guarantor[-1] == ',':
        guarantor = guarantor[:-1]
    if not guarantor:
        guarantor = "空"
    if guarantor == "某某有限公司,李某某,王某某":
        guarantor = "空"
    if guarantor == "空":
        guarantor = ''
    guarantor = re.sub(r'\n', '', guarantor)
    # print(guarantor)
    return a, b, guarantor, prompt


def identify_mortgagor(content):
    prompt = "\n\n从中提取抵押人/质押人主体名称（担保人在未说明为抵押人/质押人时不可视为抵押人/质押人，保证人在未说明为抵押人/质押人时不可视为抵押人/质押人。），主体之间以,分割。未明确为抵押人/质押人不做推理，不要输出其他无关字段,没有抵押人/质押人返回'空'，严格按照执行。案例：抵押人/质押人:某某有限公司,李某某,王某某;(每项用';'结束)注意：此案例为借鉴数据，请不要引用里面的数据。"
    a, b, mortgagor = model_name(
        content + prompt)
    mortgagor = re.sub(r'抵押人/质押人：', '', mortgagor)
    mortgagor = re.sub(r'抵押人/质押人:', '', mortgagor)
    mortgagor = re.sub(r'抵押人：|质押人：', '', mortgagor)
    mortgagor = re.sub(r'抵押人:|质押人:', '', mortgagor)
    mortgagor = re.sub(r';', ',', mortgagor)
    mortgagor = re.sub(r'；', ',', mortgagor)
    mortgagor = re.sub(r'，', ',', mortgagor)
    mortgagor = re.sub(r'、', ',', mortgagor)
    mortgagor = re.sub(r"'", '', mortgagor)
    mortgagor = re.sub(r"’", '', mortgagor)
    if mortgagor[-1] == ',':
        mortgagor = mortgagor[:-1]
    if not mortgagor:
        mortgagor = "空"
    if mortgagor == "某某有限公司,李某某,王某某":
        mortgagor = "空"
    if mortgagor == "空":
        mortgagor = ''
    mortgagor = re.sub(r'\n', '', mortgagor)
    # print(mortgagor)
    return a, b, mortgagor, prompt


def deepseek_item_mortgagor_2(content):
    prompt = "\n\n提取所有抵质押人的名称，输出结果：XX有限公司,张三,李四（去重，单个主体以“,”分割，没有返回‘空’，不要输出其他无关字段）。"
    a, b, mortgagor = model_name(
        content + prompt)
    mortgagor = re.sub(r'抵押人/质押人：', '', mortgagor)
    mortgagor = re.sub(r'抵押人/质押人:', '', mortgagor)
    mortgagor = re.sub(r'抵押人：|质押人：', '', mortgagor)
    mortgagor = re.sub(r'抵押人:|质押人:', '', mortgagor)
    mortgagor = re.sub(r';', ',', mortgagor)
    mortgagor = re.sub(r'；', ',', mortgagor)
    mortgagor = re.sub(r'，', ',', mortgagor)
    mortgagor = re.sub(r'、', ',', mortgagor)
    mortgagor = re.sub(r"'", '', mortgagor)
    mortgagor = re.sub(r"’", '', mortgagor)
    if mortgagor[-1] == ',':
        mortgagor = mortgagor[:-1]
    if not mortgagor:
        mortgagor = "空"
    if mortgagor == "XX有限公司,张三,李四":
        mortgagor = "空"
    if mortgagor == "空":
        mortgagor = ''
    # print(mortgagor)
    mortgagor = re.sub(r'\n', '', mortgagor)
    return a, b, mortgagor, prompt


def identify_collateral(content):
    prompt = "\n\n从中提取抵押物/质押物(当担保物没有特殊说明时默认为抵押物/质押物)信息，不要输出其他无关字段,没有抵押物/质押物返回'空'，严格按照执行。案例：抵押物/质押物:位于某处房产,某工厂;注意：此案例为借鉴数据，请不要引用里面的数据。"
    a, b, collateral = model_name(
        content + prompt)
    collateral = re.sub(r'抵押物/质押物：', '', collateral)
    collateral = re.sub(r'抵押物/质押物:', '', collateral)
    collateral = re.sub(r'抵押物：|质押物：', '', collateral)
    collateral = re.sub(r'抵押物:|质押物:', '', collateral)
    collateral = re.sub(r';', '', collateral)
    collateral = re.sub(r'；', ',', collateral)
    collateral = re.sub(r'，', ',', collateral)
    if not collateral:
        collateral = "空"
    if collateral == "位于某处房产,某工厂":
        collateral = "空"
    if collateral == "空":
        collateral = ''
    collateral = re.sub(r'\n', '', collateral)
    # print(collateral)
    return a, b, collateral, prompt
