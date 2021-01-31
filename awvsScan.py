# -*- coding: utf-8 -*-
# @Author  : P2hm1n
# @Software: PyCharm
# @Blog    ：https://p2hm1n.com/

import requests
import sys
import json
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings()

# AWVS 默认配置信息
api_key = "1986ad8c0a5b3df4d7028d5f3c06e936cbef4c30ef4914f53a471d85f4448d84c"
awvs_url = "https://127.0.0.1:13443/"
awvs_email = "admin@admin.com"

# AWVS 扫描配置信息
scan_speed = "slow"
scan_id_type = "11111111-1111-1111-1111-111111111111"
scan_number = 2
proxy_address = "127.0.0.1"
proxy_port = 7777

# 脚本发包配置信息
awvs_headers = {
    "Content-Type": "application/json; charset=utf8",
    "X-Auth": api_key
}


def get_url(starturl):
    if starturl.endswith("/"):
        url = starturl[:-1]
    else:
        url = starturl
    return url


def check_api(aurl, aheaders, email):
    try:
        # 获取所有目标信息
        checkreq = requests.get(url=get_url(aurl) + "/api/v1/me",
                                headers=aheaders,
                                timeout=30,
                                verify=False)
    except Exception as e:
        print("exception:", e)
    if checkreq and checkreq.status_code == 200:
        checkme = checkreq.json()
        if email == checkme['email']:
            return True
        else:
            return False


def add_tasks(aurl, aheaders, urlfile):
    tatgets_add_list = []
    try:
        with open(urlfile) as all_url:
            for url in all_url.readlines():
                if url in ['\n', '\r\n'] or url.strip() == "":
                    pass
                else:
                    if "://" in url.strip():
                        add_url = url.strip()
                    else:
                        add_url = "http://" + url.strip()
                    add_data = {'address': add_url,
                                'description': 'awvsScan add',
                                'criticality': '10'}
                    try:
                        addreq = requests.post(url=get_url(aurl) + "/api/v1/targets",
                                               headers=aheaders,
                                               data=json.dumps(add_data),
                                               timeout=30,
                                               verify=False)
                        if addreq and addreq.status_code == 201:
                            print("已成功添加目标：", add_url)
                            tatgets_add_list.append(addreq.json()['target_id'])
                    except Exception as e:
                        print(e)
    except OSError as reason:
        print("发生错误！！！ 请输入正确的文件绝对路径")
    return tatgets_add_list


def del_tasks(aurl, aheaders):
    try:
        # 获取所有目标信息
        delreq = requests.get(url=get_url(aurl) + "/api/v1/targets",
                              headers=aheaders,
                              timeout=30,
                              verify=False)
    except Exception as e:
        print(get_url(awvs_url) + "/api/v1/targets", e)
    if delreq and delreq.status_code == 200:
        now_targets = delreq.json()
        if now_targets['pagination']['count'] == 0:
            print("已经全部清除")
        else:
            for tid in range(now_targets['pagination']['count']):
                targets_id = now_targets['targets'][tid]['target_id']
                try:
                    del_target = requests.delete(url=get_url(aurl) + "/api/v1/targets/" + targets_id,
                                                 headers=aheaders,
                                                 timeout=30,
                                                 verify=False)
                    if del_target and del_target.status_code == 204:
                        print("正在删除 ", now_targets['targets'][tid]['address'])
                except Exception as e:
                    print(get_url(awvs_url) + "/api/v1/targets/" + targets_id, e)
            delreq_check_number = requests.get(url=get_url(aurl) + "/api/v1/targets",
                                               headers=aheaders,
                                               timeout=30,
                                               verify=False)
            check_now_targets = delreq_check_number.text
            if len(check_now_targets) < 200:
                print("已经全部清除")
            else:
                print("请稍等...")
                time.sleep(20)


def get_all_targets_address(aurl, aheaders):
    all_targets = []
    try:
        # 获取所有目标信息
        setreq = requests.get(url=get_url(aurl) + "/api/v1/targets",
                              headers=aheaders,
                              timeout=30,
                              verify=False)
    except Exception as e:
        print(get_url(awvs_url) + "/api/v1/targets", e)
    setreq_json = setreq.json()
    for tid in range(setreq_json['pagination']['count']):
        all_targets.append(setreq_json['targets'][tid]['address'])
    return all_targets


