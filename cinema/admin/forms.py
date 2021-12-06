from django import forms
from user.forms import UserUpdateForm
from main.models import TopBanner, BackgroundImage, NewsBanner, BannersCarousel
from django.forms import modelformset_factory

from PIL import Image


# region User
class ExtendedUserUpdateForm(UserUpdateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        super().Meta.fields += ('is_staff', 'is_superuser')
# endregion User


# region Banners
class TopBannerForm(forms.ModelForm):

    def clean_image(self):
        image = self.cleaned_data['image']
        width, height = 1000, 190
        if Image.open(image).size != (width, height):
            raise forms.ValidationError(f'Выберите изображение с разрешением {width}x{height}')
        return image

    class Meta:
        model = TopBanner
        fields = ('image', 'is_active')
        widgets = {
            'image': forms.ClearableFileInput(attrs={"onchange": "validate_then_set_thumbnail(event)"})
        }


TopBannerFormSet = modelformset_factory(TopBannerForm.Meta.model, form=TopBannerForm,
                                        extra=0, can_delete=True)


class BackgroundImageForm(forms.ModelForm):
    is_active = forms.TypedChoiceField(
                   label='',
                   coerce=lambda x: x == 'True',
                   choices=((True, 'Изображение на фоне'), (False, 'Цвет на фоне')),
                   widget=forms.RadioSelect
                )

    def clean_image(self):
        image = self.cleaned_data['image']
        width, height = 2000, 3000
        if Image.open(image).size != (width, height):
            raise forms.ValidationError(f'Выберите изображение с разрешением {width}x{height}')
        return image

    class Meta:
        model = BackgroundImage
        fields = ('image', 'is_active')


class NewsBannerForm(forms.ModelForm):

    def clean_image(self):
        image = self.cleaned_data['image']
        width, height = 1000, 190
        if Image.open(image).size != (width, height):
            raise forms.ValidationError(f'Выберите изображение с разрешением {width}x{height}')
        return image

    class Meta:
        model = NewsBanner
        fields = ('image', 'is_active')
        labels = {
            'image': 'Новости | Акции',
        }


NewsBannerFormSet = modelformset_factory(NewsBannerForm.Meta.model, form=NewsBannerForm,
                                         extra=0, can_delete=True)


class BannersCarouselForm(forms.ModelForm):

    class Meta:
        model = BannersCarousel
        fields = ('is_active', 'data_interval')
        widgets = {
            'is_active': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',
            }),
            'data_interval': forms.Select(attrs={
                'class': 'form-control ml-4 mr-auto',
                'style': 'width: 64px;'
            }),
        }

# endregion Banners
