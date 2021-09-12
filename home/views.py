from django.shortcuts import render

# Create your views here.
from works.models import Work, Category


def index(request):
    works = Work.objects.active()
    category = Category.objects.filter(status=True)
    context = {'works': works, 'category': category}
    return render(request, 'home/index.html', context)


def ContactMe(request):
    pass


def AboutMe(request):
    pass
