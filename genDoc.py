#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import urllib.request, asyncio ,aiohttp     
import time

#THE PROXY INFO
proxy_uri="server:port"
proxy_user = "user"
proxy_pwd = "pwd"


proxy_info=proxy_user+':'+proxy_pwd+'@'+proxy_uri
proxy_sever = 'http://'+proxy_uri
proxy_handler = urllib.request.ProxyHandler({'http':proxy_info})
urlopener = urllib.request.build_opener(proxy_handler)


def get_pages_info():
    
    print("get_pages_url... BEGIN")   
    
    #OPEN THE HOME PAGE OF LIAO'S PATHON TUTORIAL
    f = urlopener.open("http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000")
    home_page = f.read()
    f.close()
    
    #MAKE IT IN ONE LINE
    home_page=str(home_page)
    home_page = home_page.replace("\\n", "")
    home_url = home_page.replace(" ", "")
    
    #FETCH THE URL STRINGS 
    url_list = home_url.split(r'style="margin-left:')[1:122]
    #ADD THE FIRST PAGE
    url_list.insert(0, '1em;"><ahref="/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000">')
    
    level1_index=-1
    level2_index=-1
    
    page_info_list=[]
    for element in url_list:
        
        #GET THE LEVEL OF THE ARTICLE
        level=element[0]
        if level=='1':
            level1_index=level1_index+1 
            level2_index=0
        else:
            level2_index=level2_index+1
        
        page_url = element.split(r'em;"><ahref="')[1]
        page_url = page_url.split(r'">')[0]
        page_url = 'http://www.liaoxuefeng.com' + page_url   
        
        page_info={}
        page_info['level1']=level1_index
        page_info['level2']=level2_index
        page_info['url']=page_url
        
        page_info_list.append(page_info)
    print("get_pages_url... DONE")
    return page_info_list
    

@asyncio.coroutine
def write_doc(page_info):
    print("docs/" + "%02d.%d 正在处理" %(page_info['level1'],page_info['level2']) )
    #OPEN THE HOME PAGE OF LIAO'S PATHON TUTORIAL 
    '''
    opener = urllib.request.build_opener(proxy_handler)
    f = opener.open(page_info['url'])
    html = f.read()
    f.close()
    #DECODE CHINESE CODE
    html=html.decode('utf-8') 
    '''
    conn = aiohttp.ProxyConnector(proxy=proxy_sever,proxy_auth=aiohttp.BasicAuth(proxy_user, proxy_pwd))
    response = yield from aiohttp.get(page_info['url'], connector=conn)
    html = yield from response.text()
    
    #GET THE TITLE
    title = html.split("<h4>")[1].replace("/", " ")
    title = title.split("< h4>")[0]
    
    
    #GET THE CONTENT
    html = str(html).split(r'<div class="x-wiki-content">')[1]
    html = html.split(r'''
    </div>
    <hr>
    <div id="x-wiki-prev-next" class="uk-clearfix uk-margin-left uk-margin-right">
    </div>
    '''
    )[0]
    
    #TRANSFER THE PATH OF THE <SRC> DOCS
    html = html.replace(r'src="', 'src="' + 'http://www.liaoxuefeng.com')
    
    #COMPLETE THE HTML
    html = r''' <HTML><head>
    <link rel="stylesheet" href="css/codemirror.css">
    <link rel="stylesheet" href="css/highlight.css">
    <link rel="stylesheet" href="css/itranswarp.css">
    </HEAD>
    <BODY>''' +"<H4>"+title+"</H4>"+ html+"</body></html>"
    
    #WRITE FILES
    filename="docs/" + "%02d.%d " % (page_info['level1'],page_info['level2']) + title + '.html'
    
    output = open(filename, 'w')
    output.write(html)
    print("%s 处理完毕" % filename)
    output.close()
    


if __name__ == '__main__':
    start = time.clock()
    page_info_list=get_pages_info()
    loop=asyncio.get_event_loop()
    tasks = [write_doc(page_info) for page_info in page_info_list]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    end = time.clock()
    print ("cost: %f s" % (end - start))