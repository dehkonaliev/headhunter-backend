from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and request.user == obj.user) \
        or request.method in SAFE_METHODS
        
        
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.user_role == "EMPLOYEE") \
        or request.method in SAFE_METHODS
        
class IsEmployeeStrict(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_role == "EMPLOYEE"
        
class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.user_role == "EMPLOYER") \
        or request.method in SAFE_METHODS