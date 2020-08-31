#!/user/bin/env python3
# -*- coding: utf-8 -*-
from framework.Method import Merhod
from framework.GetExceltolist import GetExceltolist

for i in (GetExceltolist().GetExceltolist()):
    url, method, param, headers, testname=i['url'],i['method'],i['param'],i['headers'],i['testname'],
    apidata=Merhod().merhod(url,method, param,headers,testname)
    print(apidata)



