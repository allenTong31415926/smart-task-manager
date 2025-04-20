from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsTaskAssigneeOrProjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.assigned_to == request.user or
            (hasattr(obj, 'project') and obj.project.owner == request.user)
        )
