from django.conf.urls import url, include
from app_trialv17 import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.TitikPuskesmasView)

urlpatterns =[
	#url(r'^Pasien', views.pasienJSON, name="pasienJSON"),
	url(r'^$', views.index, name='index'),
	url(r'^PasienAPI/', views.PasienAPI.as_view()),
	url(r'^SearchView/', views.SearchView.as_view()),
	url(r'^PuskesmasView/', views.PuskesmasView.as_view()),
	url(r'^PuskesmasView2/', views.PuskesmasView.as_view(), name='PuskesmasView2'),
	url(r'^IndeksView/', views.IndeksView.as_view()),
	url(r'^titikpuskesmas/', include(router.urls), name='titikpuskesmas'),
]