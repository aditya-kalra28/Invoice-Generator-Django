from urllib import request
from django.shortcuts import render
from rest_framework import viewsets
from .models import Product
from .serializer import productSerializer
import requests
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import View
from django.contrib.staticfiles import finders
import os
from django.conf import settings

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = productSerializer

def index(request):
    data = requests.request("GET","http://127.0.0.1:8000/api").json()
    if request.method=="POST":
        if 'ViewInvoice' in request.POST:
            formData = request.POST.items()
            final=[]
            ind=0
            total=0
            total_quantity=0
            for i in formData:
                if ind==0:
                    ind=1
                elif i[0]=="GetPDF" or i[0]=="ViewInvoice":
                    pass
                else:
                    a=0
                    if i[1]=='':
                        pass
                    else:
                        a=int(i[1])
                    final.append([ind,data[ind-1]['id'],data[ind-1]['name'],data[ind-1]['description'],data[ind-1]['price'],a,a*data[ind-1]['price']])
                    total+=a*data[ind-1]['price']
                    ind+=1
                    total_quantity+=a
            print(final)
            return render(request,"invoice.html",{"final": final, "total":total, "total_quantity": total_quantity})
        elif 'GetPDF' in request.POST:
            formData = request.POST.items()
            final=[]
            ind=0
            total=0
            total_quantity=0
            for i in formData:
                if ind==0:
                    ind=1
                elif i[0]=="GetPDF" or i[0]=="ViewInvoice":
                    pass
                else:
                    a=0
                    if i[1]=='':
                        pass
                    else:
                        a=int(i[1])
                    final.append([ind,data[ind-1]['id'],data[ind-1]['name'],data[ind-1]['description'],data[ind-1]['price'],a,a*data[ind-1]['price']])
                    total+=a*data[ind-1]['price']
                    ind+=1
                    total_quantity+=a
            print(final)
            template_path = 'invoice.html'
            context = {"final": final, "total":total, "total_quantity": total_quantity}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)

            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)
            # if error then show some funny view
            if pisa_status.err: 
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        
    return render(request,"index.html",{"data": data})



def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path

