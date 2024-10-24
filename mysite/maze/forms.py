from django import forms
from .models import ServiceProvider, ServiceProviderImage

# Form for ServiceProvider (excluding images)
class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ['name', 'description', 'contact_info']

# Form for ServiceProviderImage
class ServiceProviderImageForm(forms.ModelForm):
    class Meta:
        model = ServiceProviderImage
        fields = ['image']

# Formset for multiple images
ServiceProviderImageFormSet = forms.inlineformset_factory(
    ServiceProvider, 
    ServiceProviderImage, 
    form=ServiceProviderImageForm, 
    extra=3,  # Allowing up to 3 images
    max_num=3
)



class ContactForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    phone_number = forms.CharField(label='Phone Number', max_length=15, required=True)
    message = forms.CharField(label='Message', widget=forms.Textarea, required=True)



from django import forms
from .models import Service, Category, SubCategory

class ServiceForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label="Category",
        widget=forms.Select(attrs={'id': 'id_category'})
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.none(),
        required=True,
        label="SubCategory",
        widget=forms.Select(attrs={'id': 'id_subcategory'})
    )

    class Meta:
        model = Service
        fields = ['title', 'description', 'category', 'subcategory', 'file', 'image']

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['subcategory'].queryset = SubCategory.objects.none()
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.subcategory.category.subcategories.order_by('name')
        else:
            self.fields['subcategory'].queryset = SubCategory.objects.none()


class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={'placeholder': 'Search services...', 'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Category',
        widget=forms.Select(attrs={'id': 'search_category', 'class': 'form-control'})
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.none(),
        required=False,
        label='SubCategory',
        widget=forms.Select(attrs={'id': 'search_subcategory', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['subcategory'].queryset = SubCategory.objects.none()
        elif self.initial.get('category'):
            category_id = self.initial.get('category').id
            self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
        else:
            self.fields['subcategory'].queryset = SubCategory.objects.none()

