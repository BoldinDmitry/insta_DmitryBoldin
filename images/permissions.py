from rest_framework import permissions


class CanEditOnlyItself(permissions.BasePermission):
    def __init__(self, allowed_methods):
        super().__init__()
        self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        username = view.kwargs.get("username")
        if username is not None:
            return request.user.username == username
        return False
