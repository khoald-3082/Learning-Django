from django.core.paginator import Paginator
from rest_framework.response import Response

def paginate_queryset(queryset, request, serializer_class):
    """
    Helper function to paginate queryset
    """
    page_size = int(request.GET.get("page_size", 10))
    page_number = int(request.GET.get("page", 1))

    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page_number)
    return Response({
        "data": serializer_class(page_obj, many=True).data,
        "pagination": {
            "total": paginator.count,
            "current_page": page_number,
            "total_pages": paginator.num_pages,
            "has_data": len(page_obj) > 0
        }
    })
