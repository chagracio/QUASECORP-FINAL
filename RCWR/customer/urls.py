from django.urls import path
from customer import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('dashboard/', views.dashboard, name = "dashboard"),
    path('addRice/', views.addRice, name = "addRice"),
    path('customerHomepage/', views.CustomerHomepage, name = "Customer"),
    path('checkout/', views.Checkout, name = "checkout"),
    path('ricelist/', views.RiceList, name = "ricelist"),
    path('orders/', views.orders, name = "orders"),
    path('update_item/', views.updateItem, name = "update_item"),
    path('process_order/', views.processOrder, name = "process_order"),
    path('CustomerDashboard', views.CustomerDashboard, name = "CustomerDashboard"),
    path('contactUs/', views.Inquiry, name = "contactUs"),
    path('lendingStatus/', views.LendingStatus, name = "lendingStatus"),
    path('customerLendingStatus/', views.CustomerStatus, name = "customerLendingStatus"),
    path('delete/<int:id>', views.deleteRice, name = "deleteRice"),
    path('edit/<int:id>', views.updateRice, name = "updateRice"),
    path('update/<int:id>', views.UpdateOrderStatus, name = "updateOrderStatus"),
    path('updateStat/<int:id>', views.UpdateLendingStatus, name = "updateLendingStatus"),
]