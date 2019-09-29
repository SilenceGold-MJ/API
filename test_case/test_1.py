import unittest
from framework.logger import Logger
import ddt
from framework.FindValue import FindValue
from framework.Method import Merhod
from framework.GetExceltolist import GetExceltolist
from framework.WExcel import WExcel
logger = Logger(logger="Test1").getlog()
GetExceltolist =GetExceltolist()
@ddt.ddt
class Test(unittest.TestCase):
    def setUp(self):
        print  ("----------SetUp -----\n")
    def tearDown(self):
        print  ("-----------TearDown----\n")
    @ddt.data(*GetExceltolist.GetExceltolist())
    def test_1(self,data):


        PM=Merhod.merhod(self,data["url"],data["method"], data["param"], data["headers"],data["testname"])
        print('测试Excel名称：' + str(data["path_ex"]).split('\\')[-1])
        print('测试项名称：'+str(data["testname"]))
        print('请求地址：' + (data["url"]))
        print('请求参数：' + str(data["param"]))
        print('请求方式：' + str(data["method"]))
        print('响应时间：'+str(PM["time"]))
        print('响应码：'+str(PM["Status_Code"]))
        print('响应报文：'+ str(PM["Response_Data"]))
        print('断言关键字：'+str(data["expect"]))
        logger.info('《'+str(data["path_ex"].split('\\')[-1])+'用例》'+'；《' + str(data["testname"]) + '》项，请求成功。响应时间：' + str(PM["time"]) + '、状态码：' + str(PM["Status_Code"]))
        WExcel.WExcel(self,data["path_ex"],PM,data["expect"],data["row"]+1,data["path_ex"].split('\\')[-1])
        self.assertEqual(FindValue.find_value(self,PM["Response_Data"],data["expect"]),True)

if __name__=='__main__':

    # unittest.main() # 使用main()直接运行时，将按case的名称顺序执行
    suite=unittest.TestSuite()
    #suite.addTest(Relicl("test_entrance"))# 将需要执行的case添加到Test Suite中，没有添加的不会被执行
    #suite.addTest(Relicl("test_entrance"))
    unittest.TextTestRunner().run(suite)  # 将根据case添加的先后顺序执行
