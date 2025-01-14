import re
from deepseek import deepseek_chat
from doubao import doubao_pro_32k

model_name = deepseek_chat


def identify_guarantee(content):
    content_prompt = f"""
你的任务是从给定的文本中提取保证人主体（担保人默认为保证人），单个主体以逗号分割，如果没有保证人则返回'空'。不要输出其他无关字段且保证主体去重。以下是文本详情：
<文本详情>
{{{content}}}
</文本详情>
操作步骤如下：
1. 仔细阅读文本详情的内容。
2. 识别其中提到的保证人主体（即承担担保责任的个人或组织）。
3. 去除重复的主体内容。
4. 将所有保证人主体以逗号分割的形式整理好。
5. 如果未发现保证人主体，则直接返回'空'。
"""
    prompt_ = """你的任务是从给定的文本中提取保证人主体（担保人默认为保证人），单个主体以逗号分割，如果没有保证人则返回'空'。不要输出其他无关字段且保证主体去重。以下是文本详情：
<文本详情>
{{content}}
</文本详情>
操作步骤如下：
1. 仔细阅读担保情况的内容。
2. 识别其中提到的保证人主体（即承担担保责任的个人或组织）。
3. 去除重复的主体内容。
4. 将所有保证人主体以逗号分割的形式整理好。
5. 如果未发现保证人主体，则直接返回'空'。"""
    a, b, guarantor = model_name(
        content_prompt)
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
    # guarantor = re.sub(r'\n', '', guarantor)
    print(guarantor)
    return a, b, guarantor, prompt_


def deepseek_item_guarantee_2(content):
    content_prompt = f"""你的任务是从给定的文本中提取保证人主体。保证人主体之间以逗号分割，如果没有保证人则返回'空'。请仔细阅读以下文本：
<text>
{content}
</text>
首先，明确债务加入主体和保证人主体的概念区别。债务加入主体是指主动加入债务关系承担债务的主体，而保证人主体是为债务提供保证担保的主体，我们这里仅需提取保证人主体，不要混淆二者。
接下来按照以下步骤提取保证人主体：
1. 仔细阅读文本内容。
2. 寻找与保证或担保相关的表述部分。
3. 在确定疑似保证人主体时，可以通过对文本中与担保相关的表述进行逐句分析，标记已确定的保证人主体，避免遗漏。
4. 在确定保证人主体时，必须以最简洁的形式呈现，不允许包含任何与主体本身无关的额外信息，例如括号内的更名、限定词（如“自然人”）、无关表述（如“已去世”等）。对于夫妇等可能存在组合主体的情况，需要单独列出个体作为保证人主体，例如“蔡福林夫妇”应拆分为“蔡福林”，而不能拆分为“蔡福林”和“蔡福林的夫人”这种包含多余表述的形式。
5. 确定其中涉及的保证人主体，将它们记录下来并去除重复项。
6. 如果没有发现任何保证人主体，则直接返回'空'。

请按照上述要求准确地提取保证人主体并输出结果。
"""
    prompt_ = """你的任务是从给定的文本中提取保证人主体。保证人主体之间以逗号分割，如果没有保证人则返回'空'。请仔细阅读以下文本：
<text>
{content}
</text>
首先，明确债务加入主体和保证人主体的概念区别。债务加入主体是指主动加入债务关系承担债务的主体，而保证人主体是为债务提供保证担保的主体，我们这里仅需提取保证人主体，不要混淆二者。
接下来按照以下步骤提取保证人主体：
1. 仔细阅读文本内容。
2. 寻找与保证或担保相关的表述部分。
3. 在确定疑似保证人主体时，可以通过对文本中与担保相关的表述进行逐句分析，标记已确定的保证人主体，避免遗漏。
4. 在确定保证人主体时，必须以最简洁的形式呈现，不允许包含任何与主体本身无关的额外信息，例如括号内的更名、限定词（如“自然人”）、无关表述（如“已去世”等）。对于夫妇等可能存在组合主体的情况，需要单独列出个体作为保证人主体，例如“蔡福林夫妇”应拆分为“蔡福林”，而不能拆分为“蔡福林”和“蔡福林的夫人”这种包含多余表述的形式。
5. 确定其中涉及的保证人主体，将它们记录下来并去除重复项。
6. 如果没有发现任何保证人主体，则直接返回'空'。

请按照上述要求准确地提取保证人主体并输出结果。"""
    a, b, guarantor = model_name(
        content_prompt)
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
    # guarantor = re.sub(r'\n', '', guarantor)
    print(guarantor)
    return a, b, guarantor, prompt_


