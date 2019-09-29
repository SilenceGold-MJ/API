from framework.RequestAPI import RequestAPI
from framework.logger import Logger
logger = Logger(logger="Merhod").getlog()
class Merhod():

    def merhod(self,  url,method, param,headers,testname ):#expect,sheet1,  row
        try:
            if method=='get':
                APIdata=RequestAPI.get(self,url, param,headers, testname)
                return APIdata
                #RequestAPI.writedata(API_data, expect, sheet1, row, testname)

            elif method=='post':
                APIdata=RequestAPI.post(self,url, param,headers, testname)
                return APIdata
                #RequestAPI.writedata(API_data, expect, sheet1, row, testname)

        except Exception as e:
            logger.error(e)
            logger.error('《' + str(testname) + '》项异常，请检查网络、接口地址、入参是否正常！！！')