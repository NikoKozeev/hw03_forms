from django.core.paginator import Paginator
from constants import OPTIMAL_NUMBER_OF_POSTS


def page_func(request, post_list):
    paginator = Paginator(post_list, OPTIMAL_NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