def identify_mortgagor(content):
    content_prompt = f"""你的任务是从一段文字中提取抵押人/质押人的主体名称。如果有多个抵押人/质押人则以,分隔开。请注意，只要提供抵押/质押的主体都为抵押人/质押人，只有在明确说明为抵押人/质押人的时候才可以返回答案，如果没有明确说明文中含有抵押人/质押人但你觉得里面含有抵押人/质押人就返回'未明确'，没有抵押人/质押人就返回'无'。一般抵押物/质押物含有抵押人/质押人的主体信息。合同与主体无关。
以下是需要分析的文字：
<text>
{content}
</text>
你可以按照以下步骤进行操作：
1. 仔细阅读这段文字。
2. 寻找明确提及抵押人/质押人的部分。
3. 如果找到，提取出主体名称；如果没有找到但疑似存在，返回'未明确'；如果确定不存在，返回'无'。
4.只输出主体名称。
"""
    prompt_ = """你的任务是从一段文字中提取抵押人/质押人的主体名称。如果有多个抵押人/质押人则以,分隔开。请注意，只要提供抵押/质押的主体都为抵押人/质押人，只有在明确说明为抵押人/质押人的时候才可以返回答案，如果没有明确说明文中含有抵押人/质押人但你觉得里面含有抵押人/质押人就返回'未明确'，没有抵押人/质押人就返回'无'。一般抵押物/质押物含有抵押人/质押人的主体信息。合同与主体无关。
以下是需要分析的文字：
<text>
{content}
</text>
你可以按照以下步骤进行操作：
1. 仔细阅读这段文字。
2. 寻找明确提及抵押人/质押人的部分。
3. 如果找到，提取出主体名称；如果没有找到但疑似存在，返回'未明确'；如果确定不存在，返回'无'。
4.只输出主体名称。"""
    a, b, mortgagor = model_name(
        content_prompt)
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
    # mortgagor = re.sub(r'\n', '', mortgagor)
    print(mortgagor)
    return a, b, mortgagor, prompt_


def deepseek_item_mortgagor_2(content):
    content_prompt = f"""你的任务是从给定的关于债权相关的文字中提取抵质押人的主体名称。
以下是关于债权的文字内容：
<debt_related_text>
{{{content}}}
</debt_related_text>
你需要仔细阅读这段文字，从中找出抵质押人的主体名称，将所有主体名称用逗号隔开后直接输出。不需要进行额外的解释或者添加其他内容，只输出主体名称即可。现在开始提取。"""
    prompt_ = """你的任务是从给定的关于债权相关的文字中提取抵质押人的主体名称。
以下是关于债权的文字内容：
<debt_related_text>
{{content}}
</debt_related_text>
你需要仔细阅读这段文字，从中找出抵质押人的主体名称，将所有主体名称用逗号隔开后直接输出。不需要进行额外的解释或者添加其他内容，只输出主体名称即可。现在开始提取。
"""
    a, b, mortgagor = model_name(
        content_prompt)
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
    print(mortgagor)
    # mortgagor = re.sub(r'\n', '', mortgagor)
    return a, b, mortgagor, prompt_


def identify_collateral(content):
    content_prompt = f"""你的任务是从给定的文本中提取抵押物/质押物信息。当担保物没有特殊说明时默认为抵押物/质押物，如果没有抵押物/质押物则返回'空'。请仔细阅读以下文本：
<text>
{{{content}}}
</text>
按照以下步骤进行操作：
1. 仔细浏览整个文本内容。
2. 查找与抵押物/质押物相关的表述。
3. 只提取抵押物/质押物相关的信息，不要输出其他无关字段。
请直接给出提取的抵押物/质押物信息或者'空'。"""
    prompt_ = """你的任务是从给定的文本中提取抵押物/质押物信息。当担保物没有特殊说明时默认为抵押物/质押物，如果没有抵押物/质押物则返回'空'。请仔细阅读以下文本：
<text>
{{content}}
</text>
按照以下步骤进行操作：
1. 仔细浏览整个文本内容。
2. 查找与抵押物/质押物相关的表述。
3. 只提取抵押物/质押物相关的信息，不要输出其他无关字段。
请直接给出提取的抵押物/质押物信息或者'空'。"""
    a, b, collateral = model_name(
        content_prompt)
    collateral = re.sub(r'抵押物/质押物：', '', collateral)
    collateral = re.sub(r'抵押物/质押物:', '', collateral)
    collateral = re.sub(r'抵押物：|质押物：', '', collateral)
    collateral = re.sub(r'抵押物:|质押物:', '', collateral)
    collateral = re.sub(r';', ',', collateral)
    collateral = re.sub(r'；', ',', collateral)
    collateral = re.sub(r'，', ',', collateral)
    if not collateral:
        collateral = "空"
    if collateral == "位于某处房产,某工厂":
        collateral = "空"
    if collateral == "空":
        collateral = ''
    # collateral = re.sub(r'\n', '', collateral)
    print(collateral)
    return a, b, collateral, prompt_
