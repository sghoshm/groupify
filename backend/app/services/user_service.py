# backend/app/services/user_service.py
from supabase import Client
from postgrest.base_request_builder import APIResponse # Import for type hinting Supabase responses

class UserService:
    """Service class for handling user-related logic with Supabase."""
    def __init__(self, supabase_client: Client):
        self.supabase_client = supabase_client

    def create_user_profile(self, user_id: str, username: str | None = None) -> APIResponse:
        """
        Creates a new entry in the 'profiles' table for a newly authenticated user.
        This should typically be called after a successful user signup.
        """
        # Insert a row into the profiles table with the user's ID
        # The 'id' column in 'profiles' has a default of auth.uid(), but explicitly
        # setting it here ensures it matches the user created by auth.signup
        # You might add username here if collected during signup
        data_to_insert = {"id": user_id}
        if username:
            data_to_insert["username"] = username

        # The RLS policy for INSERT on 'profiles' should allow the user to create their own profile (auth.uid() = id)
        # This call inserts the data into the 'profiles' table
        response = self.supabase_client.from_("profiles").insert(data_to_insert).execute()
        return response


    def get_user_profile(self, user_id: str) -> APIResponse:
        """
        Fetches a user's profile from the 'profiles' table by their ID.
        The RLS policy for SELECT on 'profiles' will determine if the requesting
        user is allowed to view this profile.
        """
        # Select all columns from the profiles table where the id matches
        response = self.supabase_client.from_("profiles").select("*").eq("id", user_id).execute()
        return response

    # Add other user-related methods as needed (e.g., update profile, get user list)
    # def update_user_profile(self, user_id: str, profile_data: dict) -> APIResponse:
    #     # The RLS policy for UPDATE on 'profiles' should allow the user to update their own profile (auth.uid() = id)
    #     return self.supabase_client.from_("profiles").update(profile_data).eq("id", user_id).execute()

    # def get_all_profiles(self) -> APIResponse:
    #     # Be careful with RLS here - you likely don't want everyone to see all profiles
    #     return self.supabase_client.from_("profiles").select("*").execute()
