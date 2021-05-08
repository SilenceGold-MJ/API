#!/user/bin/env python3
# -*- coding: utf-8 -*-
from framework.logger import Logger
import json

logger = Logger(logger="Out").getlog()

class Out_info:
    def html_out_info(self,data):
        print("测试项目："+str(data['project']))
        print('测试项名称：' + str(data["testname"]))
        print('请求地址：' + (data["url"]))
        print('请求头：' + str(data["headers"]))
        print('请求参数：' + json.dumps(data["param"]))
        print('请求方式：' + str(data["method"]))
        print('响应时间：' + str(data["time"]))
        print('响应码：' + str(data["Status_Code"]))
        print('响应报文：' + str(data["Response_Data"]))
        print('断言关键字：' + str(data["expect"]))

        if str(data["expect"]) in str(data["Response_Data"]):
            result1 = "通过"
        else:
            result1 = "失败"
        logger.info('《' + str(data["project"] + '》' + ',《' + str(
            data["testname"]) + '》项，接口测试' + result1 + '。响应时间：' + str(data["time"]) + '、状态码：' + str(data["Status_Code"])))

