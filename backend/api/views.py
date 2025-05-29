from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes
from .models import JobseekerCV, Question, Choice, TestSubmission
from .serializers import AdminRegisterSerializer, AdminLoginSerializer, JobseekerCVSerializer, QuestionSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import RetrieveUpdateDestroyAPIView


# ✅ Import your AdminUser model
from .models import AdminUser
import json

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
    mobile = request.data.get('mobile')
    
    if not mobile:
        return Response({'error': 'Mobile number is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        jobseeker = JobseekerCV.objects.get(contact_no=mobile)
        full_name = f"{jobseeker.first_name} {jobseeker.middle_name} {jobseeker.last_name}".strip()
        # Remove extra spaces if middle_name is empty:
        full_name = ' '.join(full_name.split())

        return Response({
            'exists': True,
            'id': jobseeker.id,
            'full_name': full_name,
        }, status=status.HTTP_200_OK)
    except JobseekerCV.DoesNotExist:
        return Response({'exists': False}, status=status.HTTP_200_OK)
    except Exception as e:
        print("ERROR in mobile_login:", e)
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import json

class BulkQuestionCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        index = 0
        saved_count = 0

        while f'questions[{index}][question_text]' in request.POST or f'questions[{index}][question_image]' in request.FILES:
            question_data = {
                'test_category': request.POST.get(f'questions[{index}][test_category]'),
                'question_type': request.POST.get(f'questions[{index}][question_type]'),
                'question_text': request.POST.get(f'questions[{index}][question_text]', ''),
                'question_format': request.POST.get(f'questions[{index}][question_format]'),
                'has_answer_key': request.POST.get(f'questions[{index}][has_answer_key]') == 'true',
                'answer_key': request.POST.get(f'questions[{index}][answer_key]', ''),
                'question_image': request.FILES.get(f'questions[{index}][question_image]'),
            }

            # Save the question
            question = Question.objects.create(**question_data)

            # Save the choices (if any)
            choices_json = request.POST.get(f'questions[{index}][choices]')
            if choices_json:
                try:
                    choices = json.loads(choices_json)
                    for choice in choices:
                        Choice.objects.create(
                            question=question,
                            text=choice.get('text', ''),
                            is_correct=choice.get('is_correct', False)
                        )
                except json.JSONDecodeError:
                    return Response({'error': f'Invalid choices JSON at index {index}'}, status=400)

            saved_count += 1
            index += 1

        return Response({'message': f'{saved_count} questions saved successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def questions_by_category(request, category):
    questions = Question.objects.filter(test_category=category)
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

class QuestionDetailView(APIView):

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return None

    def get(self, request, pk):
        question = self.get_object(pk)
        if question is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk):
        question = self.get_object(pk)
        if question is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SubmitTestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Received POST data:", request.data)  # DEBUG
        data = request.data
        jobseeker_id = data.get('jobseeker_id')
        answers = data.get('answers', [])

        if not jobseeker_id or not answers:
            print("Missing jobseeker_id or answers")
            return Response({"error": "jobseeker_id and answers are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            jobseeker = JobseekerCV.objects.get(id=jobseeker_id)
        except JobseekerCV.DoesNotExist:
            print(f"Jobseeker {jobseeker_id} not found")
            return Response({"error": "Jobseeker not found"}, status=status.HTTP_404_NOT_FOUND)

        created_submissions = []

        for ans in answers:
            question_id = ans.get('question_id')
            submitted_answer = ans.get('answer')

            if not question_id or submitted_answer is None:
                print(f"Skipping invalid answer: {ans}")
                continue  # skip invalid
            
            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                print(f"Question {question_id} not found, skipping")
                continue  # skip invalid

            submission, created = TestSubmission.objects.update_or_create(
                jobseeker=jobseeker,
                question=question,
                defaults={'submitted_answer': submitted_answer}
            )
            print(f"Submission saved: {submission.id}")
            created_submissions.append(submission.id)

        return Response({"message": "Submissions saved", "submission_ids": created_submissions}, status=status.HTTP_201_CREATED)

    
