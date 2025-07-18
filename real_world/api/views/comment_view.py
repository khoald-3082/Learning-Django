from rest_framework.views import APIView
from rest_framework.response import Response

class CommentView(APIView):
    """Controller handle for API of Comments"""

    def get(self, request, id=None):
        """GET comments for article"""
        return Response({"message": f"Comment profile details for comment {id}"})

    def post(self, request):
        """POST create comment for article"""
        return Response({"message": "Comment created"})

    def put(self, request):
        """PUT update comment for article"""
        return Response({"message": "Comment updated"})

    def delete(self, request):
        """DELETE comment for article"""
        return Response({"message": "Comment deleted"})
