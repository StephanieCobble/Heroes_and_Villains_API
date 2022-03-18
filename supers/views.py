
# Create your views here.



from django.http import Http404 
from rest_framework.views import APIView  

from rest_framework.response import Response

from super_types.models import SuperType
from .serializers import SuperSerializer  
from .models import Super  
from rest_framework import status  


class SuperList(APIView):
    def get(self, request):
        type_param = request.query_params.get('type')
        supers = Super.objects.all()
        
        custom_response_dictionary = {}        

        super_types = SuperType.objects.all()
        if type_param:
            supers = supers.filter(super_type__type=type_param)
            serializer = SuperSerializer(supers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            for super_type in super_types:
                supers = Super.objects.filter(super_type_id=super_type.id)
                serializer = SuperSerializer(supers, many=True)
                custom_response_dictionary[super_type.type] = {
                    "supers": serializer.data,
                    
                }    
            return Response(custom_response_dictionary, status=status.HTTP_200_OK)
   

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


