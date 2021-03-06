from django.http import Http404
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Pledge, Comment, Category
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, CommentSerializer, CategorySerializer, CategoryProjectSerializer
from .permissions import IsOwnerOrReadOnly

class ProjectList(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get(self, request):
        projects = self.get_query()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def get_query(self):
        queryset = Project.objects.all()
        project = self.request.query_params.get('q', None)
        if project is not None:
            queryset = queryset.filter(title__icontains=project)
        return queryset


    def post(self,request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status= status.HTTP_400_BAD_REQUEST
        )


class ProjectDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly    
    ]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance=project,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request,pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentList(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly    
    ]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        comments = project.comment.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self,request, pk):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status= status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request,pk):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status.HTTP_204_NO_CONTENT)

class CommentDetail(APIView): 
    def get_object(self, pk):
        try:
            return CommentDetail.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentDetailSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        comment = self.get_object(pk)
        data = request.data
        serializer = CommentDetailSerializer(
            instance=comment,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
            serializer.errors,
            status= status.HTTP_400_BAD_REQUEST
        )

class PledgesList(APIView):

    def get(self, request):
        pledges = Pledge.objects.values()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status= status.HTTP_400_BAD_REQUEST
        )

class PledgesDetail(APIView):

    def get_object(self, pk):
        try:
            return Pledge.objects.get(pk=pk)
        except Pledge.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        pledges = self.get_object(pk)
        serializer = PledgeSerializer(pledges)
        return Response(serializer.data)

    def put(self, request, pk):
        pledge = self.get_object(pk)
        data = request.data
        serializer = PledgeSerializer(
            instance=pledge,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save(supporter=request.user)
        else:
            return Response(
            serializer.errors,
            status= status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request,pk):
        pledge = self.get_object(pk)
        pledge.delete()
        return Response(status.HTTP_204_NO_CONTENT)

class CategoryList(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )


