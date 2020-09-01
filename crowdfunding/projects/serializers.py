from rest_framework import serializers
from .models import Project, Pledge, Comment, Category

class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField()
    supporter_id = serializers.IntegerField()
    project_id = serializers.IntegerField()

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.anonymous= validated_data.get('anonymous', instance.anonymous)
        instance.supporter_id = validated_data.get('supporter_id', instance.supporter_id)
        instance.project_id = validated_data.get('project_id', instance.project_id)
        instance.save()
        return instance

class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    owner = serializers.ReadOnlyField(source='owner.id')

    def create(self, validated_data):
        return Project.objects.create(**validated_data)


class ProjectDetailSerializer(ProjectSerializer):
    pledge = PledgeSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'project_id','name', 'body', 'created_on'
        )
    name = serializers.CharField(max_length=80)
    body = serializers.CharField()
    created_on = serializers.DateTimeField()
    project_id = serializers.IntegerField()


    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

class CommentDetailSerializer(ProjectSerializer):
    comment = CommentSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.body = validated_data.get('body', instance.body)
        instance.created_on = validated_data.get('created_on', instance.created_on)
        instance.project_id = validated_data.get('project_id', instance.project_id)
        instance.save()
        return instance


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    lookup_field = 'name'

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

class CategoryProjectSerializer(CategorySerializer):
    project_categories = ProjectSerializer(many=True, read_only=True)

#     class Meta:
#         model = Category
#         fields = '__all__'

#     category = serializers.CharField(max_length=100)

    # def update(self, instance, validated_data):
    #     instance.category = validated_data.get('category', instance.category)
    #     instance.save()
    #     return instance


    # category = serializers.SlugRelatedField(slug_field='category', queryset=Category.objects.all())









