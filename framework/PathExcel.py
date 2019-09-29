import os

from framework.logger import Logger
logger = Logger(logger="PathExcel").getlog()
class PathExcel():
    def path_excel(self):
        excle = os.listdir(os.path.abspath('.') + '\\data_excel\\')
        path_excel=[]
        for i in excle:
            path_excel.append(os.path.join(os.path.abspath('.') + '\\data_excel\\',i))
        return path_excel