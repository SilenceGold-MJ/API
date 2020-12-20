import requests
import json
from framework.logger import Logger

import configparser,os
proDir = os.getcwd()
configPath = os.path.join(proDir, "config\config.ini")
cf = configparser.ConfigParser()

cf.read(configPath)#encoding="utf-8-sig"
logger = Logger(logger="RequestAPI").getlog()
class RequestAPI():
    def get(self, url, param,headers,testname):
        param = eval(param)  # Exel读出来的数据类型是字符串，而get请求的入参必须是字典类型，post请求的入参是json字符串类型
        #headers = eval(headers)
        headers.update({'Content-Type': 'application/json;charset=UTF-8',})

        try:
            r = requests.get(url, params=param,headers=headers)
            r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
        except requests.RequestException as e:
            #print(e)
            return {
                "testname": testname,
                "time": 'error',
                "Status_Code": 500,
                "Response_Data": e,
            }

        else:
            js = json.dumps(r.json())
            #logger.info( '请求项名称：'+testname+'、请求响应时间：'+str(r.elapsed.total_seconds()),'、请求状态：'+str(r.status_code))
            return {
                "testname": testname,
                "time": r.elapsed.total_seconds(),
                "Status_Code": r.status_code,
                "Response_Data": r.json(),
            }
    #
    # def post(self, url, param,headers,testname):
    #     payload = (param)
    #
    #     #headers = eval(headers)
    #     try:
    #         r = requests.post(url, data=payload,headers=headers)
    #         r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
    #     except requests.RequestException as e:
    #         #print(e)
    #         return {
    #             "testname": testname,
    #             "time": 'error',
    #             "Status_Code": 'error',
    #             "Response_Data": e,
    #         }
    #
    #     else:
    #         js = json.dumps(r.json())
    #         #logger.info('请求项名称：' + testname + '、请求响应时间：' + str(r.elapsed.total_seconds()), '、请求状态：' + str(r.status_code))
    #         return {
    #                    "testname":testname,
    #                    "time":r.elapsed.total_seconds(),
    #                     "Status_Code":r.status_code,
    #                    "Response_Data":r.json(),
    #                 }
    #         #logger.info(r.json())

    def API_post(self,url, param,headers,testname):
        #headers =eval(headers)
        headers.update({'Content-Type': 'application/json',})
        #{'Content-Type': 'application/json;charset=UTF-8', }

        try:
            r = requests.request("POST", url, headers=headers, data=param)
            dic = {
                "testname": testname,
                "time": r.elapsed.total_seconds(),
                "Status_Code": r.status_code,
                "Response_Data": r.text,
            }
            # logger.info("dic:%s"%dic)
        except requests.RequestException as e:

            dic = {
                "testname": testname,
                "time": 'error',
                "Status_Code": 500,
                "Response_Data": e,
            }

            # logger.info("dic:%s"%dic)
        return dic

    def API_delete(self,url, param,headers,testname):
        # url = "http://192.168.1.200:9090/hyh/vehicle/sytcarinfo/del/119"
        #
        # payload = {}
        # headers = {
        #     'token': '56c58e9d2d6ca17283010448d1afcbad',
        #     'Cookie': 'JSESSIONID=EA7C1E4A0A319AC4AB980DB58510D89B'
        # }
        #
        # response = requests.request("DELETE", url, headers=headers, data=payload)
        #
        # print(response.text)
        param = eval(param)#转字典类型
        headers.update({'Content-Type': 'application/json',})
        #{'Content-Type': 'application/json;charset=UTF-8', }

        try:
            r = requests.request("DELETE", url, headers=headers, data=param)
            dic = {
                'param':param,
                "testname": testname,
                "time": r.elapsed.total_seconds(),
                "Status_Code": r.status_code,
                "Response_Data": r.text,
            }
            # logger.info("dic:%s"%dic)
        except requests.RequestException as e:

            dic = {
                "testname": testname,
                "time": 'error',
                'param': param,
                "Status_Code": 500,
                "Response_Data": e,
            }

            # logger.info("dic:%s"%dic)
        return dic
    #######################################################################
    def API_post_code(self,path, param,token):
        url='%s%s'%(cf.get("Data", "address"),path)#无前缀读取配置文件添加前缀
        headers={'Content-Type': 'application/json',"token":token}
        try:
            r = requests.request("POST", url, headers=headers, data=json.dumps(param))
            dic = {
                'param': param,
                "time": r.elapsed.total_seconds(),
                "headers": headers,
                "url":url,
                "Status_Code": r.status_code,
                "Response_Data": json.loads(r.text),
                "method":"POST"
            }
            # logger.info("dic:%s"%dic)
        except requests.RequestException as e:

            dic = {
                'param': param,
                "time": 'error',
                "headers": headers,
                "url": url,
                "Status_Code": 500,
                "Response_Data": e,
                "method": "POST"
            }

            # logger.info("dic:%s"%dic)
        return dic
    def API_get_code(self, path, param,token):
        url='%s%s'%(cf.get("Data", "address"),path)#无前缀读取配置文件添加前缀
        headers={'Content-Type': 'application/json',"token":token}
        try:
            r = requests.get(url, params=param,headers=headers)
            r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
        except requests.RequestException as e:
            #print(e)
            return {
                'param': param,
                "headers": headers,
                "url": url,
                "time": 'error',
                "Status_Code": 500,
                "Response_Data": e,
                "method": "GET"
            }

        else:
            js = json.dumps(r.json())
            #logger.info( '请求项名称：'+testname+'、请求响应时间：'+str(r.elapsed.total_seconds()),'、请求状态：'+str(r.status_code))
            return {
                'param': param,
                "headers": headers,
                "url": url,
                "time": r.elapsed.total_seconds(),
                "Status_Code": r.status_code,
                "Response_Data": json.loads(r.text),
                "method": "GET"
            }
    def API_delete_code(self, path, param,token):
        url='%s%s'%(cf.get("Data", "address"),path)#无前缀读取配置文件添加前缀
        headers={'Content-Type': 'application/json',"token":token}

        try:
            r = requests.request("DELETE", url, headers=headers, data=param)
            dic = {
                'param': param,
                "time": r.elapsed.total_seconds(),
                "headers": headers,
                "url":url,
                "Status_Code": r.status_code,
                "Response_Data": json.loads(r.text),
                "method":"DELETE"
            }
            # logger.info("dic:%s"%dic)
        except requests.RequestException as e:

            dic = {
                'param': param,
                "headers": headers,
                "url": url,
                "time": 'error',
                "Status_Code": 500,
                "Response_Data": e,
                "method": "DELETE"
            }

            # logger.info("dic:%s"%dic)
        return dic
