from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, ExpenseViewSet

# ==============================================================================
# 🔀 ROUTAGE API REST (Membre 2)
# ==============================================================================

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'expenses', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('api/', include(router.urls)),
]
