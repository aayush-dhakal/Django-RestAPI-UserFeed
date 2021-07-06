from rest_framework import authentication
from rest_framework.views import APIView
# for viewsets
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


# APIView section
class HelloApiView(APIView):
    """Test API View"""

    # serializer here tells our api view what data to expect for different post/put/patch request
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""

        an_apiview = [
            'uses HTTP methods as function (get,post,put,patch,delete)',
            'is similar to traditional Django view',
            'Gives you the most control over your application logic',
            'is mapped manually to urls'
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """create a hello message with our name"""

        # here we retrieve the serializer and parse in the data that was sent in the request
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():  # checking the validation of input field from serializer
            name = serializer._validated_data.get('name')  # gets the name's value from serializer
            message = f'Hello {name}'
            return Response({'message': message})

        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                ) # default response status is 200


    # pk stands for primary key so it is an id that describes the object to be updated
    def put(self, request, pk=None): 
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None): 
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None): 
        """Delete an object"""
        return Response({'method': 'DELETE'})

    

# viewsets section   
class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    # specifying the serializer
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""

        a_viewset = [
            'uses actions (list, create, retrieve, update, partial_update, destroy)',
            'automatically maps to URLs using routers',
            'provides more functionality with less code'
        ]

        return Response({'message':'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """create a hello message with our name"""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer._validated_data.get('name')  
            message = f'Hello {name}!'
            return Response({'message': message})

        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )

    def retrieve(self, request, pk=None): 
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None): 
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None): 
        """Handle a partial update of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None): 
        """Delete an object"""
        return Response({'http_method': 'DELETE'})


# modelviewset section (used when working with database)
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""

    # first assign the serializer class
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all() # assigned all the retrieved objects from the model in querset 
    # in modelviewset when you do above two steps django automatically configurs all the common http methods(list, update, destroy,..) for us

    # checks if user's credential is correct(like loggin in)
    authentication_classes = (TokenAuthentication,)  # make sure to add comma(,) at end so that tokens can be created as tuple instead of a single item

    # to allow the authorization for modifying the data
    permission_classes = (permissions.UpdateOwnProfile,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')  # seach by name or email for filtering


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""

    # you could directly attach ObtainAuthToken in urls path(if only gonna test with postman) however,
    # obtainauthtoken is not enabled in browsable django admin site so to enable it we have to create this class and add following code
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handle creating, reading and updating profile feed items"""
    authentication_classes=(TokenAuthentication,)
    serializer_class=serializers.ProfileFeedItemSerializer
    queryset=models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus, # our own custom permission. this stops users to try to update other user's feed
        # IsAuthenticatedOrReadOnly  # django rest permission. this makes sure user must be  authenticated to perform any request that is not a read request ie stops user on creating a new feed if they are not authenticated. However, this method does allows non authenticated user to view the api(ie the feed api)
        IsAuthenticated # user can now only view the api if they are logged in ie authenticated. even the basic GET readable only api are shown only if users are logged in
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)