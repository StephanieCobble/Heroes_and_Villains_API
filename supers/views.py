
# Create your views here.



from django.http import Http404 
from rest_framework.views import APIView  

from rest_framework.response import Response

from super_types.models import SuperType
from .serializers import SuperSerializer  
from .models import Power, Super  
from rest_framework import status  
from django.db.models import Count


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

    def get_power(self, pk):
        try:
            return Power.objects.get(pk=pk)
        except Power.DoesNotExist:
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

    def patch(self, request, pk, pk2):
        super = self.get_object(pk)
        power = self.get_power(pk2)
        super.powers.add(power)
        serializer = SuperSerializer(super)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Bonus 2:
# •	Create an endpoint that allows you to pass in a hero name and villain name as Query params.
# •	Query for each of the submitted Supers and compare their number of powers. Whoever has more powers listed is the winner
# •	Send back a custom object response that contains a 'winner' key containing the winner's info and a 'loser' key containing the loser's info, or a different message if it is a tie.


class SuperFight(APIView):

    def get_super(self, super):
        try:
            return Super.objects.get(name=super)  
        except Super.DoesNotExist:
            raise Http404
    
    def hero_vs_villain(self, super_one, super_two):
        super_type_one = super_one.super_type
        super_type_two = super_two.super_type
        if super_type_one == super_type_two:
            False
        else:
            return True

    def power_count(self, super):
        power_count_result = Super.objects.annotate(power_number=Count('powers')).get(id=super.id)
        count = power_count_result.power_number
        return count

    def get(self, request, super_one, super_two):
        super_one = self.get_super(super_one)
        super_two = self.get_super(super_two)
        battle = self.hero_vs_villain(super_one, super_two)
        if battle == False:
            if super_one.super_type_id == 1:
                return Response(f'You must battle against an opponent!')
            else:
                return Response(f'You must battle again an opponent!')
        super_one_count = self.power_count(super_one)
        super_two_count = self.power_count(super_two)
        if super_one_count == super_two_count:
            custom_battle_response = "Draw!"
        elif super_one_count > super_two_count:
            win_serializer = SuperSerializer(super_one)
            lose_serializer = SuperSerializer(super_two)
        else:
            win_serializer = SuperSerializer(super_two)
            lose_serializer = SuperSerializer(super_one)
        custom_battle_response = {
            "Winner!": win_serializer.data,
            "Loser!": lose_serializer.data
        }
        return Response(custom_battle_response, status=status.HTTP_200_OK)