from framework.logger import Logger
logger = Logger(logger="FindValue").getlog()
class FindValue():
    def find_value1(self,dir_data, fvalue):  #封装个在查字典中的查找value
        yesOrno = False
        for key in dir_data.keys():
            if (dir_data[key] == fvalue):

                yesOrno = True
                break
        return (yesOrno)
    def find_value(self,dir_data, fvalue):  #封装个在查字典中的查找value
        yesOrno = False
        if str(fvalue) in str(dir_data):
            yesOrno = True
        return (yesOrno)
