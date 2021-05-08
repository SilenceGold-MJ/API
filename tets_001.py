import requests

url = 'http://192.168.1.81:9530/api/diseaseRecord/diseaseUploadProcFile'
headers = {"token": 'web_token_171d0faf7946a19ee2decf24006777ab'}
# 要上传的文件
files = {'file': open('123.docx', 'rb')}
# post携带的数据
datass = {'diseaseRecordId': 1214}
r = requests.post(url,datass,files=files,headers=headers)
print(r.text)

