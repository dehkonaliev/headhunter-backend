from rest_framework.permissions import BasePermission


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.user_role == "EMPLOYEE")


class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.user_role == "EMPLOYER")


class IsVacancyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        vacancy = getattr(obj, "vacancy", obj)
        return vacancy.company.owner == request.user