from django.urls import path
# from rest_framework.routers import SimpleRouter
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views
# from pprint import pprint

router = routers.DefaultRouter()
router.register('products', views.ProductsViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
# pprint(router.urls)
# URLConf
# urlpatterns = [
#     path('products/', views.product_list),  for function based views
#     path('products/', views.ProductList.as_view()),   # for class based views
#     path('products/<int:id>/', views.product_detail),    for function based views
#     path('products/<int:pk>/', views.ProductDetail.as_view()),    # for class based views
#     path('collections/', views.collection_list),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
# ]

urlpatterns = router.urls + products_router.urls
