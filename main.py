# -*- coding: utf-8 -*-
# @Time    : 2022/5/8 12:36
# @Author  : huni
# @Email   : zcshiyonghao@163.com
# @File    : main.py
# @Software: PyCharm
import re
import json
import requests
import os
import redis
import asyncio
import threading
from httpx import AsyncClient
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
import uvicorn
import urllib.parse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
from dotenv import load_dotenv
import ujson

# 加载 .env 文件
load_dotenv(".env")
# 连接Redis数据库
redis_pool = redis.Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=int(os.getenv('REDIS_DB')), password=os.getenv('REDIS_PASS'))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.json_loads = ujson.loads
app.json_dumps = ujson.dumps

# 创建线程锁
lock = threading.Lock()

app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory = "templates")
# 设置 logging
logging.basicConfig(filename = 'app.log', level = logging.INFO)


# 添加 middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    if 'static' not in request.url.path:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 设置时区为北京时间
        # 记录请求信息，包括请求方法、URL 和 IP 地址、请求时间
        logging.info(f"{now} | 请求 {request.method} | {request.url} | 请求IP {request.client.host}")
    response = await call_next(request)
    if 'static' not in request.url.path:
        # 记录响应信息，包括响应状态码
        logging.info(f"响应 | {response.status_code}")
    return response


@app.get("/")
def getdate(request: Request):
    return templates.TemplateResponse('main.html', context = {'request': request})


@app.get("/d/{taskid}")
def turn(taskid: str):
    try:
        old_region_list = ['shanxi', 'shenzhen', "henan", 'guangdong', 'anhui', 'jiangsu']
        accname = ['test转苍穹']
        taskid = taskid.strip()
        rule_json = 'static/rule.json'
        with open(rule_json, mode = 'rb') as f:
            rule_json_list = f.read()
            rule_json_list = json.loads(rule_json_list)

        proxies = {
            "http": None,
            "https": None,
        }
        param = {
            'taskId': taskid
        }
        resp = {}
        if taskid.startswith('1'):

            resp = requests.get(os.getenv('ZWYMOCK'), params = param,
                                proxies = proxies).json()
            if ((not resp['data'].get('defaultRule')) and (resp['data']['region'] not in old_region_list)) or resp[
                'data'].get('accName') in accname:
                resp['data']['defaultRule'] = rule_json_list

        elif taskid.startswith('3'):
            resp = requests.get(os.getenv('ZWYPROD'), params = param,
                                proxies = proxies).json()
            if (not resp['data'].get('defaultRule')) and (resp['data']['region'] not in old_region_list):
                resp['data']['defaultRule'] = rule_json_list

        else:
            pass
    except Exception as e:
        output = str(e)
    else:
        output = json.dumps(resp.get('data'), ensure_ascii = False) if (
                    resp.get('code') == 200 and resp.get('msg') == 'success') else {}
    return {'output': output}


@app.post("/t")
async def translate(request: Request):
    try:
        proxies = {
            "http": None,
            "https": None,
        }
        data = await request.json()
        tstr = data.get("input_str", "")
        if not tstr:
            output = {}
        else:
            trans_type = 'auto2zh'
            zh = re.findall('[\u4e00-\u9fa5]', tstr)
            if zh:
                trans_type = 'auto2en'
            url = os.getenv('CAIYUNURL')
            token = os.getenv('CAIYUNTOKEN')
            payload = {
                "source": tstr,
                "trans_type": trans_type,
                "request_id": "demo",
                "detect": True,
            }
            headers = {
                "content-type": "application/json",
                "x-authorization": "token " + token,
            }
            response = requests.request("POST", url, data = json.dumps(payload), headers = headers, proxies = proxies)
            output = json.loads(response.text)["target"]
    except:
        output = {}

    return {'output': output}


@app.post("/o")
async def ocr(request: Request):
    output = {}
    try:
        proxies = {
            "http": None,
            "https": None,
        }
        data = await request.json()
        image = data.get("image", "")
        if not image:
            output = {}
        else:
            url = "https://aip.baidubce.com/oauth/2.0/token"
            params = {"grant_type": "client_credentials", "client_id": os.getenv('OCRAPIKEY'), "client_secret": os.getenv('OCRSECRETKEY')}
            access_token = str(requests.post(url, params = params, proxies = proxies).json().get("access_token"))
            url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token={access_token}"

            # 对二进制数据进行URL编码
            url_encoded_data = urllib.parse.quote(image.split(",")[1])
            payload = 'image=' + url_encoded_data
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }

            response = requests.request("POST", url, headers = headers, data = payload, proxies = proxies)
            if 'error' in str(response.text):
                output = {}
            if 'words_result' in str(response.text):
                output = ''
                res = response.json()
                for line in res['words_result']:
                    output += line['words'] + '\n'

    except Exception as e:
        logging.error(e)

    return {'output': output}


@app.post("/c")
async def curl2requests(request: Request):
    output = {}
    try:
        proxies = {
            "http": None,
            "https": None,
        }
        data = await request.json()
        input_str = data.get("input_str", "")
        if not input_str:
            output = {}
        else:
            url = 'https://spidertools.cn/spidertools/tools/format'

            post_data = {
                "format_type": "curl_to_request",
                "input_str": str(input_str)
            }
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"}

            response = requests.post(url, data = json.dumps(post_data), headers = headers, proxies = proxies)
            if 'import requests' in str(response.text):
                output = response.text.replace('\\nprint(response)"', '')
                output = output.replace('"import', 'import')
                output = re.sub(r'(?<!\\)\\(?=")', '', output)
                output = output.replace('\\\\\\', '\\')

            else:
                output = "转换失败"

    except Exception as e:
        logging.error(e)

    return {'output': output}


