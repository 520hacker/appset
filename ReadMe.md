# 讯飞星火Demo

![img](https://memosfile.qiangtu.com/picgo/assets/2023/06/28202306_28235526.png)

本工程clone自 https://github.com/qnmlgbd250/appset

因为需要测试一下讯飞星火的api,所以找了一个易于调用的方案。

实现页面 http://xunfei.qiangtu.com

### 请略微注意

- 本项目依然是以支持OPENAI为目标实现的，我只是改了一下部分连接信息，修改了某个小bug，然后添加了一下Docker发布。
- 连接讯飞API依赖于我的另一个半成品项目 [xunfei2gpt](https://github.com/520hacker/xunfei2gpt) ，稍后开源, 其原理就是把讯飞的原本的websocket 的支持给转成OPENAI 的API 支持，没有办法现在兼容OPENAI的客户端更多一点。
- 这个项目是一个半成品，如果需要深度GPT开发可以联系原创作者。
- 欢迎交流讯飞API开发。

### 下一步计划

- 本项目暂无下一步计划，因为可以遇见讯飞的测试KEY的token会很快耗完，在没有测试需求的情况下，本项目会处于暂停状态。
- 有兴趣即申请讯飞相关key并共享给我的可以联系我 https://t.me/Odinluo

### 怎么申请讯飞的KEY

​			这个貌似是要靠工单手动支持你接入的

-  https://console.xfyun.cn/app/create?redirect=%2Fapp%2Fmyapp 创建应用
-  https://console.xfyun.cn/services/cbm 获得APPID
-  https://xinghuo.xfyun.cn/ 页面底部点 合作咨询
-  填写表单 申请接入能力。

### 部署说明

- 已经实现好的docker image地址 odinluo/xunfei2ui 
- 直接pull它， 然后注意在环境变量中更新 xunfei2gpt  的ip和端口，替换原 192.168.2.101:xxx 的内容为你的内容
- 指定一个映射端口，原web服务端口为 20235 , 你可以指定你自己的对外端口，比如 8080:20235 。
- 建议映射目录 /app/static  ， 比如参考我 /docker/xunfei2ui/static:/app/static ， 这样的好处是，在脚本common.js 中有一处把域名写死了为xunfei.qiangtu.com的地方，你可以改过来不受影响,这样你就可以使用https域名了，没https就没必要折腾这个映射。
- 启动

### 推荐链接

https://github.com/sdcb/Sdcb.SparkDesk

Sdcb.SparkDesk is an unofficial open-source project that provides a .NET client for SparkDesk WebSocket API(https://console.xfyun.cn/services/cbm). 
Upstream document: https://www.xfyun.cn/doc/spark/Guide.html

It can be used to build chatbots and virtual assistants that can communicate with users in natural language.

Sdcb.SparkDesk 是讯飞星火大模型WebSocket API的非官方.NET开源客户端 (https://console.xfyun.cn/services/cbm)。

 # iFLYTEK Xinghuo Demo

![img](https://memosfile.qiangtu.com/picgo/assets/2023/06/29202306_29000618.png)

This project is cloned from https://github.com/qnmlgbd250/appset.

In order to test the iFLYTEK Xinghuo API, I found a solution that is easy to use.

Implemented page: http://xunfei.qiangtu.com

### A Gentle Reminder

- This project still aims to support OPENAI. I made some modifications to the connection information, fixed a small bug, and added Docker deployment.
- Connecting to the iFLYTEK API relies on my other project, xunfei2gpt, which is still a work in progress. It converts the original websocket support from iFLYTEK to OPENAI API support. It is currently unable to support more OPENAI clients.
- This project is a work in progress. If you need advanced GPT development, please contact the original author.
- I welcome discussions on iFLYTEK API development.

### Next Steps

- There are currently no plans for further development in this project. The testing key for iFLYTEK API tokens will be quickly consumed, so without testing requirements, this project will be in a paused state.
- If you are interested and would like to share your iFLYTEK related keys with me, please contact me at https://t.me/Odinluo.

### How to Apply for iFLYTEK API Keys

It seems like you will need manual support to access the keys.

- Create an application at https://console.xfyun.cn/app/create?redirect=%2Fapp%2Fmyapp
- Obtain the APPID at https://console.xfyun.cn/services/cbm
- Go to https://xinghuo.xfyun.cn/ and click on "合作咨询" at the bottom of the page.
- Fill out the form to apply for access capabilities.

### Deployment Instructions

- The Docker image has already been implemented at odinluo/xunfei2ui.
- Simply pull it and pay attention to updating the IP and port of xunfei2gpt in the environment variables, replacing the original content of 192.168.2.101:xxx with your own.
- Specify a mapped port. The original web service port is 20235. You can specify your own external port, such as 8080:20235.
- It is recommended to map the directory /app/static. For example, you can refer to /docker/xunfei2ui/static:/app/static. The benefit of this is that there is a hardcoded domain name "xunfei.qiangtu.com" in the script common.js. You can change it without any impact, so you can use an HTTPS domain name. Otherwise, there is no need to bother with this mapping.
- Start the deployment.

### Recommended Links

https://github.com/sdcb/Sdcb.SparkDesk

Sdcb.SparkDesk is an unofficial open-source project that provides a .NET client for the SparkDesk WebSocket API (https://console.xfyun.cn/services/cbm).
Upstream document: https://www.xfyun.cn/doc/spark/Guide.html

It can be used to build chatbots and virtual assistants that can engage in natural language communication with users.

Sdcb.SparkDesk 是讯飞星火大模型WebSocket API的非官方.NET开源客户端 (https://console.xfyun.cn/services/cbm)。