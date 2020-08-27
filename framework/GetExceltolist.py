from framework.PathExcel import PathExcel
from framework.logger import Logger
from framework.RExcetodicl import RExcetodicl
logger = Logger(logger="GetExceltolist").getlog()
class GetExceltolist():

    def GetExceltolist(self):
        datalist = []
        try:
            for i in PathExcel().path_excel():
                data = RExcetodicl().RExcetodicl(i)
                datalist.extend(data["data"])
        except Exception as e:

            logger.error(str(e)+"用例Excel文件可能存在异常,或者Excel未关闭！！！")

        return datalist