def scan_targets(aurl, aheaders, scan_speed, scan_id_type, input_file, scan_number):
    tatgets_scan_list = add_tasks(aurl, aheaders, input_file)
    for scan_target in tatgets_scan_list:
        scan_speed_data = {
            "scan_speed": scan_speed
        }
        try:
            scan_speed_req = requests.patch(
                url=get_url(awvs_url) + "/api/v1/targets/{0}/configuration".format(scan_target),
                headers=awvs_headers,
                data=json.dumps(scan_speed_data),
                timeout=30,
                verify=False)
        except Exception as e:
            print(e)
    if len(tatgets_scan_list) <= scan_number:
        for add_scan_target in tatgets_scan_list:
            add_scan_target_data = {
                "target_id": add_scan_target,
                "profile_id": scan_id_type,
                "incremental": False,
                "schedule": {
                    "disable": False,
                    "start_date": None,
                    "time_sensitive": False
                }
            }
            try:
                add_scan_req = requests.post(url=get_url(aurl) + "/api/v1/scans",
                                             headers=aheaders,
                                             data=json.dumps(add_scan_target_data),
                                             timeout=30,
                                             verify=False)
                if add_scan_req and add_scan_req.status_code == 201:
                    get_add_scan_info_json = get_all_scan_info(aurl, aheaders, add_scan_target)
                    print(get_add_scan_info_json['scans'][0]['profile_name'], "模式启动扫描，",
                          "开始扫描：", get_add_scan_info_json['scans'][0]['target']['address'])
            except Exception as e:
                print(e)
        print("正在添加任务，请稍等...")
        time.sleep(3)
        print("正在扫描任务数为：", get_dashboard_info(aurl, aheaders)['scans_running_count'])
    else:
        flag = 0
        while flag < len(tatgets_scan_list):
            now_scan_number = get_dashboard_info(aurl, aheaders)['scans_running_count']
            print("now_scan_number", now_scan_number)
            if now_scan_number < scan_number:
                add_scan_target_data = {
                    "target_id": tatgets_scan_list[flag],
                    "profile_id": scan_id_type,
                    "incremental": False,
                    "schedule": {
                        "disable": False,
                        "start_date": None,
                        "time_sensitive": False
                    }
                }
                try:
                    add_scan_req = requests.post(url=get_url(aurl) + "/api/v1/scans",
                                                 headers=aheaders,
                                                 data=json.dumps(add_scan_target_data),
                                                 timeout=30,
                                                 verify=False)
                except Exception as e:
                    print(e)
                if add_scan_req and add_scan_req.status_code == 201:
                    get_add_scan_info_json = get_all_scan_info(aurl, aheaders, tatgets_scan_list[flag])
                    print(get_add_scan_info_json['scans'][0]['profile_name'], "模式启动扫描，",
                          "开始扫描：", get_add_scan_info_json['scans'][0]['target']['address'])
                    print("正在添加任务，请稍等...")
                    time.sleep(3)
                    print("正在扫描任务数为：", get_dashboard_info(aurl, aheaders)['scans_running_count'])
                    flag += 1
            elif now_scan_number > scan_number + 2 and now_scan_number > 6:
                print("程序bug，扫描任务过多，为保护内存，现删除所有目标并退出程序")
                del_tasks(aurl, aheaders)
                sys.exit()
            else:
                time.sleep(30)
        while True:
            now_scan_number_final = get_dashboard_info(aurl, aheaders)['scans_running_count']
            if now_scan_number_final == 0:
                print("已全部扫描完成")
            else:
                time.sleep(30)


def get_dashboard_info(aurl, aheaders):
    get_info = requests.get(url=get_url(aurl) + "/api/v1/me/stats",
                            headers=aheaders,
                            timeout=30,
                            verify=False)
    get_info_json = get_info.json()
    return get_info_json


def get_all_scan_info(aurl, aheaders, targetid):
    try:
        # 获取所有目标信息
        delreq = requests.get(url=get_url(aurl) + "/api/v1/scans?l=20&q=target_id:{0}".format(targetid),
                              headers=aheaders,
                              timeout=30,
                              verify=False)
        return delreq.json()
    except Exception as e:
        print(e)


