from django.conf.urls import patterns, include, url
from blog.views import ArticleYearArchiveView

urlpatterns = patterns('blog.views',
    url(r'^$', 'index'),
    url(r'^(?P<article_id>\d+)/$', 'detail'),
    url(r'^category/(?P<category_id>\d+)/$', 'category_article'),
    url(r'^archive_index/$', 'archive_index'),
    url(r'^category/$', 'category'),
    url(r'^search/$', 'search'),
    url(r'^archive/(?P<year>\d{4})/$',
        ArticleYearArchiveView.as_view(),
        name="article_year_archive",)
)
