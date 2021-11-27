from django import forms
from user.forms import UserUpdateForm
from main.models import TopBanner, BackgroundImage, NewsBanner
from django.forms import modelformset_factory

from PIL import Image
from copy import copy


# region User
class ExtendedUserUpdateForm(UserUpdateForm):

    Meta = copy(UserUpdateForm.Meta)
    Meta.fields += ('is_staff', 'is_superuser')
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
        labels = {
            'image': 'Баннер',
            'is_active': 'Активен',
        }


TopBannerFormSet = modelformset_factory(TopBannerForm.Meta.model, form=TopBannerForm,
                                        extra=0, can_delete=True)


class BackgroundImageForm(forms.ModelForm):

    def clean_image(self):
        image = self.cleaned_data['image']
        width, height = 2000, 3000
        if Image.open(image).size != (width, height):
            raise forms.ValidationError(f'Выберите изображение с разрешением {width}x{height}')
        return image

    class Meta:
        model = BackgroundImage
        fields = ('image', 'is_active')
        labels = {
            'is_active': 'Картинка на фоне',
        }


BackgroundImageFormSet = modelformset_factory(BackgroundImageForm.Meta.model, form=BackgroundImageForm,
                                              extra=0, max_num=1, can_delete=True)


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
            'image': 'Баннер',
            'is_active': 'Активен',
        }


NewsBannerFormSet = modelformset_factory(NewsBannerForm.Meta.model, form=NewsBannerForm,
                                         extra=0, can_delete=True)
# endregion Banners
