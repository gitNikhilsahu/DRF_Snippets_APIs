from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import View
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .serializers import ProductSerializers

import io
import json

from django.core.serializers import serialize


from .models import ProductModel
from .serializers import ProductSerializers 

def DRF_Home_View(request):
    return render(request, 'DRF/DRFHomePage.html')

class Product_CBV(View):
    def get(self, request):
        data = request.body
        if data:
            try:
                jd = json.loads(data)
                pno = jd.get("pno")
                qs = ProductModel.objects.get(no=pno)
                ps = ProductSerializers(qs)
                json_data = JSONRenderer().render(ps.data)
                return HttpResponse(json_data, content_type="application/json")
            except ProductModel.DoesNotExist:
                message = {"error": "Product Not There"}
                return HttpResponse(JSONRenderer().render(message), content_type="application/json")
            
        else:
            qs = ProductModel.objects.all()
            ps = ProductSerializers(qs, many=True)
            json_data = JSONRenderer().render(ps.data)
            return HttpResponse(json_data, content_type="application/json")

    def post(self, request):
        byte_data    = request.body
        stream_data  = io.BytesIO(byte_data)
        dict_data    = JSONParser().parse(stream_data)
        ps           = ProductSerializers(data=dict_data)

        if ps.is_valid():
            ps.save()
            message = {"message": "Product is Saved"}
        else:
            message = {"errors": ps.errors}
        
        json_data = JSONRenderer().render(message)
        return HttpResponse(json_data, content_type="application/json")
