from django.urls import path
from .views import home, about, services, impact, contact_us, get_involved, annual_reports, NewsListView, NewsDetailView

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('impact/', impact, name='impact'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('annual-reports/', annual_reports, name='annual_reports'),
    path('contact/', contact_us, name='contact_us'),
    path('get-involved/', get_involved, name='get_involved'),
]