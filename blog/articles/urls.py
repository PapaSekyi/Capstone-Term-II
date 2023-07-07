from django.urls import path
from . import views 

app_name='articles'

urlpatterns=[

    path('',views.articles,name='arti'),
    path('predict/', views.predict_next_words, name='predict_next_words'),
    path('add_genre/',views.get_genre,name='add_genre'),
    path('add_article/',views.add_article,name='add_article'),
    path('<slug:slug>/update_article/',views.UpdateArticleMixin.as_view(),name='update_article'),
    path('<slug:slug>/delete_article/',views.DeleteArticleMixin.as_view(),name='delete_article'),
    path('<slug:slug>/',views.article_detail,name='article_detail'), 

]