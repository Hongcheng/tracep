# Create your views here.
from models import *
from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Template,Context
from models import Amazon_class

def GetPid(query):
    start = query.find(u'/dp/')
    if start != -1:
        start += len(u'/dp/')
        end = query.find(u'/',start)
        return query[start:end]
    start = query.find(u'/gp/product/')
    if start != -1:
        start += len(u'/gp/product/')
        end = query.find(u'/',start)
        return query[start:end]
    return ''

def Amazon_Home_Page(request):
    query = request.GET.get('pID','')
    Rest = ''
    a = Amazon_class()
    ProductList = a.ReturnAllID()
    if query:
        pID = GetPid(query)#use this line to use the url as the input
        # pID = query#use this line to use ID as the input
        print pID
        a.ProductID = pID
        rest = a.UpdateDatePrice()
        print rest
        if rest == 'First' or rest == 'Add' or rest == 'Time':
            Rest = 'Succeed to add the product:' + pID
        else:
            Rest = 'Threr is no such a product:' + pID
    else:
        Rest = 'Input the productID you want to trace'
    t = get_template('Amazon_Home_Page.html')
    html = t.render(Context({'Rest':Rest, 'ProductList':ProductList}))
    return HttpResponse(html)

def Show_Amazon_Price(request, pID):
    a = Amazon_class(ProductID = pID)
    a.ProductID = pID
    Product = a.ReturnDatePrice()
    if Product == None:
        html = '<html><body><h1>There is no such a productID or this product have not been added to trace!!</h1></body></html>'
    else:    
        t = get_template('Amazon_Product.html')
        html = t.render(Context({'Product':Product}))
    return HttpResponse(html)

def AddAmazonPID(request):
    a = Amazon_class()
    a.ProductID = pID
    rest = a.UpdateDatePrice()
    if rest == None:
        html = '<html><body><h1>Faile to add this product ID</h1></body></html>'
    else:
        html = '<html><body><h1>Succeed to add this product ID</h1></body></html>'
        return HttpResponse(html)

if __name__ == '__main__':
    ShowAmazonPrice('B001130JN8')
