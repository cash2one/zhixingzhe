from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from main.views import answer, detail, home, index_login, profile
from main.views import register, search, index_logout
from main.api import answers, questions, vote, push_answer, question, question_all, topics, push_comment, push_answer
from main.uploadview import upload_image

urlpatterns = [
	url(r'^$', home),
    url(r'^admin/', admin.site.urls),
    url(r'^answer/$', answer, name="answer"),
    url(r'^detail/(?P<question_id>\d+)/$', detail, name="detail"),
    url(r'^home/$', home, name="home"),
    url(r'^login', index_login, name="login"),
    url(r'^logout/$', index_logout, name="logout"),
    url(r'^profile/(?P<user_id>\d+)$', profile, name="profile"),
    url(r'^register/$', register, name="register"),
    url(r'^search/$', search, name="search"),

    url(r'^vote/$', vote, name="vote"),
    url(r'^api/answers/(?P<start>\d+)/(?P<end>\d+)$', answers, name="answers"),
    url(r'^api/topics/$', topics, name="topics"),
    url(r'^api/question/$', question, name="question"),
    url(r'^api/push_comment/$', push_comment, name="push_comment"),
    url(r'^api/question_all/$', question_all, name="question_all"),
    url(r'^api/questions/(?P<id>\d+)$', questions, name="questions"),
    url(r'^api/push_answer/$', push_answer, name="push_answer"),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^uploadimg/',upload_image),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
