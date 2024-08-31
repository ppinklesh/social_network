from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from django.db.models import Q
from rest_framework.exceptions import ValidationError

class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer

class LoginView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        return User.objects.filter(
            Q(email__iexact=query) | Q(name__icontains=query)
        ).exclude(id=self.request.user.id)[:10]

class FriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            formatted_errors = {}
            for field, messages in errors.items():
                formatted_errors[field] = [str(message) for message in messages]
            return Response(formatted_errors, status=status.HTTP_400_BAD_REQUEST)

        from_user = request.user
        to_user = serializer.validated_data.get('to_user')

        # Check if a friend request already exists
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({'error': 'Friend request already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the new friend request
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

        
class AcceptRejectFriendRequestView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)

    def patch(self, request, *args, **kwargs):
        # Retrieve the specific friend request
        try:
            friend_request = self.get_object()
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

        # Validate and update the `is_accepted` field
        is_accepted = request.data.get('is_accepted')
        if is_accepted is None:
            return Response({"error": "is_accepted field is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure that `is_accepted` is a boolean
        if is_accepted.lower() not in ['true', 'false']:
            return Response({"error": "Invalid value for is_accepted"}, status=status.HTTP_400_BAD_REQUEST)

        # Update friend request status
        friend_request.is_accepted = is_accepted.lower() == 'true'
        friend_request.save()

        serializer = self.get_serializer(friend_request)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(sent_requests__to_user=self.request.user, sent_requests__is_accepted=True)

class ListPendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, is_accepted=False)
