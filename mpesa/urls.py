from django.urls import path
from .views import get_access_token_view, register_mpesa_urls_view, mpesa_payd_view, homepage

urlpatterns = [
    path("", homepage, name="homepage"),
    path("get-access-token/", get_access_token_view, name="get_access_token"),
    path("register-mpesa-urls/", register_mpesa_urls_view, name="register_mpesa_urls"),
    path("lipa-na-mpesa/", mpesa_payd_view, name="lipa_na_mpesa"),
]
