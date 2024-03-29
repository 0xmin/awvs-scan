![awvs-scan](https://socialify.git.ci/0xmin/awvs-scan/image?description=1&font=Source%20Code%20Pro&forks=1&issues=1&language=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Light)

## 主要功能

主要实现以下功能

1. 清空 AWVS Targets 列表所有目标
2. 列出 AWVS Targets 列表所有目标
3. 批量添加 url 至 AWVS Targets 列表，但不进行扫描
4. 批量添加 url 至 AWVS Targets 列表，并进行主动扫描（可控制同时扫描的任务数量）
5. 批量添加 url 至 AWVS Targets 列表，仅爬虫模式，联动 Xray 进行扫描（可控制同时扫描的任务数量）



如果想自定义更多高级配置，可以选择第三个模式，导入目标后手动配置更多选项

## 配置信息

基础配置

```txt
# api 
api_key = ""

# 填写 AWVS 主页 URL
awvs_url = ""

# 填写 AWVS 登陆账户 email
awvs_email = ""
```

`scan_speed` 参考以下选项

| 参数       | 类型   | 说明                                        |
| :--------- | :----- | :------------------------------------------ |
| scan_speed | string | sequential <br>slow <br/>moderate <br/>fast |

`scan_id_type`参考以下选项

| 类型 | 值   |
| :----------------------------------- | :----------------------------------- |
| Full Scan                            | 11111111-1111-1111-1111-111111111111 |
| High Risk Vulnerabilities            | 11111111-1111-1111-1111-111111111112 |
| Cross-site Scripting Vulnerabilities | 11111111-1111-1111-1111-111111111116 |
| SQL Injection Vulnerabilities        | 11111111-1111-1111-1111-111111111113 |
| Weak Passwords                       | 11111111-1111-1111-1111-111111111115 |
| Crawl Only                           | 11111111-1111-1111-1111-111111111117 |
| Malware Scan                         | 11111111-1111-1111-1111-111111111120 |

`scan_number` 为同时扫描的任务数量（建议为3）



爬虫模式代理相关配置

```
# 使用代理的主机
proxy_address = "127.0.0.1"
# 使用代理的端口
proxy_port = 7777
```

## 使用方式

运行脚本可以选择运行的模式

- **列出 AWVS Targets 列表所有目标 （AWVS Targets 列表为空时）**

![](README/image-20210130195522986.png)



- **列出 AWVS Targets 列表所有目标 （AWVS Targets 列表不为空时）**

![](README/image-20210130195905560.png)



- **清空 AWVS Targets 列表所有目标**

![](README/image-20210130200116892.png)



- **批量添加 url 至 AWVS Targets 列表，但不进行扫描**

![](README/image-20210130195734971.png)



- **批量添加 url 至 AWVS Targets 列表，并进行主动扫描（可控制同时扫描的任务数量）**

![](README/image-20210130200315600.png)



- **批量添加 url 至 AWVS Targets 列表，仅爬虫模式，联动 Xray 进行扫描（可控制同时扫描的任务数量）**



效果同上

## 免责声明

本工具仅能在取得足够合法授权的企业安全建设中使用，在使用本工具过程中，您应确保自己所有行为符合当地的法律法规。 如您在使用本工具的过程中存在任何非法行为，您将自行承担所有后果，本工具所有开发者和所有贡献者不承担任何法律及连带责任。 除非您已充分阅读、完全理解并接受本协议所有条款，否则，请您不要安装并使用本工具。 您的使用行为或者您以其他任何明示或者默示方式表示接受本协议的，即视为您已阅读并同意本协议的约束。


## 参考资料

[AWVS13.X API学习记录](https://www.sqlsec.com/2020/04/awvsapi.html#toc-heading-32)

[xray 安全评估工具文档](https://docs.xray.cool/)

