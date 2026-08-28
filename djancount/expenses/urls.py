from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, ExpenseViewSet, event_detail_view, homepage_view

# ==============================================================================
# 🔀 ROUTAGE API REST (Membre 2)
# ==============================================================================

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'expenses', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('event/<int:event_id>/', event_detail_view, name='event_detail'),
    path('api/', include(router.urls)),
]
