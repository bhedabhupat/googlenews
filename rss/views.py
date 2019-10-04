from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .models import RssData


# Create your views here.
def home(request):
    if request.is_ajax():
        sorttype = request.GET.get('sorttype')
        if not sorttype:
            lists = RssData.objects.all().order_by("-pub_date")
        else:
            lists = RssData.objects.all().order_by(sorttype)
        search = request.GET.get('search')
        if search is not None:
            lists = lists.filter(
                Q(title__icontains=search) | Q(source__icontains=search) | Q(pub_date__icontains=search))
        paginator = Paginator(lists, 20)
        page = request.GET.get('page')
        rss_data = paginator.get_page(page)
        return HttpResponse(render_to_string('list.html', {'rss_data': rss_data}))
    return render(request, 'home.html')
