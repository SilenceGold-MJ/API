
import configparser,os,requests,json
proDir = os.getcwd()
configPath = os.path.join(proDir, "config\config.ini")
cf = configparser.ConfigParser()
cf.read(configPath)#encoding="utf-8-sig"






class Login_Token():
    def API_post_202012(self,url, payload):
        headers = {
            'Content-Type': 'application/json',
        }
        payload=json.dumps(payload)

        response = requests.request("POST", "%s" % (url), headers=headers, data=payload)
        re = json.loads(response.text)
        # print('入参：%s;返回值：%s' % (payload, re))
        return re

    def login_token(self,):
        url = '%s%s' % (cf.get("Data", "address"), 'sys/login')  # 登录
        payload = {"userName": cf.get("Data", "userName"), "password": cf.get("Data", "password")}  # 登录
        try:
            data = Login_Token().API_post_202012(url, payload)  # 登录

            cf.set("Data", "token", data["data"]["token"])#更新入ini
            #cf.write(open(configPath ,"w"),'utf-8')#写入
            with open(configPath, 'w') as configfile:
                cf.write(configfile,"utf-8-sig")



            return data
        except:
            return {"code":40044,"msg":"异常","data":{"token":""}}


    def token_(self,):
        return cf.get("Data", "token")

