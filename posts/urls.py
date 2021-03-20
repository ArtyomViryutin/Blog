from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('', cache_page(20)(views.PostsListView.as_view()), name='index'),
    path('new/', views.PostCreateView.as_view(), name='new_post'),
    path('follow/', views.FollowPostsListView.as_view(), name='follow'),
    path('<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('<str:username>/follow/', views.profile_follow, name='profile_follow'),
    path('<str:username>/unfollow/', views.profile_unfollow, name='profile_unfollow'),
    path('<str:username>/<int:id>/', views.PostDetailView.as_view(), name='post'),
    path('<str:username>/<int:id>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('<str:username>/<int:id>/comment', views.CommentCreateView.as_view(), name='add_comment'),
    path('group/<slug:slug>/', cache_page(20)(views.GroupPostsView.as_view()), name='group'),
]
