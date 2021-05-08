"""
A TestRunner for use with the Python unit testing framework. It
generates a HTML report to show the result at a glance.
The simplest way to use this is to invoke its main method. E.g.
    import unittest
    import HTMLTestRunner

    ... define your tests ...
    if __name__ == '__main__':
        HTMLTestRunner.main()
For more customization options, instantiates a HTMLTestRunner object.
HTMLTestRunner is a counterpart to unittest's TextTestRunner. E.g.
    # output to a file
    fp = file('my_report.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='My unit test',
                description='This demonstrates the report output by HTMLTestRunner.'
                )
    # Use an external stylesheet.
    # See the Template_mixin class for more customizable options
    runner.STYLESHEET_TMPL = '<link rel="stylesheet" href="my_stylesheet.css" type="text/css">'
    # run the test
    runner.run(my_test_suite)
------------------------------------------------------------------------
Copyright (c) 2004-2007, Wai Yip Tung
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name Wai Yip Tung nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# URL: http://tungwaiyip.info/software/HTMLTestRunner.html

__author__ = "Wai Yip Tung"
__version__ = "0.8.2"

"""
Change History
Version 0.8.2
* Show output inline instead of popup window (Viorel Lupu).
Version in 0.8.1
* Validated XHTML (Wolfgang Borgert).
* Added description of test classes and test cases.
Version in 0.8.0
* Define Template_mixin class for customization.
* Workaround a IE 6 bug that it does not treat <script> block as CDATA.
Version in 0.7.1
* Back port to Python 2.3 (Frank Horowitz).
* Fix missing scroll bars in detail log (Podi).
"""

# TODO: color stderr
# TODO: simplify javascript using ,ore than 1 class in the class attribute?

import datetime
import io
import sys
import time
import unittest
from xml.sax import saxutils


# ------------------------------------------------------------------------
# The redirectors below are used to capture output during testing. Output
# sent to sys.stdout and sys.stderr are automatically captured. However
# in some cases sys.stdout is already cached before HTMLTestRunner is
# invoked (e.g. calling logging.basicConfig). In order to capture those
# output, use the redirectors for the cached stream.
#
# e.g.
#   >>> logging.basicConfig(stream=HTMLTestRunner.stdout_redirector)
#   >>>

class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


# ----------------------------------------------------------------------
# Template

class Template_mixin(object):
    """
    Define a HTML template for report customerization and generation.
    Overall structure of an HTML report
    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    STATUS = {
        0: 'pass',
        1: 'fail',
        2: 'error',
    }

    DEFAULT_TITLE = 'Unit Test Report'
    DEFAULT_DESCRIPTION = ''

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    %(stylesheet)s
</head>
<body style="background-color:#C0C0C0" >
<script language="javascript" type="text/javascript"><!--
output_list = Array();
/* level - 0:Summary; 1:Pass; 2:Fail; 3:Error; 4:All */
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;
        if (id.substr(0,2) == 'Ft') {
            if (level == 2) {
                tr.className = '';
            }
            else if(level == 4) {
                tr.className = '';
            }
            else if(level == 5) {
                tr.className = '';
            }
            else{
                tr.className = 'hiddenRow';
            }
        }
        if (id.substr(0,2) == 'Pt') {
            if (level == 1) {
                tr.className = '';
            }
            else if(level == 4 ) {
                tr.className = '';
            }
            else{
                tr.className = 'hiddenRow';
            }
        }
        if (id.substr(0,2) == 'Et') {
            if (level == 3) {
                tr.className = '';
            }
            else if(level == 4 ) {
                tr.className = '';
            }
            else if(level == 5 ) {
                tr.className = '';
            }
            else{
                tr.className = 'hiddenRow';
            }
        }
    }
}
function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        tid0 = 't' + cid.substr(1) + '.' + (i+1);
        tid = 'F' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'P' + tid0;
            tr = document.getElementById(tid);
            if(!tr){
                tid = 'E' + tid0;
                tr = document.getElementById(tid);
            }
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        if (toHide) {
            document.getElementById('div_'+tid).style.display = 'none'
            document.getElementById(tid).className = 'hiddenRow';
        }
        else {
            document.getElementById(tid).className = '';
        }
    }
}
function showTestDetail(div_id){
    var details_div = document.getElementById(div_id)
    var displayState = details_div.style.display
    // alert(displayState)
    if (displayState != 'block' ) {
        displayState = 'block'
        details_div.style.display = 'block'
    }
    else {
        details_div.style.display = 'none'
    }
}
function html_escape(s) {
    s = s.replace(/&/g,'&');
    s = s.replace(/</g,'<');
    s = s.replace(/>/g,'>');
    return s;
}
/* obsoleted by detail in <div>
function showOutput(id, name) {
    var w = window.open("", //url
                    name,
                    "resizable,scrollbars,status,width=800,height=450");
    d = w.document;
    d.write("<pre>");
    d.write(html_escape(output_list[id]));
    d.write("\n");
    d.write("<a href='javascript:window.close()'>close</a>\n");
    d.write("</pre>\n");
    d.close();
}
*/
--></script>
%(heading)s
%(report)s
%(ending)s
%(chart)s
</body>
</html>
<script type="text/javascript"> 
function drawCircle(pass, fail, error){ 
    var color = ["#6c6","#c60","#c00"];  
    var data = [pass,fail,error]; 
    var canvas = document.getElementById("circle");  
    var ctx = canvas.getContext("2d");  
    var startPoint=0;  
    for(var i=0;i<data.length;i++){  
        ctx.fillStyle = color[i];  
        ctx.beginPath();  
        ctx.moveTo(112,84);   
        ctx.arc(112,84,84,startPoint,startPoint+Math.PI*2*(data[i]/(data[0]+data[1]+data[2])),false);  
        ctx.fill();  
        startPoint += Math.PI*2*(data[i]/(data[0]+data[1]+data[2]));  
    }  
}
function FillRect(cxt, x1, y1, width, height, color) {
    cxt.fillStyle = color; 
    cxt.fillRect(x1, y1, width, height);
} 
function drawBar(pass, fail, error){ 
    var color = ["#6c6","#c60","#c00"];  
    var data = [pass,fail,error];
    var count = pass + fail + error;
    var h =[10+(1 - pass/count)*148,10+(1 - fail/count)*148,10+(1 - error/count)*148];
    var x = [30,90,150];
    var y = [70,130,190];
    var canvas = document.getElementById("bar");  
    var ctx = canvas.getContext("2d");
    DrawString(ctx, 'Count(c)', '', '', '', '', 15, 10)
    DrawLine(ctx,5,15,10,10,'black');
    DrawLine(ctx,15,15,10,10,'black');
    DrawLine(ctx,10,10,10,158,'black');
    DrawLine(ctx,10,158,215,158,'black');
    DrawLine(ctx,210,153,215,158,'black');
    DrawLine(ctx,210,163,215,158,'black');
    DrawString(ctx, 'Type(c)', '', '', '', '', 180, 160)
    for(var i=0;i<3;i++) {
        DrawLine(ctx,x[i],h[i],x[i],158,color[i]);
        DrawLine(ctx,x[i],h[i],y[i],h[i],color[i]);
        DrawLine(ctx,y[i],h[i],y[i],158,color[i]); 
        DrawLine(ctx,(y[i]+x[i])/2,153,(y[i]+x[i])/2,158,color[i]);
        DrawString(ctx, data[i], '', color[i], '', '', (y[i]+x[i])/2, h[i]-15);
        FillRect(ctx, x[i], h[i], 40, 158-h[i], color[i]);
    }
} 
function DrawP(ctx, P) {
    with (ctx) {
        moveTo(P[0],P[1]);
        lineTo(P[0]+1,P[1]+1);
     }
}
function DrawLine(cxt, x1, y1, x2, y2, color) {
    cxt.strokeStyle = color;
    cxt.beginPath();
    cxt.moveTo(x1, y1);
    cxt.lineTo(x2, y2);
    cxt.stroke();
}
function DrawString(cxt, text, font, color, align, v_align, x, y) {
    if (font == "") {
        cxt.font = "10px";
    }
    else {
        cxt.font = font;
    }
    if (color == "") {
        cxt.fillStyle = "#000000";
    }
    else {
        cxt.fillStyle = color;
    }
    if (align == "") {
        cxt.textAlign = "left";
    }
    else {
        cxt.textAlign = align;
    }
    if (v_align == "") {
        cxt.textBaseline = "top";
    }
    else {
        cxt.textBaseline = v_align;
    }
    cxt.fillText(text, x, y);
}
function drawline(pass, fail, error){ 
    var color = ["#6c6","#c60","#c00"];  
    var data = [pass,fail,error];
    var count = pass + fail + error;
    var x = [30,90,150];
    var y = [70,130,190];
    var h =[10+(1 - pass/count)*148,10+(1 - fail/count)*148,10+(1 - error/count)*148];
    var canvas = document.getElementById("line");  
    var ctx = canvas.getContext("2d");
    DrawString(ctx, 'Count(c)', '', '', '', '', 15, 10)
    DrawLine(ctx,5,15,10,10,'black');
    DrawLine(ctx,15,15,10,10,'black');
    DrawLine(ctx,10,10,10,158,'black');
    DrawLine(ctx,10,158,215,158,'black');
    DrawLine(ctx,210,153,215,158,'black');
    DrawLine(ctx,210,163,215,158,'black');
    DrawString(ctx, 'Type(c)', '', '', '', '', 180, 160)
    for(var i=0;i<3;i++) {
        p = Array((y[i]+x[i])/2,h[i]);
        DrawP(ctx,p);
        DrawLine(ctx,(y[i]+x[i])/2,153,(y[i]+x[i])/2,158,color[i]);
        DrawString(ctx, data[i], '', color[i], '', '', (y[i]+x[i])/2, h[i]-15);
        if(i < 2) {

            DrawLine(ctx,(y[i]+x[i])/2,h[i],(y[i+1]+x[i+1])/2,h[i+1],'black');

        }

    }

} 
</script>  
"""
    # variables: (title, generator, stylesheet, heading, report, ending)

    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">

    STYLESHEET_TMPL = """
