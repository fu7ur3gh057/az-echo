from rest_framework.pagination import PageNumberPagination


class SynthesisPagination(PageNumberPagination):
    page_size = 9
