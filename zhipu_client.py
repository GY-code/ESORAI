import json
import re

import bs4
import requests
from zhipuai import ZhipuAI

from constant import ASSISTANT_TYPE
from prompt import PromptFactory

zhipu_api_key = "06e1352c3ae3a9c41968f518c96b4cc0.9VzNz0sfBdiSgij9"
client = ZhipuAI(api_key=zhipu_api_key)  # 请填写您自己的APIKey
prompt_factory = PromptFactory()


def single_msg_call(model="glm-4", msg=""):
    response = client.chat.completions.create(
        model=model,  # 请填写您要调用的模型名称
        messages=[
            {"role": "user", "content": msg}
        ],
    )
    print(model + '有以下回复：\n', response)
    return response.choices[0].message


def single_msg_call_with_web(model="glm-4", msg=""):
    tools = [{
        "type": "web_search",
        "web_search": {
            "enable": True,  # 默认为关闭状态（False） 禁用：False，启用：True。
            "search_result": True
        }
    }]
    response = client.chat.completions.create(
        model=model,  # 请填写您要调用的模型名称
        messages=[
            {"role": "user", "content": msg}
        ],
        tools=tools
    )
    print(model + '有以下回复：\n', response)
    return response.choices[0].message


def single_long_msg_call(msg):
    model = "glm-4-long"
    return single_msg_call(model, msg)


def web_search_call(msg):
    msg = [
        {
            "role": "user",
            "content": msg
        }
    ]
    tool = "web-search-pro"
    url = "https://open.bigmodel.cn/api/paas/v4/tools"
    data = {
        "tool": tool,
        "stream": False,
        "messages": msg
    }
    resp = requests.post(
        url,
        json=data,
        headers={'Authorization': zhipu_api_key},
        timeout=300
    )
    print(resp.content.decode())
    search_result_data = json.loads(resp.content.decode())["choices"][0]["message"]["tool_calls"][1]["search_result"]
    # 对列表中的每一项新加一个内容字段，用于存放网页内容
    for item in search_result_data:
        item["content_detail"] = parse_url_content_to_text(item["link"])
    return search_result_data

def assistant_call(id=ASSISTANT_TYPE.AI_SEARCH, msg=""):
    generate = client.assistant.conversation(
        assistant_id=id,
        conversation_id=None,
        model="glm-4-assistant",
        messages=[
            {
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": msg
                }]
            }
        ],
        stream=True,
        attachments=None,
        metadata=None
    )
    for resp in generate:
        print(resp)
    return generate


def propose_idea_startup_generate(msg):
    return single_msg_call_with_web(msg=prompt_factory.ProposeIdeaStartupPrompt(msg))

def propose_idea_based_on_before_generate(msg):
    return single_msg_call_with_web(msg=prompt_factory.ProposeIdeaBasedOnBeforePrompt(msg))

def warning_before_experiment_generate(msg):
    return single_msg_call_with_web(msg=prompt_factory.WarningBeforeExperiment(msg))


def parse_url_content_to_text(url):
    #  get html content using bs4
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers).content
    response = bs4.BeautifulSoup(response, 'html.parser')
    text = response.text
    # remove spaces and newlines
    text = re.sub(r'\s+', '', text)
    return text
