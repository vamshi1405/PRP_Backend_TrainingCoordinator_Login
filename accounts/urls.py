from django.urls import path

from .views import (
    TrainingCoordinatorLoginAPIView,
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
)

urlpatterns = [

    path(
        "training-coordinator/login/",
        TrainingCoordinatorLoginAPIView.as_view(),
    ),

    path(
        "training-coordinator/forgot-password/",
        ForgotPasswordAPIView.as_view(),
    ),

    path(
        "training-coordinator/reset-password/",
        ResetPasswordAPIView.as_view(),
    ),
]