<style type="text/css" media="screen">
body        { font-family: verdana, arial, helvetica, sans-serif; font-size: 80%; }
table       { font-size: 100%; }
pre         { }
/* -- heading ---------------------------------------------------------------------- */
h1 {
    font-size: 16pt;
    color: gray;
}
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}
.heading .attribute {
    margin-top: 1ex;
    margin-bottom: 0;
}
.button{  
    border:1px solid #cccccc;  
    cursor:pointer;  
    margin:10px 5px;  
    height:40px;  
    text-align:center;  
    border-radius: 4px;  
    border-color: #636263 #464647 #A1A3A5;  
    text-shadow: 0 1px 1px #F6F6F6;  
    background-image: -moz-linear-gradient(center top, #D9D9D9, #A6A6A6 49%, #A6A6A6 50%);  
    background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0, #D9D9D9),color-stop(1, #A6A6A6));  
}  
.buttonText{  
    position:relative;  
    font-weight:bold;  
    top:10px;
    color:#58595B;  
}   
.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}
.panel .description{  
    border:1px solid #CCCCCC;  
    border-color: #636263 #464647 #A1A3A5;  
    margin:10px 5px;  
    height:165px;  
    border-radius: 4px;  
}  
.scroll-item {  
    position: relative;  
    width: 100%;  
    height: 32px;  
    border-bottom:1px solid gray;  
    cursor: pointer;  
}  
.item-even {  
    background-color: #E7E8EC;  
}  

.item-odd {  
    background-color: #E0ECF6;  
}  
.rect {  
    float: left;  
    margin-top: 5px;  
    margin-left: 5px;  
    width: 20px;  
    height: 20px;  
    border-radius: 3px;  
}  
.item-text{  
    margin-left: 5px;  
    height: 100%;  
    float: left;  
    font-size: 14px;   
    vertical-align: middle;  
    display: inline-block;  
    line-height: 30px;  
}  
.bg{  
    position:absolute;  
    height:97%;  
    width:80%;  
    overflow-x: hidden;  
    overflow-y:hidden;  
}  
.panel{  
    position:absolute;  
    height:550px;  
    width:750px;  
    left:45px;  
    top:45px;  
    border-radius: 12px;  
    background-image: -moz-linear-gradient(top,#EBEBEB, #BFBFBF);  
    background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0, #EBEBEB),color-stop(1, #BFBFBF));  
    }  
.panel1{  
    position:absolute;  
    height:550px;  
    width:200px;  
    left:800px;  
    top:45px;  
    border-radius: 12px;  
    background-image: -moz-linear-gradient(top,#EBEBEB, #BFBFBF);  
    background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0, #EBEBEB),color-stop(1, #BFBFBF));  
    } 
.panelBg{  
    position:absolute;  
    height:600px;  
    width:1000px;  
    left:20px;  
    top:20px;  
    border-radius: 12px;  
    background-color:#000000;  
    opacity:0.5;  
}  
.title{  
    border:1px solid green;  
    position:relative;  
    margin:5px;  
    font-size:22px;  
    font-weight:bold;  
    text-align:center;  
    color:#58595B;  
} 
.piechart{  
    border:1px solid green;  
    margin:5px;  
    height:170px;  
} 
.barchart{  
    border:1px solid green;  
    margin:5px;  
    height:170px;  
}  
.linechart{  
    border:1px solid green;  
    margin:5px;  
    height:170px;  
} 

.subTitle{  
    border:1px solid green;  
    margin:5px;   
    font-size:14px;  
    height:70px;  
    font-weight:bold;  
    text-indent:2em;  
    color:#6D6E71;  
}  
/* -- css div popup ------------------------------------------------------------------------ */
a.popup_link {
}
a.popup_link:hover {
    color: red;
}
.popup_window {
    display: none;
    position: relative;
    left: 0px;
    top: 0px;
    /*border: solid #627173 1px; */
    padding: 10px;
    background-color: #E6E6D6;
    font-family: "Lucida Console", "Courier New", Courier, monospace;
    text-align: left;
    font-size: 8pt;
    width: 500px;
}
}
/* -- report ------------------------------------------------------------------------ */
#show_detail_line {
    margin-top: 3ex;
    margin-bottom: 1ex;
}
#result_table {
    width: 80%;
    border-collapse: collapse;
    border: 1px solid #777;
}
#header_row {
    font-weight: bold;
    color: white;
    background-color: #777;
}
#result_table td {
    border: 2px solid #777;
    padding: 3px;
}
#total_row  { font-weight: bold; }
.passClass  { background-color: #6c6; }
.failClass  { background-color: #c60; }
.errorClass { background-color: #c00; }
.passCase   { color: #6c6; font-weight: bold;}
.failCase   { color: #c60; font-weight: bold; }
.errorCase  { color: #c00; font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }
#section1{  
    border:1px solid green;  
    position:relative;  
    float:left;  
    width:235px;  
    height:530px;  
    top:10px;  
    left:10px;  
}  
#section2{  
    border:1px solid green;  
    position:relative;  
    float:left;  
    width:235px;  
    height:530px;  
    top:10px;  
    left:20px;  
}  
#section3{  
    border:1px solid green;  
    position:relative;  
    float:left;  
    width:235px;  
    height:530px;  
    top:10px;  
    left:30px;  
}  
#section4{  
    border:1px solid green;  
    position:relative;  
    float:left;  
    width:180px;  
    height:530px;  
    top:10px;  
    left:10px;  
}  
/* -- ending ---------------------------------------------------------------------- */
#ending {
}
</style>
"""

    # ------------------------------------------------------------------------
    # Heading
    #

    HEADING_TMPL = """<div class='heading'>
<h1>%(title)s</h1>
%(parameters)s
<p class='description'>%(description)s</p>
</div>
"""  # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s:</strong> %(value)s</p>
"""  # variables: (name, value)

    # ------------------------------------------------------------------------
    # Report
    #

    REPORT_TMPL = """
<p id='show_detail_line'>Show
<a href='javascript:showCase(1)'>通过</a>
<a href='javascript:showCase(2)'>失败</a>
<a href='javascript:showCase(3)'>错误</a>
<a class="btn btn-primary" href='javascript:showCase(0)'>通过率 [%(passrate)s ]</a>
<a href='javascript:showCase(4)'>总数</a>
</p>
<table id='result_table'>
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row'>
    <td>Test Group/Test case</td>
    <td>Count</td>
    <td>Pass</td>
    <td>Fail</td>
    <td>Error</td>
    <td>CaseInfo</td>
</tr>
%(test_list)s
<tr id='total_row'>
    <td>执行情况</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>%(error)s</td>
    <td>通过率：%(passrate)s</td>

</tr>
</table>
"""  # variables: (test_list, count, Pass, fail, error)

    REPORT_CLASS_TMPL = r"""
<tr class='%(style)s'>
    <td>%(desc)s</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>%(error)s</td>
    <td><a href="javascript:showClassDetail('%(cid)s',%(count)s)">Detail</a></td>
</tr>
"""  # variables: (style, desc, count, Pass, fail, error, cid)

    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='4' align='center'>
    <!--css div popup start-->
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_%(tid)s')" >
        %(status)s</a>
    <div id='div_%(tid)s' class="popup_window">
        <div style='text-align: right; color:red;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_%(tid)s').style.display = 'none' " >
           [x]</a>
        </div>
        <pre>
        %(script_out)s
        </pre>
    </div>
    <!--css div popup end-->
    </td>
    <td colspan='1' align='center'>%(script_info)s</td>
</tr>
"""  # variables: (tid, Class, style, desc, status)

    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='4' align='center'>%(status)s</td>
    <td colspan='1' align='center'>%(script_info)s</td>
</tr>
"""  # variables: (tid, Class, style, desc, status)

    REPORT_TEST_OUTPUT_TMPL = r"""
%(id)s: %(output)s
"""  # variables: (id, output)

    CASEINFO_OUTPUT_TMPL = r"""
%(caseinfo)s
"""  # variables: (caseinfo)

    # ------------------------------------------------------------------------
    # ENDING
    #

    ENDING_TMPL = """<div id='ending'> </div>"""
    CHART_TMPL = """<div class="bg">
                       <div class="panelBg"></div>  
                       <div class="panel"> 
                       <div id="section1"> 
                           <div class="title">Pie Chart</div>  
                           <div class="subTitle">This chart is to show the rate that statis of test cases</div> 
                           <div class="piechart">   
                               <canvas id="circle" width="225" height="168" onmousemove='javascript:drawCircle(%(Pass)s, %(fail)s, %(error)s)'>your browser does not support the canvas tag</canvas>
                           </div> 
                           <div class="description">  
                           <div class="scroll-item item-even">  
                               <div class="rect" style="background-color: #6c6; "></div>  
                               <div class="item-text">Passcase:%(Pass)s</div>  
                           </div>  
                           <div class="scroll-item item-odd">  
                               <div class="rect" style="background-color: #c60; "></div>  
                               <div class="item-text">failcase:%(fail)s</div>  
                           </div>   
                           <div class="scroll-item item-even">  
                               <div class="rect" style="background-color: #c00; "></div>  
                               <div class="item-text">errorcase:%(error)s</div>  
                           </div> 
                           <div class="scroll-item item-odd">  
                           </div> 
                           <div class="scroll-item item-even">    
                           </div> 
                       </div> 
                       </div>  
                       <div id="section2">  
                       <div class="title">Bar Chart</div>  
                           <div class="subTitle">This chart is to show the count that statis of test cases</div> 
                           <div class="barchart">   
                               <canvas id="bar" width="225" height="168" onclick='javascript:drawBar(%(Pass)s, %(fail)s, %(error)s)'>your browser does not support the canvas tag</canvas>
                           </div> 
                           <div class="description">  
                           <div class="scroll-item item-even">  
                               <div class="rect" style="background-color: #6c6; "></div>  
                               <div class="item-text">Passcase:%(Pass)s</div>  
                           </div>  
                           <div class="scroll-item item-odd">  
                               <div class="rect" style="background-color: #c60; "></div>  
                               <div class="item-text">failcase:%(fail)s</div>  
                           </div>   
                           <div class="scroll-item item-even">  
                               <div class="rect" style="background-color: #c00; "></div>  
                               <div class="item-text">errorcase:%(error)s</div>  
                           </div> 
                           <div class="scroll-item item-odd">  
                           </div> 
                           <div class="scroll-item item-even">    
                           </div> 
                       </div> 
                       </div>  
                       <div id="section3"> 
                        <div class="title">Line Chart</div>  
                           <div class="subTitle">This chart is to show the rate that data of test cases</div> 
                           <div class="linechart">   
                               <canvas id="line" width="225" height="168" onclick='javascript:drawline(%(Pass)s, %(fail)s, %(error)s)'>your browser does not support the canvas tag</canvas>
                           </div> 
                           <div class="description">  
                           <div class="scroll-item item-even">  
                               <div class="rect" style="background-color: #6c6; "></div>  
                               <div class="item-text">Passcase:%(Pass)s</div>  
                           </div>  
                           <div class="scroll-item item-odd">  
                               <div class="rect" style="background-color: #c60; "></div>  
                               <div class="item-text">failcase:%(fail)s</div>  
                           </div>   
                           <div class="scroll-item item-even">  
                               <div class="rect" style="background-color: #c00; "></div>  
                               <div class="item-text">errorcase:%(error)s</div>  
                           </div> 
                           <div class="scroll-item item-odd">  
                           </div> 
                           <div class="scroll-item item-even">    
                           </div> 
                       </div> 
                       </div>
                       </div>
                       <div class="panel1">
                       <div id="section4">
                           <a>%(Pass)s 通过用例, %(fail)s 失败用例, %(error)s 错误用例.</a>
                       </div>
                       </div>
                    </div>"""


# -------------------- The end of the Template class -------------------


TestResult = unittest.TestResult


class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, verbosity=1):
        TestResult.__init__(self)
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []
        # 增加一个测试通过率 --Findyou
        self.passrate = float(0)

    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        self.outputBuffer = io.StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()

    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')


class HTMLTestRunner(Template_mixin):
    """
    """

    def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None):
        self.stream = stream
        self.verbosity = verbosity
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description

        self.startTime = datetime.datetime.now()

    def run(self, test, caseinfo={}):
        "Run the given test case or test suite."
        result = _TestResult(self.verbosity)
        test(result)
        self.stopTime = datetime.datetime.now()
        self.generateReport(test, result, caseinfo)
        print(sys.stderr, '\nTime Elapsed: %s' % (self.stopTime - self.startTime))
        return result

    def sortResult(self, result_list):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        classes = []
        for n, t, o, e in result_list:
            cls = t.__class__
            if not cls in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, o, e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def getReportAttributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        status = []
        status.append('总数 %s' % (result.success_count + result.failure_count + result.error_count))
        if result.success_count: status.append('通过 %s' % result.success_count)
        if result.failure_count: status.append('失败 %s' % result.failure_count)
        if result.error_count:   status.append('错误 %s' % result.error_count)
        if status:
            status = '，'.join(status)
            self.passrate = str("%.2f%%" % (float(result.success_count) / float(
                result.success_count + result.failure_count + result.error_count) * 100))
        else:
            status = 'none'
        return [
            ('测试人员', 'XXX'),
            ('开始时间', startTime),
            ('合计耗时', duration),
            ('测试结果', status + "，通过率= " + self.passrate),
        ]

    def generateReport(self, test, result, caseinfo):
        report_attrs = self.getReportAttributes(result)
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result, caseinfo)
        ending = self._generate_ending()
        chart = self._generate_chart(result)
        output = self.HTML_TMPL % dict(
            title=saxutils.escape(self.title),
            generator=generator,
            stylesheet=stylesheet,
            heading=heading,
            report=report,
            ending=ending,
            chart=chart,
        )
        self.stream.write(output.encode('utf-8'))

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                name=saxutils.escape(name),
                value=saxutils.escape(value),
            )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title=saxutils.escape(self.title),
            parameters=''.join(a_lines),
            description=saxutils.escape(self.description),
        )
        return heading

    def _generate_report(self, result, caseinfo):
        rows = []
        sortedResult = self.sortResult(result.result)
        for cid, (cls, cls_results) in enumerate(sortedResult):
            # subtotal for a class
            np = nf = ne = 0
            for n, t, o, e in cls_results:
                if n == 0:
                    np += 1
                elif n == 1:
                    nf += 1
                elif n == 2:
                    ne += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name
            row = self.REPORT_CLASS_TMPL % dict(
                style=ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass',
                desc=desc,
                count=np + nf + ne,
                Pass=np,
                fail=nf,
                error=ne,
                cid='c%s' % (cid + 1),
            )
            rows.append(row)

            for tid, (n, t, o, e) in enumerate(cls_results):
                self._generate_report_test(rows, cid, tid, n, t, o, e, caseinfo)

        report = self.REPORT_TMPL % dict(
            test_list=''.join(rows),
            count=str(result.success_count + result.failure_count + result.error_count),
            Pass=str(result.success_count),
            fail=str(result.failure_count),
            error=str(result.error_count),
            passrate=self.passrate,
        )
        return report

    def _generate_report_test(self, rows, cid, tid, n, t, o, e, caseinfo):
        # e.g. 'Pt1.1', 'Ft1.1','E1.1,' etc
        has_output = bool(o or e)
        if n == 0:
            tid = 'Pt%s.%s' % (cid + 1, tid + 1)
        elif n == 1:
            tid = 'Ft%s.%s' % (cid + 1, tid + 1)
        else:
            tid = 'Et%s.%s' % (cid + 1, tid + 1)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name
        tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL

        # o and e should be byte string because they are collected from stdout and stderr?
        if isinstance(o, bytes):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # uo = unicode(o.encode('string_escape'))
            uo = e
        else:
            uo = o

        if isinstance(e, bytes):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # ue = unicode(e.encode('string_escape'))
            # ue = e.decode('latin-1')
            ue = e
        else:
            ue = e

        script_out = self.REPORT_TEST_OUTPUT_TMPL % dict(
            id=tid,
            output=saxutils.escape(str(uo) + str(ue)),
        )

        script_info = self.CASEINFO_OUTPUT_TMPL % dict(
            caseinfo=caseinfo.get(desc, 'No Case Detail'),
        )

        row = tmpl % dict(
            tid=tid,
            Class=(n == 0 and 'hiddenRow' or 'none'),
            style=(n == 2 and 'errorCase') or (n == 1 and 'failCase') or (n == 0 and 'passCase'),
            desc=desc,
            script_out=script_out,
            script_info=script_info,
            status=self.STATUS[n],
        )
        rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TMPL

    def _generate_chart(self, result):

        sortedResult = self.sortResult(result.result)
        report = self.CHART_TMPL % dict(
            Pass=str(result.success_count),
            fail=str(result.failure_count),
            error=str(result.error_count),
        )
        return report


##############################################################################
# Facilities for running tests from the command line
##############################################################################

# Note: Reuse unittest.TestProgram to launch test. In the future we may
# build our own launcher to support more specific command line
# parameters like test title, CSS, etc.
class TestProgram(unittest.TestProgram):
    """
    A variation of the unittest.TestProgram. Please refer to the base
    class for command line parameters.
    """

    def runTests(self):
        # Pick HTMLTestRunner as the default test runner.
        # base class's testRunner parameter is not useful because it means
        # we have to instantiate HTMLTestRunner before we know self.verbosity.
        if self.testRunner is None:
            self.testRunner = HTMLTestRunner(verbosity=self.verbosity)
        unittest.TestProgram.runTests(self)


main = TestProgram

##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":
    main(module=None)

