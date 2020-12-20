# API

1.功能：  
将指定路径下的所有Excel的接口用例读取后，执行用例，测试结果填写到Excel中，并输出Html自动化测试报告。

2.运行之前请安装下面库，已安装过的不用安装  
pip3 install openpyxl  
pip3 install requests  
pip3 install ddt  

3.更新  

2020-12-20更新  
1.添加deleteq请求方式
2.添加token获取保存至config
2.tets_2代码中添加动态参数接口测试，静态参数在Excle中添加，tets_1运行测试


2020-08-31更新  
1.修改断言校验方式  
2.添加请求方式post\get大小写兼容  
3.添加配置文件地址和Excel拼接完整地址  
4.修改请求参数不能为中文  
5.更新html报告模板  
6.兼容完整请求地址和拼接请求地址  
