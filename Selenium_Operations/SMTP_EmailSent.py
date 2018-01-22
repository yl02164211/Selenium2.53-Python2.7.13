#!/usr/bin/env python
#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart 

HOST = "smtp.163.com"
SUBJECT = u"官网流量数据报表"
TO = ';'.join(['liang.yan@hpe.com'])
FROM = "yanliang02164211@163.com"

msg=MIMEMultipart()
puretext = MIMEText("""
  <table width="800" border="0" cellspacing="0" cellpadding="4">
    <tr>
      <td bgcolor="#CECFAD" height="20" style="font-size:14px">*官网数据<a href="monitor.domain.com">更多</a></td>
    </tr>
    <td bgcolor="#EFEBDE" height="100" style="font-size:13px">
    1)日访问量:<font color=read>152433</font>访问次数:23651 页面浏览量:45123 点击数:545122 数据流量:504Mb<br>
    2)状态码消息<br>
      500:105 404;3264 503;214<br>
    3)访客浏览器信息<br>
      IE:50% firefox:10% chrome:30% other:10%<br>
    4)页面信息<br>
      /index.php 42153<br>
      /view.php 21451<br>
    </td>
    </tr>
  </table>""","html","utf-8")
msg.attach(puretext) 
msg['Subject'] = SUBJECT
msg['FROM'] = FROM
msg['To'] = TO
xlspart= MIMEApplication(open('C:/lagou.xlsx','rb').read())
xlspart.add_header('Content-Disposition', 'attachment', filename='C:/lagou.xlsx')
msg.attach(xlspart)   
try:
  server = smtplib.SMTP()
  server.connect(HOST)
  # server.ehlo()
  # server.starttls()
  server.login('yanliang02164211@163.com','yl02164211')
  server.sendmail(FROM,TO,msg.as_string())
  server.quit()
  print "邮件发送成功"
except Exception,e:
  print "失败:" + str(e)