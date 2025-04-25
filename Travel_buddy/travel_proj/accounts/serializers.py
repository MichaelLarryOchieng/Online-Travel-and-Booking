# accounts/serializers.py
# from django.contrib.auth.models import User # Don't import default User
from django.contrib.auth import get_user_model
from rest_framework import serializers
# --- Import Djoser's base serializer ---
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
# --- End Import ---

User = get_user_model() # Gets your CustomUser model

# --- This is the serializer Djoser needs for user creation ---
class CustomUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        # Add your custom fields (phone_number) and standard fields you want handled
        fields = ('id', 'username', 'email', 'password',
                  'first_name', 'last_name', 'phone_number')
# --- End Djoser Create Serializer ---


# --- Keep your existing UserSerializer if used elsewhere (e.g., for retrieving user details) ---
# You might want to rename it for clarity if it's not for creation, e.g., CustomUserDetailSerializer
class UserSerializer(serializers.ModelSerializer):
    # If this is for RETRIEVING user details, password should likely be read_only or excluded
    # password = serializers.CharField(write_only=True) # Keep if this IS used for updates

    class Meta:
        model = User
        # Define fields appropriate for retrieving/updating user details (exclude password if read-only)
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number')
        read_only_fields = ('id', 'email', 'username') # Example: Make some fields read-only

    # Remove the create method if this serializer isn't used for creation
    # def create(self, validated_data):
    #     # ... (create logic - Djoser handles this via UserCreateSerializer now) ...
    #     pass

# --- Keep your LoginSerializer ---
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

