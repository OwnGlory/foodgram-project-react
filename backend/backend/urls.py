from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from favourite.views import FavouriteViewSet
from ingredients.views import IngredientsViewSet
from recipe.views import RecipeViewSet, TagViewSet
from shoppingList.views import ShoppingListViewSet
from subscribe.views import SubscribeViewSet
from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart',
                ShoppingListViewSet, basename='shoppinglist')
router.register(r'recipes/(?P<recipe_id>\d+)/favorite',
                FavouriteViewSet, basename='favorite')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/subscriptions/', SubscribeViewSet.as_view(
        {'get': 'list'}), name='subscriptions'),
    path('api/users/<int:pk>/subscribe/', SubscribeViewSet.as_view(
        {'post': 'subscribe', 'delete': 'subscribe'}
    ), name='subscribe'),
    path('api/recipes/download_shopping_cart/',
         ShoppingListViewSet.as_view({'get': 'list'}),
         name='download_shopping_cart'),
    path('api/users/me/', UserViewSet.as_view(
        {'get': 'users_own_profile'}), name='users_own_profile'),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include(router.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
