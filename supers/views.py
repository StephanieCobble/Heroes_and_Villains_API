
# Create your views here.
from django.http import Http404 
from rest_framework.views import APIView  

from rest_framework.response import Response  
from .serializers import SuperSerializer  
from .models import Super  
from rest_framework import status  


class SuperList(APIView):
    def get(self, request, format=None):
        supers = Super.objects.all()
        # super_param = Super.objects.filter(super__type=super_param)
        type_param = self.request.query_params.get('type')
        if type_param :
            supers = supers.filter(super_type__type=type_param)

        serializer = SuperSerializer(supers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SuperDetail(APIView):
    def get_object(self, pk):
        try:
            return Super.objects.get(pk=pk)  
        except Super.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        super = self.get_object(pk)
        serializer = SuperSerializer(super)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        super = self.get_object(pk)
        serializer = SuperSerializer(super, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        super = self.get_object(pk)
        super.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SuperFK(APIView):
    def get(self, request, fk, format=None):
        super = Super.objects.filter(super_type=fk)
        serializer = SuperSerializer(super, many=True)
        return Response(serializer.data)

# class SuperListType(APIView):
#     def get(self, request, fk, format=None):
#         super_param = request.query_param.get('type')
#         sort_param = request.query_params.get('sort')
#         if super_param:
#             supers = supers.filter(super__type=super_param)
        
#         if sort_param:
#             supers = supers.order_by(sort_param)
        
#         serializer = SuperSerializer(super, many=True)
#         return Response(serializer.data)

