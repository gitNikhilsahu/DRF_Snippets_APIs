from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from django.views.generic import View
import json

from .models import ProductModel
from .forms import ProductForm

from django.core.serializers import serialize

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def Examples_App_Home_View(request):
    return render(request, 'ExamplesApp/ExamplesAppHomePage.html')

class http_response_CBV(View):
    def get(self, request):
        
        emp_info = {"idno": 101, "name": "nik", "salary": 8000000.00, "status": False, "old_company": None}

        json_data = json.dumps(emp_info)
        return HttpResponse(json_data, content_type="application/json")

class json_response_CBV(View):
    def get(self, request):
        
        emp_info = {"idno": 101, "name": "nik", "salary": 8000000.00, "status": False, "old_company": None}

        json_data = json.dumps(emp_info)
        return JsonResponse(emp_info)

class view_all_product_CBV(View):
    def get(self, request):
        qs = ProductModel.objects.all()

        data= {}
        for row in qs:
            d1 = {
                row.no:{
                    "product_name": row.name,
                    "product_price": row.price,
                    "product_quantity": row.quantity
                }
            }
            data.update(d1)
        
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type="application/json")

class view_all_product_serialize_CBV(View):
    def get(self, request):
        qs = ProductModel.objects.all()

        json_data = serialize('json', qs)
        return HttpResponse(json_data, content_type="application/json")
        

class view_one_product_CBV(View):
    def get(self, request, product):
        try:
            qs = ProductModel.objects.get(no=product)
            data = {"product_name": qs.name,
                    "product_price": qs.price,
                    "product_quantity": qs.quantity}
            json_data = json.dumps(data)
        except ProductModel.DoesNotExist:
            error_mess = {"error": "Product Not in DB"}
            json_data = json.dumps(error_mess)
        return HttpResponse(json_data, content_type="application/json")

class view_one_product_serialize_CBV(View):
    def get(self, request, product):
        try:
            res = ProductModel.objects.get(no=product)
            json_data = serialize('json', [res])
        except ProductModel.DoesNotExist:
            error_mess = {"error": "Product Not in DB"}
            json_data = json.dumps(error_mess)
        return HttpResponse(json_data, content_type="application/json")


@method_decorator(csrf_exempt, name='dispatch')
class insert_one_product(View):
    def post(self, request):
        data = request.body
        json_data = json.loads(data) #binary data to json
        pf = ProductForm(json_data)
        if pf.is_valid():
            pf.save()
            json_data = json.dumps({"success": "Product is saved"})
        else:
            json_data = json.dumps(pf.errors)
        
        return HttpResponse(json_data, content_type="application/json")


@method_decorator(csrf_exempt, name='dispatch')
class insert_multiple_product(View):
    def post(self, request):
        data = request.body
        json_data = json.loads(data) #binary data to json
        for x in json_data:
            pf = ProductForm(x)
            if pf.is_valid():
                pf.save()
                json_data = json.dumps({"success": "Product is saved"})
            else:
                json_data = json.dumps(pf.errors)
        
        return HttpResponse(json_data, content_type="application/json")


@method_decorator(csrf_exempt, name='dispatch')
class update_one_product(View):
    def put(self, request, product):
        try:
            old_product = ProductModel.objects.get(no=product)
            new_product = json.loads(request.body)
            pf = ProductForm(new_product, instance=old_product)
            if pf.is_valid():
                pf.save()
                json_data = json.dumps({"success": "Product is Updated"})
            else:
                json_data = json.dumps(pf.errors)
                return HttpResponse(json_data, content_type="application/json")
        except ProductModel.DoesNotExist:
            json_data = json.dumps({"error": "Invalid Product...."})
        return HttpResponse(json_data, content_type="application/json")


@method_decorator(csrf_exempt, name='dispatch')
class update_one_product_data(View):
    def put(self, request, product):
        try:
            old_product = ProductModel.objects.get(no=product)
            new_product = json.loads(request.body)
            
            data = {
                'no': old_product.no,
                "name:": old_product.name,
                "price": old_product.price,
                "quantity": old_product.quantity
            }

            for key, value in new_product.items():
                data[key] = value

            pf = ProductForm(data, instance=old_product)
            if pf.is_valid():
                pf.save()
                json_data = json.dumps({"success": "Product is Updated"})
            else:
                json_data = json.dumps(pf.errors)
            return HttpResponse(json_data, content_type="application/json")

        except ProductModel.DoesNotExist:
            json_data = json.dumps({"error": "Invalid Product...."})
        return HttpResponse(json_data, content_type="application/json")



@method_decorator(csrf_exempt, name='dispatch')
class delete_one_product(View):
    def delete(self, request, product):
        try:
            result = ProductModel.objects.get(no=product).delete()
            if result[0] == 1:
                json_data = json.dumps({"message": "Product is Deleted"})
                return HttpResponse(json_data, content_type="application/json")
        except:
            json_data = json.dumps({"error": "Invalid Product"})
        return HttpResponse(json_data, content_type="application/json")



class CURD(View):
    def get(self, request):
        qs = ProductModel.objects.all()

        json_data = serialize('json', qs)
        return HttpResponse(json_data, content_type="application/json")

    def post(self, request):
        data = request.body
        json_data = json.loads(data) #binary data to json
        pf = ProductForm(json_data)
        if pf.is_valid():
            pf.save()
            json_data = json.dumps({"success": "Product is saved"})
        else:
            json_data = json.dumps(pf.errors)
        
        return HttpResponse(json_data, content_type="application/json")

# price_lte = request.GET['price_lte'] GET parameters query params

    def put(self, request):
        product = request.GET['product']
        try:
            old_product = ProductModel.objects.get(no=product)
            new_product = json.loads(request.body)
            pf = ProductForm(new_product, instance=old_product)
            if pf.is_valid():
                pf.save()
                json_data = json.dumps({"success": "Product is Updated"})
            else:
                json_data = json.dumps(pf.errors)
                return HttpResponse(json_data, content_type="application/json")
        except ProductModel.DoesNotExist:
            json_data = json.dumps({"error": "Invalid Product...."})
        return HttpResponse(json_data, content_type="application/json")

    # def delete(self, request):
    #     try:
    #         result = ProductModel.objects.get(no=product).delete()
    #         if result[0] == 1:
    #             json_data = json.dumps({"message": "Product is Deleted"})
    #             return HttpResponse(json_data, content_type="application/json")
    #     except:
    #         json_data = json.dumps({"error": "Invalid Product"})
    #     return HttpResponse(json_data, content_type="application/json")







# { "no": 123, "name": "First 212 Product", "price": 299.0, "quantity": 6}

    