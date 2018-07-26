from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField
from posts.models import Post

class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
		'title',
		'slug',
		'content',
		'publish',
		]
post_detail_url = HyperlinkedIdentityField(
	view_name = "posts-api:detail",
	lookup_field = "slug",
	)
post_detail_delete_url = HyperlinkedIdentityField(
	view_name = "posts-api:delete",
	lookup_field = "slug",
	)

class PostListSerializer(ModelSerializer):
	url = post_detail_url
	class Meta:
		model = Post
		fields = [
		'url',
		'user',
		'id',
		'title',
		'content',
		'publish',
		]

class PostDetailSerializer(ModelSerializer):
	url = post_detail_url
	delete_url = post_detail_delete_url
	class Meta:
		model = Post
		fields = [
		'url',
		'title',
		'publish',
		'content',
		'delete_url'
		]