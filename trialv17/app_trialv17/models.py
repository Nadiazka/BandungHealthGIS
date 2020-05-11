from django.db.models import Q
from django.db import models
from django.contrib.gis.db import models

class AreaPuskesmas(models.Model):
    name = models.CharField(max_length=254)
    descriptio = models.CharField(max_length=254)
    timestamp = models.CharField(max_length=24)
    begin = models.CharField(max_length=24)
    end = models.CharField(max_length=24)
    altitudemo = models.CharField(max_length=254)
    tessellate = models.BigIntegerField()
    extrude = models.BigIntegerField()
    visibility = models.BigIntegerField()
    draworder = models.BigIntegerField()
    icon = models.CharField(max_length=254)
    layer = models.CharField(max_length=254)
    path = models.CharField(max_length=254)
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
    	return self.layer

class TitikPuskesmas(models.Model):
    no = models.BigIntegerField()
    puskesmas = models.CharField(max_length=254)
    x = models.FloatField()
    y = models.FloatField()
    geom = models.MultiPointField(srid=4326)

    def __str__(self):
    	return self.puskesmas

class filter(models.Manager):
	def filterWilayah(self, query=None):
		qs = self.get_queryset()
		if query is not None:
			or_lookup = (Q(kode__kode_pkm__nama_pkm__iexact=query) |
				Q(kode__kode_pkm__kecamatan__iexact=query))
			qs = qs.filter(or_lookup).values('kasus_baru', 'kasus_lama')
		return qs

	def filterPenyakit(self, query=None):
		qs = self.get_queryset()
		if query is not None:
			or_lookup = (Q(icd_10__nama_subkat__icontains=query) |
				Q(icd_10__kat__nama_kat__icontains=query) |
				Q(icd_10__kat__subchapter__nama_subchapter__icontains=query) |
				Q(icd_10__kat__subchapter__chapter__nama_chapter__icontains=query))
			qs = qs.filter(or_lookup).values('kasus_baru', 'kasus_lama')
		return qs

	def filterJenisKelamin(self, query=None):
		qs = self.get_queryset()
		if query is not None:
			qs = qs.filter(kat_pasien__jenis_kelamin__iexact=query).values('kasus_baru', 'kasus_lama')
		return qs
	#jangan lupa filter dibawah bisa pake range

	def filterUmur(self, query=None):
		qs = self.get_queryset()
		if query is not None:
			qs = qs.filter(kat_pasien__umur__icontains=query).values('kasus_baru', 'kasus_lama')
		return qs

	def filterPeriode(self, query=None):
		qs = self.get_queryset()
		if query is not None:
			qs = qs.filter(kode__tanggal__icontains=query).values('kasus_baru', 'kasus_lama')
		return qs

class Pasien(models.Model):
	"""docstring for Pasien"""
	kat_pasien = models.SmallAutoField( primary_key=True)
	umur = models.CharField(max_length=10)
	jenis_kelamin = models.CharField(max_length=10)

	def __str__(self):
		return '%s %s' % (self.umur, self.jenis_kelamin)

class Kecamatan(models.Model):
	kode_kec = models.CharField(max_length=10, primary_key=True)
	nama_kec = models.CharField(max_length=25)
	lat_kec = models.FloatField(null=True)
	longt_kec = models.FloatField(null=True)
	pddk_l = models.PositiveIntegerField()
	pddk_p = models.PositiveIntegerField()
	jml_pddk = models.IntegerField()

	def __str__(self):
		return self.nama_kec

class Puskesmas(models.Model):
	kode_pkm = models.CharField(max_length=13, primary_key=True)
	kode_kec = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
	nama_pkm = models.CharField(max_length=30)
	lat_pkm = models.FloatField(null=True)
	longt_pkm = models.FloatField(null=True)

	def __str__(self):
		return self.nama_pkm


class Indeks(models.Model):
	kode = models.SmallAutoField(primary_key=True)
	kode_pkm = models.ForeignKey(Puskesmas, on_delete=models.CASCADE)
	tanggal = models.DateField()
	deleted = models.SmallIntegerField()

	def __str__(self):
		return str(self.tanggal)

		
class ICD10_Chapter(models.Model):
	chapter = models.CharField(max_length=7, primary_key=True)
	nama_chapter = models.CharField(max_length=149)

	def __str__(self):
		return self.nama_chapter

class ICD10_Subchapter(models.Model):
	subchapter = models.CharField(max_length=9, primary_key=True)
	chapter = models.ForeignKey(ICD10_Chapter, on_delete=models.CASCADE)
	nama_subchapter = models.CharField(max_length=199)

	def __str__(self):
		return self.nama_subchapter

class ICD10_Kategori(models.Model):
	kat = models.CharField(max_length=5, primary_key=True)
	subchapter = models.ForeignKey(ICD10_Subchapter, on_delete=models.CASCADE)
	nama_kat = models.CharField(max_length=199)

	def __str__(self):
		return self.nama_kat
						
class ICD10_Subkategori(models.Model):
	subkat = models.CharField(max_length=9, primary_key=True)
	nama_subkat = models.CharField(max_length=100)
	kat = models.ForeignKey(ICD10_Kategori, on_delete=models.CASCADE)
	

	def __str__(self):
		return self.nama_subkat

class Jumlah_Kasus(models.Model):
	kode = models.ForeignKey(Indeks, on_delete=models.CASCADE)
	icd_10 = models.ForeignKey(ICD10_Subkategori, on_delete=models.CASCADE)
	jumlah_baru_l = models.PositiveSmallIntegerField()
	jumlah_baru_p = models.PositiveSmallIntegerField()
	jumlah_lama_l = models.PositiveSmallIntegerField()
	jumlah_lama_p = models.PositiveSmallIntegerField()
	jumlah = models.PositiveSmallIntegerField()
	gakin = models.PositiveSmallIntegerField()

	def __str__(self):
		return '%s %s' % (self.kode, self.icd_10)

class Kasus(models.Model):
	kode = models.ForeignKey(Indeks, on_delete=models.CASCADE)
	icd_10 = models.ForeignKey(ICD10_Subkategori, on_delete=models.CASCADE)
	kat_pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE)
	kasus_baru = models.PositiveSmallIntegerField()
	kasus_lama = models.PositiveSmallIntegerField()
	objects = filter()

	def __str__(self):
		return '%s %s' % (self.kasus_baru, self.kasus_lama)

class Jumlah_Kategori(models.Model):
	kode = models.ForeignKey(Indeks, on_delete=models.CASCADE)
	kat = models.ForeignKey(ICD10_Kategori, on_delete=models.CASCADE)
	jumlah_kat = models.PositiveIntegerField()

	def __str__(self):
		return '%s %s' % (self.kat, self.jumlah_kat)