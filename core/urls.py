from django.urls import path
from django.views.generic import TemplateView

from . import views
from .views import subscribe_newsletter

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/', views.rooms, name='rooms'),
    path('gallery/', views.gallery, name='gallery'),
    path('amenities/', views.amenities, name='amenities'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('thank-you/', TemplateView.as_view(template_name='thank-you.html'), name='thank_you'),
    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
    path('newsletter-thank-you/', views.newsletter_thank_you, name='newsletter_thank_you'),


]
