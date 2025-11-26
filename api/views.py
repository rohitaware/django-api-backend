from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer, UserSerializer
from .pagination import StandardResultsSetPagination
from .permissions import IsOwner
from datetime import date, timedelta

class DashboardStatsView(APIView):
    """
    Provides statistics for the dashboard.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        total_users = User.objects.count()
        
        today = date.today()
        start_of_month = today.replace(day=1)
        
        today_messages = Message.objects.filter(date=today).count()
        month_messages = Message.objects.filter(date__gte=start_of_month).count()

        stats = {
            'totalUsers': total_users,
            'todayMessages': today_messages,
            'monthMessages': month_messages,
        }
        return Response(stats, status=status.HTTP_200_OK)

class UserDetailView(APIView):
    """
    Provides details for the currently authenticated user.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserListView(generics.ListAPIView):
    """
    Provides a list of all users.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination

class MessageListView(generics.ListCreateAPIView):
    """
    Lists and creates messages.
    List can be optionally filtered by a date range, with pagination.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Optionally restricts the returned messages to a given date range,
        by filtering against `from_date` and `to_date` query parameters.
        """
        queryset = Message.objects.all().order_by('-date')
        from_date = self.request.query_params.get('from_date', None)
        to_date = self.request.query_params.get('to_date', None)
        if from_date:
            queryset = queryset.filter(date__gte=from_date)
        if to_date:
            queryset = queryset.filter(date__lte=to_date)
        return queryset

    def perform_create(self, serializer):
        """
        Associates the message with the currently authenticated user upon creation.
        """
        serializer.save(user=self.request.user)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a message instance.
    Only the owner can update or delete.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer