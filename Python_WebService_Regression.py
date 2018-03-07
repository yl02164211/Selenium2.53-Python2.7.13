# coding=utf-8
from suds.wsse import * # WebService Library API for Python
from suds.client import Client # WebService Library API for Python
import cx_Oracle # ODBC_Oracle API
import xlwt # Excel Write Library
import xlrd # Excel Read Library
import time

def get_WS_Method_Parms(client,methodname):
    method = client.wsdl.services[0].ports[0].methods[methodname]
    input_parms = method.binding.input
    input_parms_dts = input_parms.param_defs(method)
    parm_list =[]
    for input_parm_d in input_parms_dts:
        parm_list.append(input_parm_d[0])    
    return parm_list

def get_WS_Methods(client, wsdl):
    # get all available methods from wsdl
    method_list = []
    for method in client.wsdl.services[0].ports[0].methods:
        method_name = method
        method_parms = get_WS_Method_Parms(client,method_name) # Type = List
        per_method = [wsdl,method_name,method_parms]
        method_list.append(per_method)
    return method_list # Type = List; Format = [wsdl, method_name, [method_parms]]

def get_WS_Responses(client, ws_methods_detail, check_attribute, check_id):
    # ws_methods_detail format = [wsdl, method_name, [method_parms]] 
    for method in ws_methods_detail:
        method_wsdl, method_name,method_parms = method
        # print "%s\n%s\n%s" %(method_wsdl, method_name, method_parms)
        cmd = "%s(%s=%d)" %(method_name,check_attribute,check_id)
        print "valid command is: %s" %(cmd)
        response = client.service.method_name
        print type(response)

        # print response
        # if hasattr(response, "errors"):
        #     result = ["Error Desc: %s." %(response.errors[0].description)]
        # else:
        #     result = [response.messages[0].description]
        # print result


def get_wsdl_result(records, check_attribute='', check_id=0):
    # default wsdl index = 4  in records
    # print records[4]
    wsdl = records[4] + '?wsdl'
    ws_head_acct = records[1]
    ws_head_pwd = records[2]
    # print wsdl,ws_head_acct,ws_head_pwd 
    client = Client(wsdl)
    security = Security()
    token = UsernameToken(ws_head_acct,ws_head_pwd)
    token.setnonce()
    token.setcreated()
    security.tokens.append(token)
    client.set_options(wsse=security)
    req_WS_Detail = get_WS_Methods(client,wsdl)
    get_WS_Responses(client, req_WS_Detail, check_attribute, check_id)

    # response = client.service.manageRPLScreeningService(otherPartSiteInstanceID=opsi_id,siteName=siteName_i,coundtryCode=countryCode_i,addressLine1=addressLine1_i)
    #     if hasattr(response, "errors"):
    #         result = ['N/A',"Err_GtsDetail:%s & Err_Resubmit:%s." %(queryDesc, response.errors[0].description)]
    #     else:
    #         result = [response.rplStatus,response.messages[0].description]
    #     return result

def get_targetSheetID(sheets, keyword):
    index = 'N/A' # define the initial sheetid out of range.
    if len(sheets)>0:
        for i in range(len(sheets)):
            # print sheets[i].name
            if (keyword in sheets[i].name):
                # Read Records
                index = i
                # print "Active Sheet ID is: %d" %(index)
                break
    # print index
    return index

def get_columnid(sheet, fieldname):
    col_id = 'N/A'
    ncols = sheet.ncols
    row = 0 # In sheet, row_index is from 0
    for j in range(ncols):
        # Check target field name without consider case sensitive 
        if sheet.cell(row, j).value.lower() == fieldname.lower(): 
            col_id = j
            break
    return col_id

def testdata_iterates(test_file,test_env_company):
    xls = test_file
    workbook = xlrd.open_workbook(xls)
    sheets=workbook.sheets()
    # Find target sheetid
    targetSheetID = get_targetSheetID(sheets,test_env_company)
    if (targetSheetID == 'N/A'):
        print "Can not found particular Sheet %s in the %s.\nPlease Check the test data again." %(test_env_company, test_file)
        return '-1'
    else:
        activesheet = sheets[targetSheetID]
        nrows = activesheet.nrows # activesheet row count
        title_row = 0
        str_row = 1 # raw data rowid is from 1.
        # Find target necessary fields value
        idx_project = get_columnid(activesheet, 'projectname')
        idx_check = get_columnid(activesheet, 'tobetested')
        idx_wsname = get_columnid(activesheet, 'webservicename')
        idx_user = get_columnid(activesheet, 'username')
        idx_pwd =  get_columnid(activesheet, 'password')
        idx_wsdl = get_columnid(activesheet, 'wsdl')
        # idx_fields = [idx_project,idx_check,idx_wsname,idx_wsdl,idx_user,idx_pwd]
        # print idx_fields
        # iterator all wsdl records
        
        # Demo for only one record
        check_attribute = "OtherPartySiteInstanceId"
        check_id = 959702294
        i=0
        records=[i+str_row,activesheet.cell(i+str_row,idx_project).value,
                            activesheet.cell(i+str_row,idx_check).value,
                            activesheet.cell(i+str_row,idx_wsname).value,
                            activesheet.cell(i+str_row,idx_wsdl).value,
                            activesheet.cell(i+str_row,idx_user).value,
                            activesheet.cell(i+str_row,idx_pwd).value]
        response = get_wsdl_result(records, check_attribute, check_id)
        
        # for i in range(nrows):
        #     if i<(nrows-1):
        #         records=[   i+str_row,
        #                     activesheet.cell(i+str_row,idx_project).value,
        #                     activesheet.cell(i+str_row,idx_check).value,
        #                     activesheet.cell(i+str_row,idx_wsname).value,
        #                     activesheet.cell(i+str_row,idx_wsdl).value,
        #                     activesheet.cell(i+str_row,idx_user).value,
        #                     activesheet.cell(i+str_row,idx_pwd).value   ]
        #         print records
        #         # Start WebService Check
        #         response = get_wsdl_result(records)
        #         print response               

if __name__ == "__main__":
    testdata = "c:/tmp/Smoking_TestData.xls"
    testenv = "PRO_HPE"
    testdata_iterates(testdata, testenv)
