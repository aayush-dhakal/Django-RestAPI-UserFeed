from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""

        # if the http method is GET(ie safe method coz it doesnot alter the model objects) then we allow the user to view other users profile
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id  # returns True(if True is returned then the access is allowed) if id matches(ie the id of the user profile and the user itself) else False(which won't allow access)


class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id     