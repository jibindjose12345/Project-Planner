from rest_framework import serializers

from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.EmailField()

    class Meta:

        model = Profile

        fields = ['username','first_name','email','password','role','tech',]

        read_only_fields =['email']

        extra_kwargs = {'password': {'write_only': True}}