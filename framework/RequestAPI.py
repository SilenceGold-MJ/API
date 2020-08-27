import requests
import json
from framework.logger import Logger
logger = Logger(logger="RequestAPI").getlog()
class RequestAPI():
    def get(self, url, param,headers,testname):
        param = eval(param)  # Exel读出来的数据类型是字符串，而get请求的入参必须是字典类型，post请求的入参是json字符串类型
        headers = eval(headers)
        try:
            r = requests.get(url, params=param,headers=headers)
            r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
        except requests.RequestException as e:
            #print(e)
            return {
                "testname": testname,
                "time": 'error',
                "Status_Code": 'error',
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

    def post(self, url, param,headers,testname):
        payload = (param)

        headers = eval(headers)
        try:
            r = requests.post(url, data=payload,headers=headers)
            r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
        except requests.RequestException as e:
            #print(e)
            return {
                "testname": testname,
                "time": 'error',
                "Status_Code": 'error',
                "Response_Data": e,
            }

        else:
            js = json.dumps(r.json())
            #logger.info('请求项名称：' + testname + '、请求响应时间：' + str(r.elapsed.total_seconds()), '、请求状态：' + str(r.status_code))
            return {
                       "testname":testname,
                       "time":r.elapsed.total_seconds(),
                        "Status_Code":r.status_code,
                       "Response_Data":r.json(),
                    }
            #logger.info(r.json())

    def API_post(self,url, param,headers,testname):
        headers =eval(headers)
        r = requests.request("POST", url, headers=headers, data=param)
        dic={
            "testname": testname,
            "time": r.elapsed.total_seconds(),
            "Status_Code": r.status_code,
            "Response_Data": r.text,
        }
        #logger.info("dic:%s"%dic)
        return dic
