from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string

from works.models import Work, Category


def index(request):
    category = Category.objects.filter(status=True)

    works = Work.objects.active()
    paginator = Paginator(works, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'category': category}
    return render(request, 'home/index.html', context)


# def load_more_works_item(request):  # ajax
#     category = Category.objects.filter(status=True)
#
#     page_number = int(request.GET['page'])
#     works = Work.objects.active()
#     paginator = Paginator(works, 6)
#
#     page_obj = paginator.get_page(page_number)
#
#     context = {'page_obj': page_obj, 'category': category}
#
#     template = render_to_string('home/works_page_ajax.html', context)
#     return JsonResponse({'data': template, 'check': 'loadPge'}, status=200, )


def ContactMe(request):
    pass


def AboutMe(request):
    pass
