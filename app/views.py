
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ContactForm
from .serializers import ContactFormSerializer
from rest_framework.permissions import AllowAny

class SubmitContactForm(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            # Save the form data
            form_instance = serializer.save()
            # Get the email provided by the user in the form
            user_email = form_instance.email
            # Sending email notification to the user
            subject = 'Thank you for submitting the contact form'
            message = 'We have received your message and will get back to you soon.'
            from_email = 'tsaritservices@gmail.com'  # Update with your email
            send_mail(subject, message, from_email, [user_email])

            return Response(
                {
                    'message': 'Form was submitted successfully!'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        contacts = ContactForm.objects.all()
        serializer = ContactFormSerializer(contacts, many=True)
        return Response(serializer.data)


# count

# views.py
from django.http import JsonResponse
from .models import Visitor

def log_visit(request):
    ip_address = request.META.get('REMOTE_ADDR')
    Visitor.objects.create(ip_address=ip_address)
    return JsonResponse({'message': 'Visit logged'})

def get_visit_count(request):
    count = Visitor.objects.count()
    return JsonResponse({'visit_count': count})



