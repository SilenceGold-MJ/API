import unittest
from framework.login_token import Login_Token
from framework.RequestAPI import RequestAPI
from framework.Out_info import Out_info
import configparser,os
proDir = os.getcwd()
configPath = os.path.join(proDir, "config\config.ini")
cf = configparser.ConfigParser()

cf.read(configPath)#,encoding="utf-8-sig"
from framework.logger import Logger

logger = Logger(logger="tets_2").getlog()

url=cf.get("Data", "address")
project=cf.get("Data", "project")
#token = Login_Token().login_token()['data']['token']  # 获取登录token
token = Login_Token().token_() # 获取配置文件中的token
#token=''  #设置token为空

class Test(unittest.TestCase):


    def setUp(self):
        print  ("----------SetUp -----\n")
    def tearDown(self):
        print  ("-----------TearDown----\n")

    def test_001(self):
        testname="核对裂缝告警数量"
        expect="保存成功"
        param={"carName":"tets1","carCode":"tets1","companyId":2,"carType":"railway","currentLocation":"tets1"}
        data=RequestAPI().API_post_code("vehicle/sytcarinfo/add",param,token)
        data.update({"testname":testname,'expect':expect,"project":project})
        Out_info().html_out_info(data)

        self.assertIn(str(data["expect"]),str(data["Response_Data"]))


if __name__=='__main__':

    # unittest.main() # 使用main()直接运行时，将按case的名称顺序执行
    suite=unittest.TestSuite()
    #suite.addTest(Relicl("test_entrance"))# 将需要执行的case添加到Test Suite中，没有添加的不会被执行
    #suite.addTest(Relicl("test_entrance"))
    unittest.TextTestRunner().run(suite)  # 将根据case添加的先后顺序执行
