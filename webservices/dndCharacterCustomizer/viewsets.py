from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Character
from .serializers import CharacterSerializer

class CharacterViewSet(viewsets.ModelViewSet):
    """
    Viewset for creating, listing, updating, retrieving, and deleting Character instances.
    """

    # Specifying the serializer class to be used
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


    def retrieve(self, request, pk=None):
        """
        Get a character by primary key (pk).
        If not found, return a 404 response.
        """
        try:
            character = Character.objects.get(pk=pk)
        except Character.DoesNotExist:
            return Response({"error": "Character not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize and return character data in JSON format
        serializer = CharacterSerializer(character)
        return Response(serializer.data)

    def list(self, request):
        """
        Get a list of all characters.
        """
        queryset = self.get_queryset()  # Use the get_queryset method
        serializer = CharacterSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Handle POST requests to create a new character.
        Validate data before saving.
        """
        serializer = CharacterSerializer(data=request.data)
        if serializer.is_valid():
            # Save and create a new character instance
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Handle PUT requests to update an existing character by pk.
        """
        try:
            character = Character.objects.get(pk=pk)
        except Character.DoesNotExist:
            return Response({"error": "Character not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Update the character's data
        serializer = CharacterSerializer(character, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Handle DELETE requests to delete a character by pk.
        """
        try:
            character = Character.objects.get(pk=pk)
        except Character.DoesNotExist:
            return Response({"error": "Character not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete the character instance
        character.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
