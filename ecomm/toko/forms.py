from django import forms
from .models import ProdukReview
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PILIHAN_PEMBAYARAN = (
    ('P', 'Paypal'),
    ('S', 'Stripe'),
)

PILIHAN_RATING = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

class CheckoutForm(forms.Form):
    alamat_1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Alamat Anda', 'class': 'textinput form-control'}))
    alamat_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Apartement, Rumah, atau yang lain (opsional)', 'class': 'textinput form-control'}))
    negara = CountryField(blank_label='(Pilih Negara)').formfield(widget=CountrySelectWidget(attrs={'class': 'countryselectwidget form-select'}))
    kode_pos = forms.CharField(widget=forms.TextInput(attrs={'class': 'textinput form-outline', 'placeholder': 'Kode Pos'}))
    simpan_info_alamat = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    opsi_pembayaran = forms.ChoiceField(widget=forms.RadioSelect(), choices=PILIHAN_PEMBAYARAN)

class ProdukReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=PILIHAN_RATING, widget=forms.Select(attrs={'class': 'star-rating'}))

    class Meta:
        model = ProdukReview
        fields = ("rating","nama", "komentar")
        widgets ={
            "nama" : forms.TextInput(attrs={"class": "col-sm-12"}),
            "komentar" : forms.Textarea(attrs={"class": "form-control"}),
        }
    
    