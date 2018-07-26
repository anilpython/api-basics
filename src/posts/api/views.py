from django.db.models import Q
from rest_framework.generics import (
    ListAPIView, 
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    )

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
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
from .pagination import PostLimitOffsetPagination,PostPageNumgerPagination

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
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]#http://localhost:8000/api/posts/?search=Anil&ordering=-title
    search_fields = ['title','content','user__first_name'] #localhost:8000/api/posts/?search=Anil
    pagination_class = PostPageNumgerPagination

    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Post.objects.all() #filter(user=self.request.user)
        query = self.request.GET.get("q") #localhost:8000/api/posts/?q=Anil
        if query:
            queryset_list = queryset_list.filter(
                    Q(title__icontains=query)|
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list