def crawl_scan(aurl, aheaders, proxy_address, proxy_port, scan_speed, scan_number, input_file):
    crawl_scan_list = add_tasks(aurl, aheaders, input_file)
    for crawl_targetid in crawl_scan_list:
        crawl_scan_speed_data = {
            "scan_speed": scan_speed
        }
        crawl_config = {
            "user_agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                          "AppleWebKit/537.21 (KHTML, like Gecko) "
                          "Chrome/41.0.2228.0 Safari/537.21",
            "limit_crawler_scope": True,
            "excluded_paths": [],
        }
        proxy_config = {
            "proxy":
                {"enabled": True,
                 "protocol": "http",
                 "address": proxy_address,
                 "port": proxy_port
                 }
        }
        try:
            # 调整速度
            scan_speed_req = requests.patch(
                url=get_url(awvs_url) + "/api/v1/targets/{0}/configuration".format(crawl_targetid),
                headers=awvs_headers,
                data=json.dumps(crawl_scan_speed_data),
                timeout=30,
                verify=False)
            # 设置爬虫
            crawl_config_req = requests.patch(
                url=get_url(awvs_url) + "/api/v1/targets/{0}/configuration".format(crawl_targetid),
                headers=awvs_headers,
                data=json.dumps(crawl_config),
                timeout=30,
                verify=False)
            # 设置 http 代理
            http_config_req = requests.patch(
                url=get_url(awvs_url) + "/api/v1/targets/{0}/configuration".format(crawl_targetid),
                headers=awvs_headers,
                data=json.dumps(proxy_config),
                timeout=30,
                verify=False)
        except Exception as e:
            print(e)
        if len(crawl_scan_list) <= scan_number:
            for add_scan_target in crawl_scan_list:
                add_scan_target_data = {
                    "target_id": add_scan_target,
                    "profile_id": "11111111-1111-1111-1111-111111111117",
                    "incremental": False,
                    "schedule": {
                        "disable": False,
                        "start_date": None,
                        "time_sensitive": False
                    }
                }
                try:
                    add_scan_req = requests.post(url=get_url(aurl) + "/api/v1/scans",
                                                 headers=aheaders,
                                                 data=json.dumps(add_scan_target_data),
                                                 timeout=30,
                                                 verify=False)
                    if add_scan_req and add_scan_req.status_code == 201:
                        time.sleep(30)
                        get_add_scan_info_json = get_all_scan_info(aurl, aheaders, add_scan_target)
                        print(get_add_scan_info_json['scans'][0]['profile_name'], "模式启动扫描，",
                              "开始扫描：", get_add_scan_info_json['scans'][0]['target']['address'])
                except Exception as e:
                    print(e)
            print("正在添加任务，请稍等...")
            time.sleep(3)
            print("正在扫描任务数为：", get_dashboard_info(aurl, aheaders)['scans_running_count'])

        else:
            flag = 0
            while flag < len(crawl_scan_list):
                now_scan_number = get_dashboard_info(aurl, aheaders)['scans_running_count']
                print("now_scan_number", now_scan_number)
                if now_scan_number < scan_number:
                    add_scan_target_data = {
                        "target_id": crawl_scan_list[flag],
                        "profile_id": scan_id_type,
                        "incremental": False,
                        "schedule": {
                            "disable": False,
                            "start_date": None,
                            "time_sensitive": False
                        }
                    }
                    try:
                        add_scan_req = requests.post(url=get_url(aurl) + "/api/v1/scans",
                                                     headers=aheaders,
                                                     data=json.dumps(add_scan_target_data),
                                                     timeout=30,
                                                     verify=False)
                    except Exception as e:
                        print(e)
                    if add_scan_req and add_scan_req.status_code == 201:
                        get_add_scan_info_json = get_all_scan_info(aurl, aheaders, crawl_scan_list[flag])
                        print(get_add_scan_info_json['scans'][0]['profile_name'], "模式启动扫描，",
                              "开始扫描：", get_add_scan_info_json['scans'][0]['target']['address'])
                        print("正在添加任务，请稍等...")
                        time.sleep(3)
                        print("正在扫描任务数为：", get_dashboard_info(aurl, aheaders)['scans_running_count'])
                        flag += 1
                elif now_scan_number > scan_number + 2 and now_scan_number > 6:
                    print("程序bug，扫描任务过多，为保护内存，现删除所有目标并退出程序")
                    del_tasks(aurl, aheaders)
                    sys.exit()
                else:
                    time.sleep(30)
            while True:
                now_scan_number_final = get_dashboard_info(aurl, aheaders)['scans_running_count']
                if now_scan_number_final == 0:
                    print("已全部扫描完成")
                else:
                    time.sleep(30)


def main():
    if check_api(awvs_url, awvs_headers, awvs_email):
        print("AWVS API 认证成功")
        print("""
1. 清空 AWVS Targets 列表所有目标
2. 列出 AWVS Targets 列表所有目标
3. 批量添加 url 至 AWVS Targets 列表，但不进行扫描
4. 批量添加 url 至 AWVS Targets 列表，并进行主动扫描（可控制同时扫描的任务数量）
5. 批量添加 url 至 AWVS Targets 列表，仅爬虫模式，联动 Xray 进行扫描（可控制同时扫描的任务数量）
6. 对于脚本有更好的建议
            """)
        while True:
            try:
                choose = int(input("请选择运行的模式："))
                break
            except ValueError:
                print("请选择数字编号作为运行的模式，如：2")
        if choose == 1:
            del_tasks(awvs_url, awvs_headers)
        elif choose == 2:
            get_address = get_all_targets_address(awvs_url, awvs_headers)
            if len(get_address) == 0:
                print("AWVS Targets 列表为空, 请先传入 target")
            else:
                for _ in get_address:
                    print(_.strip())
        elif choose == 3:
            input_file_a = input("请输出传入文件绝对路径：")
            add_tasks(awvs_url, awvs_headers, input_file_a.strip())
        elif choose == 4:
            input_file_b = input("请输出传入文件绝对路径：")
            scan_targets(awvs_url,
                         awvs_headers,
                         scan_speed,
                         scan_id_type,
                         input_file_b.strip(),
                         scan_number)
        elif choose == 5:
            input_file_c = input("请输出传入文件绝对路径：")
            crawl_scan(awvs_url,
                       awvs_headers,
                       proxy_address,
                       proxy_port,
                       scan_speed,
                       scan_number,
                       input_file_c)
        elif choose == 6:
            print("vx: U2VjLU1pbgo=", "欢迎私戳")
        else:
            print("您的选项有误，请选择正确的选项")
            sys.exit()
    else:
        print("api 认证失败，请检查 api_key")
        sys.exit()


if __name__ == '__main__':
    main()
