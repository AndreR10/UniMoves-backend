from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    path('accommodations/', include('accommodation.urls')),
    path('features/', include('feature.urls')),
    path('rental-conditions/', include('rentalCondition.urls')),
    path('chats/', include('chat.urls')),
    path('messages/', include('message.urls')),
    path('leases/', include('lease.urls')),
    path('payments/', include('payment.urls')),
    path('receipts/', include('receipt.urls')),
]