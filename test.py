from framework.GetExceltolist import GetExceltolist
from framework.Method import Merhod


for data in GetExceltolist().GetExceltolist():
    print(data)
    PM = Merhod().merhod(data["url"], data["method"], data["param"], data["headers"], data["testname"])


