from rest_framework import routers

from .viewsets import ExpenseViewSet

app_name = "expense"

router = routers.DefaultRouter()
router.register(r"expense", ExpenseViewSet)

urlpatterns = []

urlpatterns += router.urls
