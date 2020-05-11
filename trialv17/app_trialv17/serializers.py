from rest_framework import serializers
from django.core.serializers import serialize
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import *
"""
serialize('geojson', AreaPuskesmas.objects.all(),
          geometry_field='polygon',
          fields='__all__')
"""
class PasienSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = Pasien
 		fields = '__all__'

class PuskesmasSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = Puskesmas
 		fields = '__all__'

class IndeksSerializer(serializers.ModelSerializer):
	class Meta:
		model = Indeks
		fields = '__all__'
			
class TitikPuskesmasSerializer(GeoFeatureModelSerializer):
 	class Meta:
 		model = TitikPuskesmas
 		geo_field = "geom"
 		id_field = False
 		fields = '__all__'

class FilterAPISerializer(serializers.ModelSerializer):
	Pkm = PuskesmasSerializer(many=True, read_only=True)
	class Meta:
		model =  Indeks
		fields = ['kode','tanggal', 'kode_pkm', 'Pkm']
			
		
"""			
class IndeksSerializer(serializers.ModelSerializer):
 	class Meta:
 		models = Indeks
 		fields = '__all__'

class ICD10_SubchapterSerializer(serializers.ModelSerializer):
 	class Meta:
 		models = ICD10_Subchapter
 		fields = '__all__'

class ICD10_KategoriSerializer(serializers.ModelSerializer):
 	class Meta:
 		models = ICD10_Kategori
 		fields = '__all__'

class ICD10_SubkategoriSerializer(serializers.ModelSerializer):
 	class Meta:
 		models = ICD10_Subkategori
 		fields = '__all__'

class Jumlah_KasusSerializer(serializers.ModelSerializer):
 	class Meta:
 		models = Jumlah_Kasus
 		fields = '__all__'
"""