from django.shortcuts import render

# Create your views here.
from .models import DoubanMovie
from django.db.models import Avg

def movie_short(request):
    ###  从models取数据传给template  ###
    shorts = DoubanMovie.objects.all()
    # 评论数量
    counter = DoubanMovie.objects.all().count()

    # 平均星级
    # star_value = DoubanMovie.objects.values('n_star')
    star_avg =f" {DoubanMovie.objects.aggregate(Avg('n_star'))['n_star__avg']:0.1f} "
    # 情感倾向
    sent_avg =f" {DoubanMovie.objects.aggregate(Avg('sentiment'))['sentiment__avg']:0.2f} "

    # 正向数量
    queryset = DoubanMovie.objects.values('sentiment')
    condtions = {'sentiment__gte': 0.5}
    plus = queryset.filter(**condtions).count()

    # 负向数量
    queryset = DoubanMovie.objects.values('sentiment')
    condtions = {'sentiment__lt': 0.5}
    minus = queryset.filter(**condtions).count()

    # return render(request, 'douban.html', locals())
    return render(request, 'result.html', locals())