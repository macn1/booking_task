from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Booking,FitnessClass
from .seriallizer import FitnessClassSerializer,BookingSerializer
import pytz
import logging

logger = logging.getLogger(__name__)


class FitnessClassListView(APIView):
    def get(self, request):
        try:
            queryset = FitnessClass.objects.filter(date_time__gt=timezone.now())
            tz = request.query_params.get('timezone')
            if tz:
                for obj in queryset:
                    obj.date_time = obj.convert_timezone(tz)
            
            serializer = FitnessClassSerializer(queryset.order_by('date_time'), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching classes: {e}")
            return Response(
                {"error": "An error occurred while fetching classes"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CreateBookingView(APIView):

    def post(self, request):
        try:
            serializer = BookingSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            fitness_class = serializer.validated_data['fitness_class']
            if fitness_class.available_slots <= 0:
                return Response(
                    {"error": "No available slots for this class"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if Booking.objects.filter(
                fitness_class=fitness_class,
                client_email=serializer.validated_data['client_email']
            ).exists():
                return Response(
                    {"error": "You have already booked this class"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            fitness_class.available_slots -= 1
            fitness_class.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f"Error creating booking: {e}")
            return Response(
                {"error": "An error occurred while processing your booking"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class ClientBookingsView(APIView):
    def get(self, request):
        try:
            email = request.query_params.get('email')
            
            if not email:
                return Response(
                    {"error": "Email parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            bookings = Booking.objects.filter(
                client_email=email,
                fitness_class__date_time__gt=timezone.now()
            ).order_by('fitness_class__date_time')
            
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error fetching bookings: {e}")
            return Response(
                {"error": "An error occurred while fetching bookings"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )