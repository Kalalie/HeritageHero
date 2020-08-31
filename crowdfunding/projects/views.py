from django.http import Http404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Pledge, Comment
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

class ProjectList(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

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
            status= status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request,pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status.HTTP_204_NO_CONTENT)

class CommentList(APIView):

    def get(self, request, pk):
        comments = Comment.objects.values()
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

# class CommentDetail(APIView): 
#     def get_object(self, pk):
#         try:
#             return CommentDetail.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         comment = self.get_object(pk)
#         serializer = CommentDetailSerializer(comment)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         comment = self.get_object(pk)
#         data = request.data
#         serializer = CommentDetailSerializer(
#             instance=comment,
#             data=data,
#             partial=True
#         )
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             return Response(
#             serializer.errors,
#             status= status.HTTP_400_BAD_REQUEST
        # )

class PledgesList(APIView):

    def get(self, request):
        pledges = Pledge.objects.values()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PledgeSerializer(data=request.data)
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
            serializer.save()
        else:
            return Response(
            serializer.errors,
            status= status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request,pk):
        pledge = self.get_object(pk)
        pledge.delete()
        return Response(status.HTTP_204_NO_CONTENT)

