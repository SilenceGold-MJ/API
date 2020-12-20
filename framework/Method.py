from framework.RequestAPI import RequestAPI
from framework.logger import Logger
logger = Logger(logger="Merhod").getlog()
class Merhod():

    def merhod(self,url,method, param,headers,testname ):#expect,sheet1,  row
        #logger.info([url,method, param,headers,testname])
        try:
            if method in ['get','GET']:
                APIdata=RequestAPI().get(url, param.encode(),headers, testname)
                #logger.info([url, param,headers, testname,APIdata])
                #logger.info([testname,url, param,  APIdata])
                return APIdata
                #RequestAPI.writedata(API_data, expect, sheet1, row, testname)

            elif  method in ['post','POST']:
                APIdata=RequestAPI().API_post(url, param.encode(),headers, testname)
                #logger.info([testname,url, param,  APIdata])
                #logger.info(APIdata)
                return APIdata
                #RequestAPI.writedata(API_data, expect, sheet1, row, testname)
            elif method in ['delete','DELETE']:

                APIdata=RequestAPI().API_delete(url, param.encode(),headers, testname)
                #logger.info([testname,url, param,  APIdata])
                #logger.info(APIdata)
                return APIdata

        except Exception as e:
            #logger.error(e)
            logger.error('《' + str(testname) + '》项异常，请检查网络、接口地址、入参是否正常！！！'+str(e))
