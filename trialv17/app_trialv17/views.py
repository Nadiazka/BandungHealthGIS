from django.db.models import Q
from itertools import chain
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework import filters
from django.shortcuts import render
from django.views.generic import View, ListView
from .models import *
from django.contrib.auth.decorators import login_required
from .serializers import *


class TitikPuskesmasView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
	serializer_class = TitikPuskesmasSerializer
	queryset = TitikPuskesmas.objects.all()
		
# Create your views here.
@login_required(login_url='login')
def index(request):
	objPasien = Pasien.objects.all()#order_by('kat_pasien')
	objPuskesmas = Puskesmas.objects.all() #order_by('kode_pkm')
	objIndeks = Indeks.objects.all() #order_by('kode')
	objICD10_Chapter = ICD10_Chapter.objects.all() #order_by('chapter')
	objICD10_Subchapter = ICD10_Subchapter.objects.all() #order_by('subchapter')
	objICD10_Kategori = ICD10_Kategori.objects.all() #order_by('kat')
	objICD10_Subkategori = ICD10_Subkategori.objects.all() #order_by('subkat')
	objKasus = Kasus.objects.all() #order_by('kode')
	objJumlah_Kasus = Jumlah_Kasus.objects.all() #order_by('kode')

	context = {
		'objPasien': objPasien,
		'objPuskesmas': objPuskesmas,
		'objIndeks': objIndeks,
		'objICD10_Chapter': objICD10_Chapter,
		'objICD10_Subchapter': objICD10_Subchapter,
		'objICD10_Kategori': objICD10_Kategori,
		'objICD10_Subkategori': objICD10_Subkategori,
		'objKasus': objKasus,
		'objJumlah_Kasus': objJumlah_Kasus
	}
	return render (request, 'app_trialv17/indexV2.html', context)


def get_data(request):
	data = {
			"male_data" : [23,30,21,26,24,13],
			"female_data" : [13,10,8,3,7,12],
			"label_data": ['13-17', '18-24', '25-34', '35-44','45-54','55-64']
			}
	return JsonResponse(data)

"""
class pasienJSON(viewsets.ModelViewSet):
	objPasien = Pasien.objects.all()
	jsonPasien = PasienSerializer
"""
#class DataKasus(generics.ListCreateAPIView):
	

class SearchView(ListView):
	template_name = 'app_trialv12/tesdatav1.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['query'] = self.request.GET.get('q')
		return context

	def get_queryset(self):
		request = self.request
		query = request.GET.get('q', None)

		if query is not None:
			wilayah_results     	= Kasus.objects.filterWilayah(query)
			penyakit_results     	= Kasus.objects.filterPenyakit(query)
			jeniskelamin_results    = Kasus.objects.filterJenisKelamin(query)
			umur_results     		= Kasus.objects.filterUmur(query)
			periode_results     	= Kasus.objects.filterPeriode(query)

			queryset_chain = chain(
			        wilayah_results,
			        penyakit_results,
			        jeniskelamin_results,
			        umur_results,
			        periode_results)

			qs = sorted(queryset_chain, reverse=True)
			self.count = len(qs) # since qs is actually a list
			return qs
		return Kasus.objects.none() # just an empty queryset as default

def getWilayah(request):
	dataWilayah = Kasus.objects.filterWilayah(request)
	return render (request, 'app_trialv17/tesdatav1.html', {'dataWilayah':dataWilayah})

class PasienAPI(APIView):
	def get(self, request):
		pasiens = Pasien.objects.all()
		serializer = PasienSerializer(pasiens, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = PasienSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PuskesmasView(generics.ListAPIView):
	queryset = Puskesmas.objects.all()
	serializer_class = PuskesmasSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['nama_pkm']

class IndeksView(generics.ListCreateAPIView):
	serializer_class = IndeksSerializer
	#pagination_class = 10

	def get_queryset(self, *args, **kwargs):
		queryset_list = Indeks.objects.all()
		query = self.request.GET.get("filter")
		if query:
			queryset_list = queryset_list.filter(
				Q(kode__icontains=query)|
				Q(tanggal__icontains=query)
				)
		return queryset_list

class PuskesmasView2(generics.ListCreateAPIView):
	serializer_class = PuskesmasSerializer

	def get_queryset(self, *args, **kwargs):
		queryset_list = Indeks.objects.all()
		query = self.request.POST.get("q")
		if query:
			

			
			queryset_list = queryset_list.filter(nama_pkm__icontains=query)
		return queryset_list
		