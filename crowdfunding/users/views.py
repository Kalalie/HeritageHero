from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly



class CustomUserList(APIView):

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class CustomUserDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly    
    ]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        CustomUser = self.get_object(pk)
        data = request.data
        serializer = CustomUserSerializer(
            instance=CustomUser,
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
        CustomUser = self.get_object(pk)
        CustomUser.delete()
        return Response(status.HTTP_204_NO_CONTENT)

class Register(APIView):
    def post(self, request):
        user = User.objects.create(
                username=request.data.get('username'),
                email=request.data.get('email'),
                full_name=request.data.get('fullname'),
            )
        user.set_password(str(request.data.get('password')))
        user.save()
        return Response({"status":"success","response":"User Successfully Created"}, status=status.HTTP_201_CREATED)
        


class MeView(APIView):
        
    def get(self, request):
        user = self.request.user
        if user.is_authenticated:
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        else:
            raise Http404
