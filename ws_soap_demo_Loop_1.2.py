#!/usr/bin/env python
#coding=utf-8

import os, shutil
import httplib
import xlrd
import xlwt
import time
import globalValue
import re
import chardet
import ssl

def msg_split(msgs, tagname_s, tagname_e):
    if len(msgs)>0:
        results = re.findall(tagname_s, msgs, re.M | re.I)
        if len(results)>0:
            msg = msgs.split(tagname_s)[-1].split(tagname_e)[0]
        else:
            msg = ""      
    else:
        msg = msgs
    return msg

def getSoapMessages(strSoapDataFile):
    # read xml file   
    if not os.path.isfile(strSoapDataFile) :
        return -1,"Argument Error, SoapData: <%s> invalid." % strSoapDataFile
    try:
        f = open(strSoapDataFile,'r')
    except IOError,e:
        return -1,"Fail to open the file: <%s>." % strSoapDataFile
    lines = f.readlines()
    f.close()
    SoapMessage = '''\n''' + ''.join(lines)
    return SoapMessage

def checkStatus_response(response):
    try:
        if response.status == 200:
            content = [response.reason,response.read()]
        else:
            errmsg = msg_split(response.read(),"<faultstring>","</faultstring>")
            content = ["Fail",errmsg]
    except Exception,e:
        errno, errmsg = e
        content = ["Block",errmsg]
    return content    

def sendSoapMsgByHTTPSConnection(strWsdl,strSoapAction,strSoapMsg): 
    # send soap request
    pos = strWsdl.find('/',8)
    # length for wsdl http=7; https=8
    if strWsdl[0:5].lower()=='http:'.lower():
        s_idx_Host = 7
    elif strWsdl[0:5].lower()=='https'.lower():
        s_idx_Host = 8
    strHost = strWsdl[s_idx_Host:pos]
    strPostval = strWsdl[pos:len(strWsdl) - 5]
    try:
        if s_idx_Host ==7:            
            webservice = httplib.HTTPConnection(strHost,timeout = 90)
        elif s_idx_Host ==8:
            webservice = httplib.HTTPSConnection(strHost,timeout = 90)
        webservice.set_debuglevel(0)
        webservice.putrequest("POST", strPostval)
        webservice.putheader("Host", strHost)
        webservice.putheader("User-Agent", "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)")
        webservice.putheader("Content-type", "application/xml; charset=\"utf-8\"")
        webservice.putheader("Content-length", "%d" % len(strSoapMsg))
        webservice.putheader("SOAPAction", "%s" %(strSoapAction))
        webservice.endheaders()    
        webservice.send(strSoapMsg)
        response = webservice.getresponse() 
        res = checkStatus_response(response) # return [OK/Fail/Block, Description]
        print res[0]
    except ssl.SSLError,e:
        errno=e.errno
        errmsg = e.message
        print "Error No: ",errno, "Err Msg:",errmsg     
        res = ['Block',errmsg]
    except Exception,e:
        print "Non-SSLError: ",e
        res = ['Block',e]
    webservice.close()
    return res # return [OK/Fail/Block, Description]

def getTargetSheet(filename, strSheetName='Configuration'):
    xls = xlrd.open_workbook(xls_f)
    if len(strSheetName)==0:
        sht = xls.sheet_by_name(strSheetName)
    else:    
        sht_nms = xls.sheet_names()
        for nm in sht_nms:
            if nm == strSheetName:
                sht = xls.sheet_by_name(nm)
                break
    return sht

def getCompareResult_ChangeLogic(responseContent, exp_res):
    results = re.findall(exp_res, responseContent, re.M | re.I)
    # print results
    if len(results) ==0:
        code = msg_split(responseContent,"<code>","</code>")
        desc = msg_split(responseContent,"<description>","</description>")
        msg = msg_split(responseContent,"<Message>","</Message>")
        if len(desc)>0:
            err = desc
        elif len(msg)>0:
            err = msg
        elif len(code)>0:
            err = code
        else:
            err = responseContent    
        validation = ["Fail",err]
    else:
        validation = "Pass"
        
    return validation

def getXMLFile(xmlfolder, strWSname):
    xml_list = os.listdir(xmlfolder)
    for xml in xml_list:
        target_xml = os.path.join(xmlfolder,xml)
        if os.path.isfile(target_xml) and os.path.splitext(xml)[0]==strWSname:  # check if xml file in xml folder or not.
            return target_xml
            break
    return -1 # not found the particular xml file in xmlfolder

def styleTargetFile():
    font=xlwt.Font()
    font.name = 'Arial'
    font.height  = 240
    font.bold= True
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 5
    alignment = xlwt.Alignment() # Create Alignment
    alignment.horz = xlwt.Alignment.HORZ_LEFT
    style = xlwt.XFStyle()
    style.pattern = pattern
    style.font = font
    style.alignment = alignment
    return style

def initTargetResultFile(targetresultfolder,strSheetName):
    # Create New excel file to save the check result
    xls_result = xlwt.Workbook()
    sht_result = xls_result.add_sheet(strSheetName,cell_overwrite_ok=True)
    # Apply style
    style = styleTargetFile()
    # Add Title in new excel file
    titles = [u'WebServiceName',u'WSDL','SOAPAction',u'CheckPoint',u'Duration(s)',u'Result',u'Comments']
    for j in range(0,len(titles)):   # Fill in the final title in excel
        sht_result.write(0,j,titles[j],style)
        sht_result.col(j).width = 7000
    targetresultfile = os.path.join(targetresultfolder,strSheetName+"_CheckResult.xls")
    xls_result.save(targetresultfile)
    # return excel, sheet, filename
    return [xls_result,sht_result, targetresultfile]

def initXMLFiles(srcFolder, targetFolder):
    xml_list = os.listdir(srcFolder)
    if len(xml_list)>0:
        for xml in xml_list:
            target_xml = os.path.join(srcFolder,xml)
            shutil.move(target_xml,targetFolder)
    print "Test XML Files have been ready for checking." 

if __name__ == "__main__":
    # Config info: Read wsdl list from excel file.
    ssl._create_default_https_context = ssl._create_unverified_context
    ws_root_fd = globalValue.WS_main_dir
    xls_f = os.path.join(ws_root_fd,"WSDL_List.xls")
    result_folder = ws_root_fd
    xml_f = os.path.join(ws_root_fd,"xml_ready/")
    xml_f_rd = os.path.join(ws_root_fd,"xml_used/")
    # Check what environments will be tested in configuration sheet in WSDL_List.xls.
    rd_conf_Sht = getTargetSheet(xls_f)
    conf_rows = rd_conf_Sht.nrows
    for i in range(1,conf_rows):
        # Get the sheetname in WSDL_List.xls need to do regression testing. 
        if rd_conf_Sht.cell_value(i,0) =='Y':
            # Reset the test xml files from readed folder <xml_rd> to initial folder <xml>.
            initXMLFiles(xml_f_rd,xml_f)
            sht_nm = rd_conf_Sht.cell_value(i,1)
            # Point target Sheet in excel file
            rd_Sht = getTargetSheet(xls_f,sht_nm)
            print "ToBeTested Sheet Name is: %s."%(rd_Sht.name)
            nrows = rd_Sht.nrows
            # idxs = [ToBeTested,WebServiceName,WSDL,SOAPAction,CheckPoint]
            idxs = [1,2,3,4,6] 
            row_start = 1
            # Initial Regression CheckResult excel file.
            wt_xls = initTargetResultFile(result_folder,sht_nm)
            rowid = 0
            # iterate all wsdl linkages when TOBETESTED = Y
            for i in range(nrows-1):  # Only for Demo, actual Range(nrows-1)
                i +=row_start
                print i
                if rd_Sht.cell_value(i,idxs[0]) =='Y':
                    print "Total Script Process is: %0.1f%%;\tCurrent ToBeTested Row is: %d."%(i*100/float(nrows-1),i+1)
                    ws_wsname = str(rd_Sht.cell_value(i,idxs[1]))
                    ws_wsdl = str(rd_Sht.cell_value(i,idxs[2])) + "?wsdl"
                    ws_soap = str(rd_Sht.cell_value(i,idxs[3]))
                    ws_exp_res = str(rd_Sht.cell_value(i,idxs[4]))
                    seconds = 0
                    res = [ws_wsname,ws_wsdl,ws_soap,ws_exp_res]
                    xmlfile = getXMLFile(xml_f, ws_wsname)  # Find target xml file 
                    if xmlfile != -1: 
                        ws_soapmsg = getSoapMessages(xmlfile)
                        stime = time.time()
                        response = sendSoapMsgByHTTPSConnection(ws_wsdl,ws_soap,ws_soapmsg) 
                        # return [OK/Fail/Block, Description]
                        if response[0] =="OK":
                            res_content = response[-1]
                            res_checked = getCompareResult_ChangeLogic(res_content,ws_exp_res)
                        else:
                            res_checked = response
                        etime = time.time()
                        seconds = etime - stime 
                        shutil.move(xmlfile,xml_f_rd) # Move the xml file to readed folder to improve performance
                    else:
                        res_checked = ["Not Start","Cannot find related XML file in related test data folder."]
                    # append handle duration(s) into resultset
                    res.append(seconds)
                    # append checkresutl into resultset
                    if type(res_checked) ==list:
                        for val in res_checked:
                            res.append(val)
                    else:
                        res.append(res_checked)
                    # Update the record to result file.        
                    rowid = rowid+1
                    for j in range(0,len(res)):
                        wt_xls[1].write(rowid,j,res[j])
                    wt_xls[0].save(wt_xls[2])

            wt_xls[0].save(wt_xls[2])
            print "Target Result File is: %s"%(wt_xls[2])
    print "Regression Test for WebService Part was completed!"
