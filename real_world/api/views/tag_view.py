from rest_framework.views import APIView
from rest_framework.response import Response

class TagView(APIView):
    """Controller handle for API of Tags"""

    def get(self, request):
        """GET tag"""
        return Response({"message": "Tag profile list"})
