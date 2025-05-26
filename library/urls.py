from django.urls import path, include

urlpatterns = [
    path('auth/', include('library.routes.auth_urls')),
    path('users/', include('library.routes.user_urls')),
    path('books/', include('library.routes.book_urls')),
    path('loans/', include('library.routes.loan_urls')),
    path('', include('library.routes.password_urls')),  
]
