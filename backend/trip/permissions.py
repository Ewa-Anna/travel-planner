from rest_framework import permissions


class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Permission to only allow organizers of a trip to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.organizer == request.user
