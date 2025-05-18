from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from .models import JobseekerCV
from .serializers import AdminRegisterSerializer, AdminLoginSerializer, JobseekerCVSerializer


class AdminRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Admin registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobseekerCVView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        # List all CVs
        cv_entries = JobseekerCV.objects.all().order_by('-date_applied')
        serializer = JobseekerCVSerializer(cv_entries, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a new CV
        serializer = JobseekerCVSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'CV submitted successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobseekerCVDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        # Get CV by id
        try:
            cv = JobseekerCV.objects.get(pk=id)
        except JobseekerCV.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = JobseekerCVSerializer(cv)
        return Response(serializer.data)