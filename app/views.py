# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import ContactForm
# from .serializers import ContactFormSerializer

# class SubmitContactForm(APIView):
#     def post(self, request, format=None):
#         serializer = ContactFormSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {
#                     'message': 'Form was submitted successfully!'
#                 },
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, format=None):
#         contacts = ContactForm.objects.all()
#         serializer = ContactFormSerializer(contacts, many=True)
#         return Response(serializer.data)
from django.shortcuts import render
def index(request):
    return render(request, 'index.html')

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ContactForm
from .serializers import ContactFormSerializer

class SubmitContactForm(APIView):
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



# views.py
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Donation
from .serializers import DonationSerializer
import razorpay

class DonationCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount'] * 100  # Razorpay amount is in paisa
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            
            razorpay_client = razorpay.Client(auth=("rzp_live_ZkV15pAiDqKCqq", "YOUR_RAZORPAY_KEY_SECRET"))
            payment_data = {
                'amount': amount,
                'currency': 'INR',
                'receipt': 'order_rcptid_11',
                'payment_capture': 1
            }
            payment = razorpay_client.order.create(data=payment_data)

            # Create the donation record in the database
            donation = Donation.objects.create(amount=serializer.validated_data['amount'],
                                                name=name,
                                                email=email,
                                                payment_id=payment['id'])

            # Send email notification
            subject = 'Thank You for Your Donation!'
            message = f"Dear {name},\n\nThank you for your generous donation of {amount} INR. Your support helps us make a difference in the lives of those in need.\n\nThank you again for your kindness and generosity!\n\nSincerely,\nYour Organization"
            send_mail(subject, message, 'your_from_email@example.com', [email])

            return Response({'payment_id': payment['id'], 'amount': amount}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # This is the endpoint where Razorpay will send the payment verification
        payment_id = request.query_params.get('payment_id')
        signature = request.query_params.get('signature')
        razorpay_client = razorpay.Client(auth=("rzp_live_ZkV15pAiDqKCqq", "YOUR_RAZORPAY_KEY_SECRET"))
        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,
            })
            donation = Donation.objects.get(payment_id=payment_id)
            donation.paid = True
            donation.save()

            # Send email notification
            subject = 'Thank You for Your Donation!'
            message = f"Dear {donation.name},\n\nThank you for your generous donation of {donation.amount} INR. Your support helps us make a difference in the lives of those in need.\n\nThank you again for your kindness and generosity!\n\nSincerely,\nYour Organization"
            send_mail(subject, message, 'your_from_email@example.com', [donation.email])

            return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
