from rest_framework.views import APIView
from rest_framework.response import Response

class ArticleView(APIView):
    """Controller handle for API of Articles"""

    def get(self, request, id=None):
        if id is not None:
            """GET detail by id"""
            return Response({"message": f"Article profile details for article {id}"})
        else:
            """GET list of articles"""
            return Response({"message": "List of articles"})

    def post(self, request):
        """POST create new article"""
        return Response({"message": "Article created"})

    def put(self, request):
        """PUT update article"""
        return Response({"message": "Article updated"})

    def delete(self, request):
        """DELETE article"""
        return Response({"message": "Article deleted"})
