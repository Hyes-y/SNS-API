from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom Pagination
    'page_size' 파라미터를 통해 사용자가 설정 가능
    default: 10
    max_size: 30
    """
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 30
