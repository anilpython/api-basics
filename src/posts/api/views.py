from rest_framework.generics import (
	ListAPIView, 
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
	)
from posts.models import Post
from .serializers import (PostListSerializer, 
	PostDetailSerializer, 
	PostCreateUpdateSerializer,
	)

from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)

from .permissions import IsOwnerOrReadOnly

class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user) # title = "my title" we can pass field values here

class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = "slug" # lookup_field_kwarg = "abc

class PostUpdateAPIView(UpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	lookup_field = "slug" # lookup_field_kwarg = "abc"
	permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

	def perform_update(self, serializer):
		serializer.save(user=self.request.user)

class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = "slug" # lookup_field_kwarg = "abc"

class PostListAPIView(ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializer

