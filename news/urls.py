from django.urls import path
from .views import dashboard, filteredDashboard, loginUser, logoutUser, searchDashboard

urlpatterns = [
    # path('login', loginUser, name="login"),
    path('dashboard/<int:pk>/', dashboard, name='notification-dashboard'),
    # path('logout', logoutUser, name="logout"),
    path('search_dashboard', searchDashboard, name="search_dashboard"),
    path('news-websites/<str:website>/<int:pk>/', filteredDashboard, name='filtered_dashboard')
]
