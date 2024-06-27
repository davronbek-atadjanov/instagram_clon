from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import  Post, PostLike, PostComment, CommentLike
from rest_framework import generics, status
from .serializers import PostSerializer, PostLikeSerializer, CommentSerializer, CommentLikeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from shared.custom_pagination import CustomPagination
class PostLisApiView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = PostSerializer

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "code": status.HTTP_200_OK,
                "message": "Post muvaffaqiyatli update bo'ldi",
                "data": serializer.data
            }
        )

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Post muvaffaqiyatli delete qilindi"
            }
        )


class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostComment.objects.filter(post__id=post_id)
        return queryset


class PostCommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id=post_id)


class CommentListCreateApiView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    queryset = PostComment.objects.all()
    pagination_class = CustomPagination
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentRetrieveView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]
    queryset = PostComment.objects.all()


class PostLikeListView(generics.ListAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return PostLike.objects.filter(post__id=post_id)


class CommentLikeListView(generics.ListAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        comment_id = self.kwargs['pk']
        return CommentLike.objects.filter(comment__id=comment_id)


# class PostLikeApiView(APIView):
#
#     def post(self, request, pk):
#         try:
#             post_like = PostLike.objects.create(
#                 author=self.request.user,
#                 post_id=pk
#             )
#             serializer = PostLikeSerializer(post_like)
#             data = {
#                 "success": True,
#                 "message": "Postga like qo'shildi",
#                 "data": serializer.data
#             }
#             return Response(data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             data = {
#                 "success": False,
#                 "message": f"{str(e)}"
#             }
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         try:
#             post_like = PostLike.objects.get(
#                 author=self.request.user,
#                 post_id=pk
#             )
#             post_like.delete()
#             data = {
#                 "success": True,
#                 "message": "Post like successfully delete"
#             }
#             return Response(data, status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#             data = {
#                 "success": False,
#                 "message": f"{str(e)}"
#             }
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)

# class PostLikeApiView(APIView):
#
#     def post(self, request, pk):
#         try:
#             post_like = PostLike.objects.get(
#                 author=self.request.user,
#                 post_id=pk
#             )
#             post_like.delete()
#             data = {
#                 "success": True,
#                 "message": "Postdan like successfully delete"
#             }
#             return Response(data, status=status.HTTP_204_NO_CONTENT)
#         except PostLike.DoesNotExist:
#             post_like = PostLike.objects.create(
#                 author=self.request.user,
#                 post_id=pk
#             )
#             serializer = PostLikeSerializer(post_like)
#             data = {
#                 "success": True,
#                 "message": "Postga like successfully add",
#                 "data": serializer.data
#             }
#             return Response(data, status=status.HTTP_201_CREATED)
#
        # Yuqoridagi kod uncha bestpractic code emas



class PostLikeApiView(APIView):

    def post(self, request, pk):
        try:
            post_like, created = PostLike.objects.get_or_create(
                author=self.request.user,
                post_id=pk
            )
            if not created:
                post_like.delete()
                data = {
                    "success": True,
                    "message": "like  removed"
                }
                return Response(data, status=status.HTTP_204_NO_CONTENT)
            else:
                serializer = PostLikeSerializer(post_like)
                data = {
                    "success": True,
                    "message": "Like added",
                    "data": serializer.data
                }
                return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {
                "success": False,
                "message": f"{str(e)}"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

# class CommentLikeApiView(APIView):
#
#     def post(self, request, pk):
#         try:
#             comment_like = CommentLike.objects.create(
#                 author=self.request.user,
#                 post_id=pk
#             )
#             serializer = CommentLikeSerializer(comment_like)
#             data = {
#                 "success": True,
#                 "message": "Comment add",
#                 "data": serializer.data
#             }
#             return Response(data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             data = {
#                 "success": False,
#                 "message": f"{str(e)}"
#             }
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         try:
#             comment_like = CommentLike.objects.get(
#                 author=self.request.user,
#                 comment_id=pk
#             )
#             comment_like.delete()
#             data = {
#                 "success": True,
#                 "message": "Comment successfully delete"
#             }
#             return Response(data, status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#             data = {
#                 "success": False,
#                 "message": f"{str(e)}"
#             }
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)
#
#


class CommentLikeApiView(APIView):
    def post(self, reqeust, pk):
        try:
            comment_like, created = CommentLike.objects.get_or_create(
                author=self.request.user,
                comment_id=pk
            )

            if not created:
                comment_like.delete()
                data = {
                    "success": True,
                    "message": "Comment like remove"
                }
                return Response(data, status=status.HTTP_204_NO_CONTENT)
            else:
                serializer = CommentLikeSerializer(comment_like)
                data = {
                    "success": True,
                    "message": "Comment like added",
                    "data": serializer.data
                }
                return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {
                "success": False,
                "message": f"{str(e)}"
            }