async def get_chat(msgdict,token=None):
    web = os.getenv('AISET')
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/json",
        "origin": f"https://{web}",
        "referer": f"https://{web}/chat/1681217446562",
        'cookie': f'connect.sid={token}',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"
    }
    url = f"https://{web}/api/chat-process"
    msg = msgdict.get('text')
    lastid = msgdict.get('id')

    data = {
        "openaiKey": "",
        "prompt": msg,
        "options": {
            "systemMessage": f"You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.\
    Knowledge cutoff: 2021-09-01\
    Current date: {datetime.today().strftime('%Y-%m-%d')}",
            "completionParams": {
                "presence_penalty": 0.8,
                "temperature": 1,
                "model": "gpt-3.5-turbo"
            }
        }
    }
    if lastid:
        data = {"openaiKey": "", "prompt": msg,
                "options": {"parentMessageId": lastid,
                            "systemMessage": f"You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: {datetime.today().strftime('%Y-%m-%d')}",
                            "completionParams": {"presence_penalty": 0.8, "temperature": 1, "model": "gpt-3.5-turbo"}}}

    async with AsyncClient() as client:
        async with client.stream('POST', url, headers = headers, json = data, timeout =30) as response:
            async for line in response.aiter_lines():
                if line.strip() == "":
                    continue
                try:
                    data = json.loads(line)
                except Exception as e:
                    logging.error(e)
                    yield {"choices": [{"delta": {"content": "OpenAI服务器连接失败,请联系管理员"}}]}
                    return
                if '刷新试试~' in str(data):
                    yield {"choices": [{"delta": {"content": "连接失败,重新键入试试~"}}]}
                    return
                if 'ChatGPT error' in str(data):
                    yield {"choices": [{"delta": {"content": "OpenAI错误,请联系管理员"}}]}
                    return
                if '今日剩余回答次数为0' in str(data):
                    yield {"choices": [{"delta": {"content": "今日回答次数已达上限"}}]}
                    return
                if '网站今日总共的免费额度已经用完' in str(data):
                    yield {"choices": [{"delta": {"content": "网站今日回答次数已达上限"}}]}
                    return
                if '今日免费额度10000已经用完啦' in str(data):
                    yield {"choices": [{"delta": {"content": "今日回答次数已达上限"}}]}
                    return
                if data['detail'].get('choices') is None or data['detail'].get('choices')[0].get(
                        'finish_reason') is not None:
                    return
                try:
                    yield data['detail']
                except Exception as e:
                    logging.error(e)
                    yield {"choices": [{"delta": {"content": "非预期错误,请联系管理员"}}]}
                    return


@app.websocket("/chat")
async def chat(websocket: WebSocket):
    client_ip = websocket.scope["client"][0]
    await websocket.accept()
    last_text = ''
    language = ["python", "java", "c", "cpp", "c#", "javascript", "html", "css", "go", "ruby", "swift", "kotlin"]
    # asyncio.create_task(send_ping(websocket))  # 创建一个发送心跳包的任务
    while True:
        try:
            data = await websocket.receive_json()
            #测试代码
            # await websocket.send_json({"text": '你好，有什么可以帮助您的吗?', "id": ''})
            token = await get_token_by_redis()
            logging.info(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {client_ip} | {str(data)}')
            async for i in get_chat(data, token=token):
                if i['choices'][0].get('delta').get('content'):
                    # logging.info(i['choices'][0])
                    response_text = i['choices'][0].get('delta').get('content')
                    if response_text.strip() == '``':
                        last_text = '``'
                        response_text = ''
                    if '`' in response_text and last_text == '``':
                        response_text = response_text.strip().replace('`', '```')
                        last_text = '```'
                    if response_text.strip() == '```':
                        last_text = '```'
                    if last_text == '```' and any([i in response_text for i in language]):
                        for j in language:
                            if j == response_text:
                                response_text = response_text.replace(j, '')
                                if j == 'c':
                                    last_text = 'c'
                                else:
                                    last_text = ''
                                break
                    if last_text == 'c' and '++' in response_text:
                        response_text = response_text.replace('++', '')
                        last_text = ''
                    response_data = {"text": response_text, "id": i.get('id')}
                    await websocket.send_json(response_data)
        except WebSocketDisconnect as e:
            # 处理断开连接的情况
            break
        except Exception as e:
            # 记录其他异常
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logging.error(f"{now} | WebSocket 异常: {repr(e)}")
            break

async def send_ping(websocket: WebSocket, interval: int = 60):
    while True:
        await asyncio.sleep(interval)
        try:
            await websocket.send_text("ping")
        except WebSocketDisconnect:
            break

async def get_token_by_redis():
    reset = False
    list_length = redis_pool.llen('cookieList')
    tokenindex = int(redis_pool.get('tokenindex'))
    if tokenindex == list_length:
        tokenindex = 0
        reset = True
    token = redis_pool.lindex('cookieList', tokenindex)
    token = token.decode('utf-8')
    if tokenindex == 0 and reset:
        tokenindex_reset = tokenindex
    else:
        tokenindex_reset = tokenindex + 1

    redis_pool.set('tokenindex', str(tokenindex_reset))
    return token


if __name__ == '__main__':
    uvicorn.run('main:app', host = "0.0.0.0", port = 20235, reload = True)
