import urllib.request, http.cookiejar, time, socket, sys
import emailsender

socket.setdefaulttimeout(5)

#cookie = http.cookiejar.CookieJar() 
#cookieProc = urllib.request.HTTPCookieProcessor(cookie) 
#opener = urllib.request.build_opener(cookieProc)
#urllib.request.install_opener(opener)

def GetUrlRequest(iUrl,iStrPostData): 
    postdata=urllib.parse.urlencode(iStrPostData) 
    postdata=postdata.encode(encoding='UTF8') 
    header = {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)','Server': 'Sun-Java-System-Web-Proxy-Server/4.0','Proxy-agent': 'SecProxy/1.0'} 
    req= urllib.request.Request( 
               url = iUrl, 
               data = postdata, 
               headers = header) 
    return urllib.request.urlopen(req).read()

def train_monitor(train_num, arriving_station, email, time_interval):
    arriving_station = urllib.request.quote(arriving_station)
    arriving_station = arriving_station.replace('%','-')
    url = "http://dynamic.12306.cn/map_zwdcx/cx.jsp?cz=%C1%C4%B3%C7&cc={}&cxlx=0&rq=2016-09-07&czEn={}&tp=1473227193741".format(train_num, arriving_station)
    raw_html = GetUrlRequest(url,"")
    mail_content = raw_html.decode('gb2312').strip()
    mail_ = emailsender.Mail(email,'列车到达时间估计',mail_content)
    #time.sleep(10)
    # print('列车晚点检测程序启动！')
    smooth = True
    while (time.strftime('%H:%M',time.localtime()) < mail_content[-5:]) or ((int(time.strftime('%H:%M',time.localtime())[:2]) - int(mail_content[-5:][:2])) > 5):
        try:
            raw_html = GetUrlRequest(url,"")
            # print('获取网页成功')
            mail_content = raw_html.decode('gb2312').strip()
            if '无' in mail_content:
                mail_.message = mail_content
                mail_.send()
                smooth = False
                break
            mail_.message =mail_content + '。检测时间：'+ time.strftime('%H:%M',time.localtime()) + ',下次检测将在' + time.strftime("%H:%M",time.localtime(time.time() + int(time_interval))) + '进行。'
            mail_.send()
            #print('发送成功')
            # print('检测时间：'+ time.strftime('%H:%M',time.localtime()) + '，下次检测将在' + time.strftime("%H:%M",time.localtime(time.time() + int(time_interval))) + '进行。')
            # print('--------------------------------------------------------------------------')
            time.sleep(int(time_interval))
        except:
            # print('获取失败！进入一分钟冷却。')
            # print('检测时间：'+ time.strftime('%H:%M',time.localtime()) + '，下次检测将在' + time.strftime("%H:%M",time.localtime(time.time() + 60)) + '进行。')
            # print('--------------------------------------------------------------------------')
            time.sleep(600)
            continue
    if smooth:
        mail_.subject = '列车已到站或无车票信息，晚点检测程序结束。'
        mail_.message = '查询结束'
        mail_.send()
	
if __name__=='__main__':
    train_monitor(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])