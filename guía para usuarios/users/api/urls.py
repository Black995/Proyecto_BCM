from rest_framework import routers
from users.api.views import GroupViewSet, PermissionViewSet, UserViewSet

app_name = 'users'

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', GroupViewSet)
router.register(r'permissions', PermissionViewSet)

urlpatterns = [
]

urlpatterns += router.urls
