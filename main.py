from fastapi import FastAPI

from zhipu_client import single_msg_call, web_search_call, assistant_call, \
    propose_idea_startup_generate, propose_idea_based_on_before_generate, warning_before_experiment_generate

app = FastAPI()


@app.get("/hello/{name}")
async def say_hello(name: str):
    msg = "你好，我叫{}，请和我打招呼".format(name)
    return single_msg_call(msg)


@app.post("/web_search")
async def web_search():
    experiment_topic = "海洋Anammox主导脱氮过程"
    return web_search_call(experiment_topic)


@app.get("/test_case")
async def test():
    return assistant_call()


@app.post("/propose_idea_startup")
async def propose_idea_startup():
    msg = "影响海洋Anammox主导脱氮过程的因素分析与效率优化"
    return propose_idea_startup_generate(msg)


@app.post("/propose_idea_based_on_before")
async def propose_idea_based_on_before():
    msg = "氨氮难以与亚硝氮同步去除、无法实现Anammox过程"
    return propose_idea_based_on_before_generate(msg)


@app.post("/warning_before_experiment")
async def warning_before_experiment():
    msg = "海洋Anammox主导脱氮过程优化"
    return warning_before_experiment_generate(msg)
