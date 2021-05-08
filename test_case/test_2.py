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
        testname="新增车辆"
        expect="保存成功"
        param={"carName":"tets1","carCode":"tets1","companyId":2,"carType":"railway","currentLocation":"tets1"}
        data=RequestAPI().API_post_code("vehicle/sytcarinfo/add",param,token)
        data.update({"testname":testname,'expect':expect,"project":project})
        Out_info().html_out_info(data)

        self.assertIn(str(data["expect"]),str(data["Response_Data"]))

    def test_002(self):
        testname = "删除车辆"
        expect = "删除成功"
        param = {}
        data_car_list = RequestAPI().API_get_code("vehicle/sytcarinfo/page?current=1&size=10&carType=&provinceCode=420000&cityCode=420100&companyId=&healthStatus=&workState=&carCode=tets1", param, token)['Response_Data']["data"]

        data = RequestAPI().API_delete_code("vehicle/sytcarinfo/del/%s" % data_car_list['records'][0]["carId"], param, token)
        data.update({"testname": testname, 'expect': expect, "project": project})
        Out_info().html_out_info(data)

        self.assertIn(str(data["expect"]), str(data["Response_Data"]))
    def test_003(self):
        testname = "编辑车辆"
        expect = "修改成功"
        param = {}
        data_car_list = RequestAPI().API_get_code("vehicle/sytcarinfo/page?cityCode=610300&current=1&provinceCode=610000&size=5", param, token)['Response_Data']["data"]

        data_carinfo = RequestAPI().API_get_code("vehicle/sytcarinfo/get/%s" % data_car_list['records'][0]["carId"], param, token)["Response_Data"]['data']
        data=RequestAPI().API_put_code("vehicle/sytcarinfo/edit",data_carinfo,token)
        data.update({"testname": testname, 'expect': expect, "project": project})
        Out_info().html_out_info(data)

        self.assertIn(str(data["expect"]), str(data["Response_Data"]))

    def test_050(self):

        testname="获取ws地址"
        expect=str(url.split(":")[1])
        data_login = RequestAPI().API_post_code("sys/login", {"userName":"huangpeng002","password":"a111111"}, token)['Response_Data']

        param={"carName":"tets1","carCode":"tets1","companyId":2,"carType":"railway","currentLocation":"tets1"}
        data=RequestAPI().API_get_code("sys/user/getSocketUrl/%s"%data_login['data']['userId'],param,token)

        data.update({"testname":testname,'expect':expect,"project":project})
        Out_info().html_out_info(data)

        self.assertIn(str(url.split(":")[1]),str(data["Response_Data"]))
    def test_051(self):
        testname="新增报表"
        expect="成功"
        param={"diseaseTypeList":["disease_type_spalling","disease_type_leak_water","disease_type_crackle","radar_disease_type_3","radar_disease_type_4","radar_disease_type_1","radar_disease_type_2"],"periodId":1,"stageId":1,"tunnelId":1}
        data=RequestAPI().API_post_code("report/syt/add",param,token)

        data.update({"testname":testname,'expect':expect,"project":project})
        Out_info().html_out_info(data)

        self.assertIn(expect,str(data["Response_Data"]))


    def test_052(self):
        import requests
        testname="查看下载Excle"
        expect="404 Not Found"
        data_Excle = RequestAPI().API_get_code("report/syt/page?reportCode=&current=1&size=10", {}, token)['Response_Data']['data']
        FileUr =RequestAPI().API_get_code("sys/config/findFileUrl", {}, token)['Response_Data']['data']

        url_Ex='%s%s'%(FileUr['httpExcelUrl'],data_Excle['records'][0]['fileUrl'])
        print('测试项目：%s'%project)
        print("测试项：%s"%testname)
        print("下载地址：%s"%url_Ex)
        response = requests.request("GET", url_Ex, headers={}, data={})

        logger.info('《' + project + '项目》' + ',《' + testname + '》项，下载地址：%s'%url_Ex )
        self.assertNotIn(expect,str(response.text))

    def test_053(self):
        testname="删除报表"
        expect="删除成功"

        Excle_list = RequestAPI().API_get_code("report/syt/page?reportCode=&current=1&size=10", {}, token)['Response_Data']['data']['records']

        param={}
        data=RequestAPI().API_delete_code("report/syt/del/%s"%Excle_list[1]["reportId"],param,token)

        data.update({"testname":testname,'expect':expect,"project":project})
        Out_info().html_out_info(data)

        self.assertIn(expect,str(data["Response_Data"]))




    def test_060(self):
        testname="新增人员"
        expect="成功"
        param={"username":"huangpeng110","password":"a111111","realname":"hp","company":"单位单位单位","phone":"18392040001","email":"397135001@qq.com","roleId":1,"tunnelId":1,"perIds":[1,2,3,4,5,6]}
        data=RequestAPI().API_post_code('sys/user/add',param,token)
        data.update({"testname":testname,'expect':expect,"project":project})
        Out_info().html_out_info(data)
        self.assertIn(expect,str(data["Response_Data"]))
    def test_062(self):
        testname = "编辑人员"
        expect = "成功"
        param = {}
        data_car_list = RequestAPI().API_get_code("sys/user/queryPage?current=1&size=5&select=", param, token)['Response_Data']["data"]

        data_userinfo = RequestAPI().API_get_code("sys/user/get/%s" % data_car_list['records'][0]["userId"], param, token)["Response_Data"]['data']
        # param_info={
        #     "userId": data_userinfo['userId'],
        #     "username": "huangpeng_tets009",
        #     "realname": "hjad",
        #     "company": "huadd",
        #     "phone": "18392040045",
        #     "email": "397135487@qq.com",
        #     "roleId": 2,
        #     "tunnelId": 1,
        #     "perIds": [1, 2, 3, 4, 5, 6]
        # }
        data_userinfo.update({"tunnelId": data_userinfo['userLine']['tunnelId']})
        del data_userinfo['userPers']
        del data_userinfo['userLine']
        data_userinfo.update({"perIds": [1, 2, 3, 4, 5, 6]})
        data=RequestAPI().API_post_code("sys/user/edit",data_userinfo,token)
        data.update({"testname": testname, 'expect': expect, "project": project})
        Out_info().html_out_info(data)

        self.assertIn(str(data["expect"]), str(data["Response_Data"]))

    def test_063(self):
        testname="删除人员"
        expect="删除成功"

        user_list=RequestAPI().API_get_code('sys/user/queryPage?current=1&size=5&select=huangpeng110',{},token)['Response_Data']['data']['records']

        param={}
        data=RequestAPI().API_delete_code('sys/user/del/%s'%user_list[0]['userId'],param,token)
        data.update({"testname":testname,'expect':expect,"project":project})
        Out_info().html_out_info(data)
        self.assertIn(expect,str(data["Response_Data"]))


    def test_064(self):
        testname="新增隧道"
        expect="保存成功"
        param={"altitudeHight":"2000","buildTypeStr":"河北地铁","designSpeed":"2365","geoTypeStr":"河北地铁","rainRang":"5000","temperatureRang":"30","tunnelLength":"23546","tunnelName":"河北地铁","provinceCode":"130000","cityCode":"130100","tunnelType":"tunnel_type_1"}
        data=RequestAPI().API_post_code('tunnel/sytline/add',param,token)
        data.update({"testname":testname,'expect':expect,"project":project})
        Out_info().html_out_info(data)
        self.assertIn(expect,str(data["Response_Data"]))


    def test_064_01(self):
        testname = "编辑隧道"
        expect = "修改成功"
        param = {}
        #获取所有数据列表
        data_all_list = RequestAPI().API_get_code("tunnel/sytline/page?current=1&size=5&queryParam=", param, token)['Response_Data']["data"]
        #获取单个信息
        data_One_info = RequestAPI().API_get_code("tunnel/sytline/get/%s" % data_all_list['records'][0]["tunnelId"], param, token)["Response_Data"]['data']
        #拿到信息编辑更新
        data=RequestAPI().API_post_code("tunnel/sytline/edit",data_One_info,token)
        data.update({"testname": testname, 'expect': expect, "project": project})
        Out_info().html_out_info(data)

        self.assertIn(str(data["expect"]), str(data["Response_Data"]))
    def test_065(self):
        testname="删除隧道"
        expect="删除成功"

        user_list=RequestAPI().API_get_code('tunnel/sytline/page?current=1&size=5&queryParam=',{},token)['Response_Data']['data']['records']

        param={}
        data=RequestAPI().API_delete_code('tunnel/sytline/del?tunnelId=%s'%user_list[0]['tunnelId'],param,token)
        data.update({"testname":testname,'expect':expect,"project":project})
        Out_info().html_out_info(data)
        self.assertIn(expect,str(data["Response_Data"]))
    # def test_070(self):
    #     testname="新增病害等级"
    #     expect="成功"
    #
    #     param_2={"gradeCode":"disease_grade_1","geoType":"geo_type_wet","crackleUp":"32","crackleDown":"23","seepageUp":"3","seepageDown":"2","spallingUp":"23","spallingDown":"23","gradeDesc":"23"}
    #     data=RequestAPI().API_post_code('tunnel/sytgrade/add',param_2,token)
    #     data.update({"testname":testname,'expect':expect,"project":project})
    #     Out_info().html_out_info(data)
    #     self.assertIn(expect,str(data["Response_Data"]))

    def test_070_01(self):
        testname = "编辑病害等级"
        expect = "修改成功"
        param = {}
        #获取所有数据列表
        data_all_list = RequestAPI().API_get_code("tunnel/sytgrade/queryPage?current=1&size=5&queryParam=", param, token)['Response_Data']["data"]
        #获取单个信息
        data_One_info = RequestAPI().API_get_code("tunnel/sytgrade/get/%s" % data_all_list['records'][0]["gradeId"], param, token)["Response_Data"]['data']
        #拿到信息编辑更新
        data=RequestAPI().API_post_code("tunnel/sytgrade/edit",data_One_info,token)
        data.update({"testname": testname, 'expect': expect, "project": project})
        Out_info().html_out_info(data)

        self.assertIn(str(data["expect"]), str(data["Response_Data"]))

    # def test_071(self):
    #     testname="删除病害等级"
    #     expect="删除成功"
    #
    #     user_list=RequestAPI().API_get_code('tunnel/sytgrade/queryPage?current=1&size=5&queryParam=%E4%BA%94%E7%BA%A7',{},token)['Response_Data']['data']['records']
    #
    #     param={}
    #     data=RequestAPI().API_delete_code('tunnel/sytgrade/del/%s'%user_list[0]['gradeId'],param,token)
    #     data.update({"testname":testname,'expect':expect,"project":project})
    #     Out_info().html_out_info(data)
    #     self.assertIn(expect,str(data["Response_Data"]))



    '''

    def test_080(self):
        testname="新增工程阶段"
        expect="成功"
        param={"stageName":"施工期_tets01","tunnelId":1}
        data=RequestAPI().API_post_code('tunnel/sytstage/add',param,token)
        data.update({"testname":testname,'expect':expect,"project":project})
        Out_info().html_out_info(data)
        self.assertIn(expect,str(data["Response_Data"]))
            '''
    def test_080_01(self):
        testname = "编辑工程阶段"
        expect = "修改成功"
        param = {}
        #获取所有数据列表
        data_all_list = RequestAPI().API_get_code("tunnel/sytstage/queryPage?current=1&size=5&queryParam=", param, token)['Response_Data']["data"]
        #获取单个信息
        data_One_info = RequestAPI().API_get_code("tunnel/sytstage/get/%s" % data_all_list['records'][0]["stageId"], param, token)["Response_Data"]['data']
        #拿到信息编辑更新
        data_One_info={
            "stageId": data_One_info['stageId'],
            "stageName": data_One_info['stageName'],
            "tunnelId": data_One_info['tunnelId']
        }
        data=RequestAPI().API_post_code("tunnel/sytstage/edit",data_One_info,token)
        data.update({"testname": testname, 'expect': expect, "project": project})
        Out_info().html_out_info(data)

        self.assertIn(str(data["expect"]), str(data["Response_Data"]))
    # def test_081(self):
    #     testname = "删除工程阶段"
    #     expect = "删除成功"
    #
    #     user_list = \
    #         RequestAPI().API_get_code('tunnel/sytstage/queryPage?current=1&size=5&queryParam=%E6%96%BD%E5%B7%A5%E6%9C%9F_tets01', {},
    #                                   token)[
    #             'Response_Data']['data']['records']
    #
    #     param = {}
    #     data = RequestAPI().API_delete_code('tunnel/sytstage/del/%s' % user_list[0]['stageId'], param, token)
    #     data.update({"testname": testname, 'expect': expect, "project": project})
    #     Out_info().html_out_info(data)
    #     self.assertIn(expect, str(data["Response_Data"]))

    def test_082(self):
        testname="新增使用单位"
        expect="保存成功"
        param={"provinceCode":"610000","cityCode":"610300","companyName":"西安铁路宝鸡分局_tets001"}
        data=RequestAPI().API_post_code('tunnel/sytcompany/add',param,token)
        data.update({"testname":testname,'expect':expect,"project":project})
        Out_info().html_out_info(data)
        self.assertIn(expect,str(data["Response_Data"]))
    def test_082_01(self):
        testname = "编辑使用单位"
        expect = "修改成功"
        param = {}
        #获取所有数据列表
        data_all_list = RequestAPI().API_get_code("tunnel/sytcompany/queryPage?current=1&size=5&queryParam=", param, token)['Response_Data']["data"]
        #获取单个信息
        data_One_info = RequestAPI().API_get_code("tunnel/sytcompany/get/%s" % data_all_list['records'][0]["companyId"], param, token)["Response_Data"]['data']
        #拿到信息编辑更新
        data=RequestAPI().API_post_code("tunnel/sytcompany/edit",data_One_info,token)
        data.update({"testname": testname, 'expect': expect, "project": project})
        Out_info().html_out_info(data)

        self.assertIn(str(data["expect"]), str(data["Response_Data"]))

    def test_083(self):
        testname = "删除使用单位"
        expect = "删除成功"

        user_list = \
            RequestAPI().API_get_code('tunnel/sytcompany/queryPage?current=1&size=5&queryParam=%E8%A5%BF%E5%AE%89%E9%93%81%E8%B7%AF%E5%AE%9D%E9%B8%A1%E5%88%86%E5%B1%80_tets001', {},
                                      token)[
                'Response_Data']['data']['records']

        param = {}
        data = RequestAPI().API_delete_code('tunnel/sytcompany/del/%s' % user_list[0]['companyId'], param, token)
        data.update({"testname": testname, 'expect': expect, "project": project})
        Out_info().html_out_info(data)
        self.assertIn(expect, str(data["Response_Data"]))

    # def test_084(self):
    #     testname = "删除规则"
    #     expect = "删除成功"
    #
    #     user_list = \
    #         RequestAPI().API_get_code('tunnel/sytalarmrule/queryPage?current=1&size=5', {},
    #                                   token)[
    #             'Response_Data']['data']['records']
    #
    #     param = {}
    #     data = RequestAPI().API_delete_code('tunnel/sytalarmrule/del/%s' % user_list[0]['alarmRuleId'], param, token)
    #     data.update({"testname": testname, 'expect': expect, "project": project})
    #     Out_info().html_out_info(data)
    #     self.assertIn(expect, str(data["Response_Data"]))
    def test_084_01(self):
        testname = "编辑规则"
        expect = "修改成功"
        param = {}
        #获取所有数据列表
        data_all_list = RequestAPI().API_get_code("tunnel/sytalarmrule/queryPage?queryParam=&current=1&size=5", param, token)['Response_Data']["data"]
        #获取单个信息
        data_One_info = RequestAPI().API_get_code("tunnel/sytalarmrule/get/%s" % data_all_list['records'][0]["alarmRuleId"], param, token)["Response_Data"]['data']
        #拿到信息编辑更新
        data=RequestAPI().API_post_code("tunnel/sytalarmrule/edit",data_One_info,token)
        data.update({"testname": testname, 'expect': expect, "project": project})
        Out_info().html_out_info(data)

        self.assertIn(str(data["expect"]), str(data["Response_Data"]))
    # def test_085(self):
    #     testname="新增规则"
    #     expect="保存成功"
    #     param={"ruleName":"规则","alarmType":"alarm_rule_type_2","diseaseType":"disease_type_leak_water","gradeId":49,"ziseDown":"34","sizeUp":"56","changeRateDowm":"24","changeRateUp":"65"}
    #     data=RequestAPI().API_post_code('tunnel/sytalarmrule/add',param,token)
    #     data.update({"testname":testname,'expect':expect,"project":project})
    #     Out_info().html_out_info(data)
    #     self.assertIn(expect,str(data["Response_Data"]))

    def test_086(self):
        testname="文件地址检查"
        expect = str(url.split(":")[1])
        param={}
        data=RequestAPI().API_get_code('sys/config/findFileUrl',param,token)
        data.update({"testname":testname,'expect':expect,"project":project})
        Out_info().html_out_info(data)

        self.assertIn(expect,str(data["Response_Data"]['data']['httpFileUrl']))
    def test_087(self):
        testname="Excle地址检查"
        expect = str(url.split(":")[1])
        param={}
        data=RequestAPI().API_get_code('sys/config/findFileUrl',param,token)
        data.update({"testname":testname,'expect':expect,"project":project})
        Out_info().html_out_info(data)

        self.assertIn(expect,str(data["Response_Data"]['data']['httpExcelUrl']))


    def test_088_01(self):
        testname = "上传病害word文件"
        expect = "成功"
        param = {}
        #获取所有数据列表
        data_all_list = RequestAPI().API_get_code("diseaseRecord/listRecord?diseaseCode=&current=1&size=10&diseaseTypes=&periodId=&tunnelId=", param, token)['Response_Data']["data"]
        diseaseId=data_all_list['records'][0]["diseaseId"]
        #获取单个信息
        #data_One_info = RequestAPI().API_get_code("diseaseRecord/diseaseRecordInfo?diseaseId=%s&diseaseRecordId=%s" % (diseaseId,diseaseId), param, token)["Response_Data"]['data']
        #拿到信息上传
        dic_data={'diseaseRecordId':diseaseId}
        word_file='123.docx'
        #API_post_code_upload(self,path, dic_data,filepath,token)
        data=RequestAPI().API_post_code_upload("diseaseRecord/diseaseUploadProcFile",dic_data,word_file,token)
        data.update({"testname": testname, 'expect': expect, "project": project})
        Out_info().html_out_info(data)

        self.assertIn(str(data["expect"]), str(data["Response_Data"]))
    def test_088_02(self):
        import requests
        testname = "下载病害word文件"
        expect="404 Not Found"
        param = {}
        #获取所有数据列表
        data_all_list = RequestAPI().API_get_code("diseaseRecord/listRecord?diseaseCode=&current=1&size=10&diseaseTypes=&periodId=&tunnelId=", param, token)['Response_Data']["data"]
        diseaseId=data_all_list['records'][0]["diseaseId"]
        #获取单个信息
        data_One_info = RequestAPI().API_get_code("diseaseRecord/diseaseRecordInfo?diseaseId=%s&diseaseRecordId=%s" % (diseaseId,diseaseId), param, token)["Response_Data"]['data']
        #拿到信息上传


        FileUr =RequestAPI().API_get_code("sys/config/findFileUrl", {}, token)['Response_Data']['data']
        url_Ex='%s%s'%(FileUr['httpFileUrl'],data_One_info['procFileUrl'])
        print('测试项目：%s'%project)
        print("测试项：%s"%testname)
        print("下载地址：%s"%url_Ex)
        response = requests.request("GET", url_Ex, headers={}, data={})

        logger.info('《' + project + '项目》' + ',《' + testname + '》项，下载地址：%s'%url_Ex )
        self.assertNotIn(expect,str(response.text))
    def test_088_03(self):
        import requests
        testname = "查看病害图片"
        expect="404 Not Found"
        param = {}
        #获取所有数据列表
        data_all_list = RequestAPI().API_get_code("diseaseRecord/listRecord?diseaseCode=&current=1&size=10&diseaseTypes=&periodId=&tunnelId=", param, token)['Response_Data']["data"]
        diseaseId=data_all_list['records'][0]["diseaseId"]
        #获取单个信息
        data_One_info = RequestAPI().API_get_code("diseaseRecord/diseaseRecordInfo?diseaseId=%s&diseaseRecordId=%s" % (diseaseId,diseaseId), param, token)["Response_Data"]['data']
        #拿到信息上传


        FileUr =RequestAPI().API_get_code("sys/config/findFileUrl", {}, token)['Response_Data']['data']
        url_Ex='%s%s'%(FileUr['httpFileUrl'],data_One_info['chartsList'][0]["fileUrl"])
        print('测试项目：%s'%project)
        print("测试项：%s"%testname)
        print("下载地址：%s"%url_Ex)
        response = requests.request("GET", url_Ex, headers={}, data={})

        logger.info('《' + project + '项目》' + ',《' + testname + '》项，病害图片地址：%s'%url_Ex )
        self.assertNotIn(expect,str(response.text))
if __name__=='__main__':

    # unittest.main() # 使用main()直接运行时，将按case的名称顺序执行
    suite=unittest.TestSuite()
    #suite.addTest(Relicl("test_entrance"))# 将需要执行的case添加到Test Suite中，没有添加的不会被执行
    #suite.addTest(Relicl("test_entrance"))
    unittest.TextTestRunner().run(suite)  # 将根据case添加的先后顺序执行
