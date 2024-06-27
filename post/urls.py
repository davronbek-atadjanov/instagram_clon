from django.urls import path
from .views import  PostLisApiView, PostCreateView, PostRetrieveUpdateDestroyView, \
    PostCommentListView, PostCommentCreateView, CommentListCreateApiView, \
    PostLikeListView, CommentRetrieveView, CommentLikeListView, PostLikeApiView, \
    CommentLikeApiView

urlpatterns = [
    path('list/', PostLisApiView.as_view()),
    path('create/', PostCreateView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyView.as_view()),
    path('<uuid:pk>/likes/', PostLikeListView.as_view()),
    path('<uuid:pk>/comments/', PostCommentListView.as_view()),
    path('<uuid:pk>/comment/create/', PostCommentCreateView.as_view()),
    path('comments/', CommentListCreateApiView.as_view()),
    path('comment/<uuid:pk>/', CommentRetrieveView.as_view()),
    path('comment/<uuid:pk>/likes/', CommentLikeListView.as_view()),

    path("<uuid:pk>/create-delete-like/", PostLikeApiView.as_view()),
    path("comment/<uuid:pk>/create-delete-like/", CommentLikeApiView.as_view()),
]
