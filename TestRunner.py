"""
version: 1.7
test_1将所有表格中的数据读取到字典中，添加至每条用例执行，测试结果填写到Excel中，并将测试结果展示到Html报告中（合二为一）。
"""
#import HTMLTestRunner
import os
import unittest
import time
from tools.HTMLTestRunner import HTMLTestRunner

if __name__ =='__main__':
    suite = unittest.TestLoader().discover("test_case")
    # 初始化一个HTMLTestRunner实例对象，用来生成报告
    # 设置报告文件保存路径
    #report_path = os.path.dirname(os.path.abspath('.')) + '/test_report/'
    report_path = os.path.join(os.getcwd() + '\\test_report\\')

    # 获取系统当前时间
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 设置报告名称格式
    HtmlFile = report_path + now + "HTMLtemplate.html"

    fp = open(HtmlFile, "wb")
    # 构建suite
    runner = HTMLTestRunner(stream=fp, title=u"自动化测试报告", description=u"用例测试情况")  #from tools.HTMLTestRunner import HTMLTestRunner
    #runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"自动化测试报告", description=u"用例测试情况") #import HTMLTestRunner
    # 开始执行测试套件
    runner.run(suite)
    fp.close()
    #input('Press Enter to exit...')

