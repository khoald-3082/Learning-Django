from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    # Override param page size to 'limit'
    page_size_query_param = 'limit'
    page_size = 10
    max_page_size = 100

    # Override param page number to 'page_number'
    page_query_param = 'page_number'

    def get_paginated_response(self, data):
        return Response({
            "data": data,
            "pagination": {
                "total_items": self.page.paginator.count,
                "current_page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "has_more": self.page.number < self.page.paginator.num_pages
            }
        })
