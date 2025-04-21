import pytest
from users.permissions import IsAdmin

@pytest.mark.django_db
class TestPermissions:
    def test_is_admin_permission_admin_user(self, admin_user):
        permission = IsAdmin()
        request = type('Request', (), {'user': admin_user})()
        view = type('View', (), {})()
        
        assert permission.has_permission(request, view) is True
    
    def test_is_admin_permission_regular_user(self, regular_user):
        permission = IsAdmin()
        request = type('Request', (), {'user': regular_user})()
        view = type('View', (), {})()
        
        assert permission.has_permission(request, view) is False
    
    def test_is_admin_permission_unauthenticated(self):
        permission = IsAdmin()
        # Create a request with no user
        request = type('Request', (), {'user': None})()
        view = type('View', (), {})()
        
        # The permission should return False for unauthenticated users
        result = permission.has_permission(request, view)
        assert result is False 