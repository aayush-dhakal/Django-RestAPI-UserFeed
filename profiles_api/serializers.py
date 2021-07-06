from rest_framework import serializers
from profiles_api import models

# serializer helps to convert data inputs into python objects and viceversa. It is needed to convert form api input data into python objects 

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
   
    class Meta: 
        # this sets up our serializer to point to userprofile model
        model = models.UserProfile  

        # list of fileds we want to manage through our serializer ie the list of fields accessable to our api
        # django automatically sets id by default and also sets it in readonly form
        fields = ('id','email','name','password')
        # password filed should only be available when creating or updating a user and should not be retrievable. To configure this use extra_kwargs
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'} # this makes password field in non readable form like *
            }
        }

    # by default ModelSerializer allows you to create simple objects in the database so it uses the default create function of the object manager to create the object. We want to override this functionality so that it uses create_user function(which we defined in models file) instead which will hash the password for us.

    def create(self, validated_date):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email = validated_date['email'],    
            name = validated_date['name'],
            password = validated_date['password'],
        )

        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        # django sets id and creaated_on to readonly by default
        fields = ('id','user_profile','status_text','created_on')
        # user_profile will be set based on the authenticated user so it should also be in readonly form
        extra_kwargs = {'user_profile': {'read_only':True}}


