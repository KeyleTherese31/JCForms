from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes
from .models import JobseekerCV, Test
from .serializers import AdminRegisterSerializer, AdminLoginSerializer, JobseekerCVSerializer, TestSerializer, BulkTestUploadSerializer

# ✅ Import your AdminUser model
from .models import AdminUser


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
            
            # ✅ Override role if superuser
            role = 'superadmin' if user.is_superuser else user.role

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'role': user.actual_role
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


@api_view(['POST'])
@permission_classes([AllowAny])
def mobile_login(request):
    """
    Checks if the submitted mobile number exists in the contact_no field of JobseekerCV.
    """
    mobile = request.data.get('mobile')
    
    if not mobile:
        return Response({'error': 'Mobile number is required'}, status=status.HTTP_400_BAD_REQUEST)

    exists = JobseekerCV.objects.filter(contact_no=mobile).exists()

    return Response({'exists': exists}, status=status.HTTP_200_OK)


class BulkTestUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BulkTestUploadSerializer(data={'questions': request.data.getlist('questions')})
        
        # For non-File inputs sent as key=value strings
        if not serializer.is_valid():
            # Try to build question objects from multi-part data
            questions = []
            i = 0
            while f'questions[{i}][test_category]' in request.data:
                question = {
                    'category': request.data.get(f'questions[{i}][test_category]'),
                    'question_type': request.data.get(f'questions[{i}][question_type]'),
                    'question_format': request.data.get(f'questions[{i}][question_format]'),
                    'has_answer_key': request.data.get(f'questions[{i}][has_answer_key]') == 'true',
                    'answer_key': request.data.get(f'questions[{i}][answer_key]'),
                    'question_text': request.data.get(f'questions[{i}][question_text]', ''),
                    'choices': request.data.get(f'questions[{i}][choices]', '[]'),
                    'question_image': request.FILES.get(f'questions[{i}][question_image]')
                }
                questions.append(question)
                i += 1
            serializer = BulkTestUploadSerializer(data={'questions': questions})
            serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({"message": "Questions created successfully!"}, status=status.HTTP_201_CREATED)


class TestListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        category = request.query_params.get('category')
        if category:
            tests = Test.objects.filter(category=category).order_by('id')
        else:
            tests = Test.objects.all().order_by('id')
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)