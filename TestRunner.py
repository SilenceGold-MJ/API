"""
version: 1.7
test_1,将所有表格中的数据读取到字典中，添加至每条用例执行，测试结果填写到Excel中，并将测试结果展示到Html报告中（合二为一）。

"""
#import HTMLTestRunner
import os
import unittest
import time
from tools.HTMLTestRunner import HTMLTestRunner

if __name__ =='__main__':
    suite = unittest.TestLoader().discover("test_case")
    report_path = os.path.join(os.getcwd() + '\\test_report\\')
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    HtmlFile = report_path + now + "HTMLtemplate.html"
    fp = open(HtmlFile, "wb")
    runner = HTMLTestRunner(stream=fp, title=u"自动化测试报告", description=u"用例测试情况")  #from tools.HTMLTestRunner import HTMLTestRunner
    runner.run(suite)
    fp.close()
    #input('Press Enter to exit...')
