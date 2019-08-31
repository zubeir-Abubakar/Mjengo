from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import *
from .serializers import *
from django.core.mail import send_mail

from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions



def home(request):
    return render(request, 'home.html')


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        a_project = Project.objects.create(
            project_name=request.data["project_name"],
            contractor_email=request.data["contractor_email"],
            description=request.data["description"],
            user=request.user,
            developer_email = request.user.email,
        )
        project_name=request.data["project_name"]
        description=request.data["description"]
        user=request.user    
        developer_email = request.user.email
        email=request.data["contractor_email"]
        send_mail(
            'MJENZI',
            'Hello,'
            'There is a new project request and a post . Login into your account with your credantials to see the post ',
            'Cheers!'
            'Innovex group of companies'
            "{EMAIL_HOST_USER}",
            ['{email}'.format(email=email)],
            fail_silently=False,
        )
        return Response(
            data=ProjectSerializer(a_project).data,
            status=status.HTTP_201_CREATED
        )

class ProjectDetail(generics.RetrieveDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs["pk"])
        if not request.user == project.user:
            raise PermissionDenied("You can not delete this project.")
        return super().destroy(request, *args, **kwargs)


class MaterialList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Materials.objects.filter(project_id=self.kwargs["pk"])
        return queryset

    serializer_class = MaterialsSerializer


class ReportList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Reports.objects.filter(project_id=self.kwargs["pk"])
        return queryset

    serializer_class = ReportSerializer

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs["pk"])
        if not request.user == project.user:
            raise PermissionDenied("You can not create reports for this project.")
        return super().post(request, *args, **kwargs)


class RequestList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Requests.objects.filter(project_id=self.kwargs["pk"])
        return queryset

    serializer_class = RequestSerializer

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs["pk"])
        if not request.user == project.user:
            raise PermissionDenied("You can not create requests for this project.")
        return super().post(request, *args, **kwargs)


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

    """
    POST auth/register/
    """

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        password2 = request.data.get("password2", "")
        email = request.data.get("email", "")
        if not username and not password and not email and not password2:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if password != password2:
            return Response(
                data={
                    "message": "Passwords don't match"
                },      
                developer_email = request.user.email("developer_email"),
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        send_mail(
            'MJENZI',
            'Congratulations you have been succesfully registered. Welcome to Mjenzi App.',
            'cheers!, '
            'Innovex groups of companies'
            "{EMAIL_HOST_USER}",
            ['{email}'.format(email=email)],
            fail_silently=False,
        )
        Token.objects.create(user=new_user)
        return Response(
            data=UserSerializer(new_user).data, status=status.HTTP_201_CREATED
        )



class LoginView(APIView):
    permission_classes = ()

    def post(self, request, ):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
