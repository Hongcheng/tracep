#! usr/bin/env python
#coding:utf-8
from mongoengine import *
# from django.db import models
# from django.http import HttpResponse
# from django.template.loader import get_template
# from django.template import Template,Context
import socket
import requests
import json
import datetime
from mongoengine import *
from bs4 import BeautifulSoup
connect('tracep')
UpdateThresh = 10
HistoryListLength = 5
amazonip = 'http://203.81.17.130'
# Create your models here.

# def PriceToInt(sPrice):


def GetThePrice(self):
    # if self.ProductID == None:
    #     return None,None
    # purl = amazonip+'/gp/twister/ajax/prefetch?parentAsin='+self.ProductID+'&asinList='+self.ProductID
    purl = ''.join([amazonip,'/gp/twister/ajax/prefetch?parentAsin=',self.ProductID,'&asinList=',self.ProductID])
    try:
        pr = requests.get(purl)
    except:
        return None,None
    '''
    If length < 100, it means that there is no such a product in this ID
    '''
    soup = BeautifulSoup(pr.text)
    body = soup.find('body')
    
    # print pr.text.encode('utf-8')
    if len(pr.text) < 100:
        return None,None
    pstart = pr.text.find(u'actualPriceValue')
    pstart = pr.text.find(u'<b class="priceLarge">￥',pstart+len('actualPriceValue'))
    pend = pr.text.find(u'</b>',pstart+len(r'<b class="priceLarge">￥ '))
    price = pr.text[pstart+len(u'<b class="priceLarge">￥ '):pend]
    price = price.replace(',','')
    try:
        price = float(price)
    except:
        print 'not float'
        return None,None

    nstart = pr.text.find(u'btAsinTitle')
    nstart = pr.text.find(u'<span style="padding-left: 0" >',nstart)
    nend1 = pr.text.find(u'<',nstart+len(r'<span style="padding-left: 0" >')+10)
    nend2 = pr.text.find(u'\\n\\',nstart+len(r'<span style="padding-left: 0" >')+10)
    if nend1 < nend2:
        nend = nend1
        # print 1
    else:
        nend = nend2
        # print 2
    name = pr.text[nstart+len(r'<span style="padding-left: 0" >')+4:nend]
    # print name.encode('utf-8')
    return price,name


class Amazon_class(Document):
    ProductID = StringField(max_length = 20)
    ProductName = StringField()
    DatePrice = ListField()

    # def __init__(self, pID):
    #     # ID = str(ID)
    #     self.ProductID = pID
    #     # print self.ProductID

    def UpdateAll(self):
        Amazon_Objects = Amazon_class.objects()
        now = datetime.datetime.now()
        UpdateRest = {}
        for obj in Amazon_Objects:
            self.ProductID = obj.ProductID
            if (now - obj.DatePrice[-1]['Date']).seconds < UpdateThresh:
                UpdateRest[self.ProductID] = 'Time'
                continue
            price,name = GetThePrice(self)
            if price == None:
                UpdateRest[self.ProductID] = 'Web'
                continue
            TodayPrice = {'Date':now, 'Price':price}
            self = obj
            self.DatePrice.append(TodayPrice)
            if len(self.DatePrice) > HistoryListLength:
                self.DatePrice = self.DatePrice[-HistoryListLength:]
            self.save()
            UpdateRest[self.ProductID] = 'Add'
        return UpdateRest

    def UpdateDatePrice(self):
        Amazon_Objects = Amazon_class.objects(ProductID = self.ProductID)
        now = datetime.datetime.now()
        print now
        print self.ProductID
        if len(Amazon_Objects) != 0 and (now - Amazon_Objects[0].DatePrice[-1]['Date']).seconds < UpdateThresh:
            return 'Time'

        price,name = GetThePrice(self)
        if price == None:
            return None

        TodayPrice = {'Date':now, 'Price':price}
        if len(Amazon_Objects) == 0:
            self.DatePrice.append(TodayPrice)
            self.ProductName = name
            self.save()
            return 'First'
        else:
            self = Amazon_Objects[0]
            self.DatePrice.append(TodayPrice)
            self.ProductName = name
            if len(self.DatePrice) > HistoryListLength:
                self.DatePrice = self.DatePrice[-HistoryListLength:]
            self.save()
            return 'Add'

    def ReturnDatePrice(self):
        Amazon_objs = Amazon_class.objects(ProductID = self.ProductID)
        if len(Amazon_objs) != 0:
            self = Amazon_objs[0]
            return self
        else:
            return None

    def ReturnAllID(self):
        ProductList = []
        Amazon_objs = Amazon_class.objects()
        for obj in Amazon_objs:
            ProductList.append(obj)
        return ProductList
        
        # print Amazon_Objects[0].ProductID,Amazon_Objects[0].DatePrice
if __name__ == '__main__':
    a = Amazon_class()
    # a.ProductID = 'B001130JN8'
    UpdateRest = a.UpdateAll()
    print UpdateRest