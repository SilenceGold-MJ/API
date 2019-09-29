from framework.FindValue import FindValue
from framework.logger import Logger
logger = Logger(logger="WriteData").getlog()
class WriteData():

    def writedata(self,PM,expect,sheet1,row,testname):

        #PM['Response_Data'] = PM['Response_Data'] .replace("'", '"')  # 替换"'", '"'
        #dict_data = json.loads(PM['Response_Data'] )  # 转python字典

        if FindValue.find_value(self,PM['Response_Data'] , expect) == True:  # ReadAPI.get(url, param,testname)[3])==200:
            sheet1.cell(row=row, column=8, value=str(PM['Response_Data']))  # 响应结果
            sheet1.cell(row=row, column=9, value=PM['time'])  # 请求时间
            sheet1.cell(row=row, column=10, value=int(PM['Status_Code']))  # 状态码
            sheet1.cell(row=row, column=11, value="pass")  # 判断通过
            #logger.info('《' + str(testname) + '》项，响应成功、响应时间：' + str(PM['time']) + '、状态码：' + str(PM['Status_Code']))
            return "pass"

        else:
            sheet1.cell(row=row, column=8, value=str(PM['Response_Data']))  # 响应结果
            sheet1.cell(row=row, column=9, value=PM['time'])  # 请求时间
            sheet1.cell(row=row, column=10, value=int(PM['Status_Code']))  # 状态码
            sheet1.cell(row=row, column=11, value="fail")  # 判断通过
            #logger.info('《' + str(testname) + '》项，响应成功、响应时间：' + str(PM['time']) + '、状态码：' + str(PM['Status_Code']))
            return "fail"



