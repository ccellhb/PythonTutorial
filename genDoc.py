#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request        

#THE PROXY INFO
proxy='username:password@server:port'
#OPEN THE HOME PAGE OF LIAO'S PATHON TUTORIAL
proxy_handler = proxy_handler = urllib.request.ProxyHandler({'http':proxy})   

opener = urllib.request.build_opener(proxy_handler)
f = opener.open("http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000")
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
last_level_index=-1
#FETCH THE CONTENTS
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
     
    proxy_handler = proxy_handler = urllib.request.ProxyHandler({'http':proxy})   
    opener = urllib.request.build_opener(proxy_handler)
    f = opener.open(page_url)
    html = f.read()
    f.close()
    #DECODE CHINESE CODE
    html=html.decode('utf-8') 
    
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
    html = " <HTML><BODY>" +"<H4>"+title+"</H4>"+ html+"</body></html>"
    
    #WRITE FILES
    filename="docs/" + "%d.%d " % (level1_index,level2_index) + title + '.html'
    print("name:"+filename)
    output = open(filename, 'w')
    output.write(html)
    output.close()
    
