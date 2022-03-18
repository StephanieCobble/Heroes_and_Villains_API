
# Create your views here.

from django.http import Http404 
from rest_framework.views import APIView  
from rest_framework.response import Response

from supers.models import Super
from supers.serializers import SuperSerializer
from .serializers import SuperTypeSerializer  
from .models import SuperType  
from rest_framework import status  


class SuperTypeList(APIView):
    def get(self, request, format=None):
        super_types = SuperType.objects.all()
        serializer = SuperTypeSerializer(super_types, many=True)
        
        custom_response_dictionary = {}
        for super_type in super_types:
            supers = Super.objects.filter(super_type_id=super_type.id)
            super_serializer = SuperSerializer(supers, many=True)
            custom_response_dictionary[super_type.type] = {
                "type": super_type.type,
                "supers": super_serializer.data
            }
            return Response(custom_response_dictionary)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SuperTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SuperTypeDetail(APIView):
    def get_object(self, pk):
        try:
            return SuperType.objects.get(pk=pk)  
        except SuperType.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        super_type = self.get_object(pk)
        serializer = SuperTypeSerializer(super_type)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        super_type = self.get_object(pk)
        serializer = SuperTypeSerializer(super_type, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        super_type = self.get_object(pk)
        super_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)