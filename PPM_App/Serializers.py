from rest_framework import serializers
from PPM_App.Models import Poll, Choice, Response

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class ResponseSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Response
        fields = '__all__'

class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    responses = ResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = '__all__'
