# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import shutil
import os

'''
The sequence is 1st request the latest page , 2st seach all the link in the board and push then into the set , 
3st request the next page and return to 2st until you don't want ,
the final is going through the link in the set and go through them


'''

def RequestUrl(url):
    html=requests.get(url)
    return html.text
def DealBoardUrl(html,counter):
    '''
    The second step is deal with board url.
    '''
    UselessUrl=AnnouncUrl() #The first page always exist the announcement
    Board=CreateSet()
    tmp=CreateSet()
    #AllLink=CreateSet()
    
    for i in range(int(counter)):
        print (u'現在要處理第 %d 頁\n'%(i+1))
        bsObj=BeautifulSoup(html,'html.parser')
        ThemeLink=GetBoardThemeLink(bsObj,tmp)
        print
        if len(ThemeLink) !=0:
            tmp=ThemeLink.symmetric_difference(UselessUrl)
        
        if i <= int(counter):
            nexturl=GetNextPage(bsObj)
            print (nexturl)
            html=RequestUrl(nexturl)
            print(u'第 %d 頁已經處理完\n'%(i+1))
    DelSet(UselessUrl)
    DelSet(Board)
      
    return tmp
def DealPageUrl(text):
    res=CreateSet()
    bsObj=BeautifulSoup(text,'html.parser')
    for link in bsObj.find('div',{'id':'main-content'}).findAll('a'):
        res.add(link.attrs['href'])
    return res

def GetNextPage(bsObj):
    group=bsObj.find('div',{'class':'btn-group btn-group-paging'})
    Nextpage=group.select('a')[1].attrs['href']
    Url='https://www.ptt.cc'+Nextpage
    return Url

def GetBoardThemeLink(bsObj,Theme):
    #Get  Theme Links 
    for links in bsObj.findAll('div',{'class':'r-ent'}):
        
        try:
            link=links.find('div',{'class':'title'}).find('a').attrs['href']
            DataWord='http://www.ptt.cc'+link   
            Theme.add(DataWord)
           
        except:
            pass
    
        
    
    return Theme



def DelUselessData(res):
    #After Comparing the pattern,we get just imgur url 
    pattern = re.compile(r'http://i.imgur.com/')
    data=list()
    for i in res:
        if re.match(pattern,i):
            data.append(i)
        else:
            pass
        
    del res  
    return data
def GoThroughBoard(html,counter):
    BoardUrl=DealBoardUrl(html,counter)
    for i in BoardUrl:   
        text=RequestUrl(i)
        res=DealPageUrl(text)
        data=DelUselessData(res)
        GetPicture(data)
    print(u'所有的程序已完成')       
def GetPicture(res):
    print(u'現在開始下載照片\n')
    for i in res:
        print (i)
        filename=i.split('/')[-1]
        pic=requests.get(i,stream=True)
        fb=open(filename,'wb')
        shutil.copyfileobj(pic.raw,fb)
        fb.close()

def AnnouncUrl():
    #The function is used to avoid the Annocenment Url
    Useless=CreateSet()
    Useless.add('http://www.ptt.cc/bbs/Beauty/M.1443906121.A.65B.html') #[公告] 不願上表特 ＆ 優文推薦 ＆ 檢舉建議專區
    Useless.add('http://www.ptt.cc/bbs/Beauty/M.1423752558.A.849.html') #[公告] 表特板板規 (2015.2.12)
    Useless.add('http://www.ptt.cc/bbs/Beauty/M.1430099938.A.3B7.html') #[公告] 對於謾罵，希望大家將心比心
    Useless.add('http://www.ptt.cc/bbs/Beauty/M.1476111251.A.C20.html') #[公告] 偷拍相關板規修訂
    return Useless

#The page link will be pushed into the set
def CreateSet():
    Urls=set()
    return Urls
def DelSet(Aset):
    del Aset


def main():
    #Declare Beauty Board
    url='https://www.ptt.cc/bbs/Beauty/index.html'
    
    print(u'此程式是專門幫你抓表特版照片\n')
    print(u'不提供選擇按讚數,日期,指定主題\n\n')
    counter=input(u'需要處理幾頁表特版頁數 ? ')
  
    
    text=RequestUrl(url)
    GoThroughBoard(text,counter)
   
main()
