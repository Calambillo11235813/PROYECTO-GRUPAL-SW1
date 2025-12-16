from rest_framework.routers import DefaultRouter
from .views import VideoUploadViewSet, AnalysisResultViewSet

router = DefaultRouter()
router.register(r'videoupload', VideoUploadViewSet, basename='videoupload')
router.register(r'analysisresult', AnalysisResultViewSet, basename='analysisresult')

urlpatterns = router.urls
