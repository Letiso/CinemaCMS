from django import forms
from user.forms import UserUpdateForm
from main.models import TopBanner, BackgroundImage, NewsBanner
from django.forms import modelformset_factory

from copy import copy


# region User
class ExtendedUserUpdateForm(UserUpdateForm):

    Meta = copy(UserUpdateForm.Meta)
    Meta.fields += ('is_staff', 'is_superuser')
# endregion User


# region Banners
class TopBannerForm(forms.ModelForm):

    class Meta:
        model = TopBanner
        fields = ('image', 'is_active')
        labels = {
            'image': 'Баннер',
            'is_active': 'Вкл/Выкл.',
        }
        widgets = {}


TopBannerFormSet = modelformset_factory(TopBanner, form=TopBannerForm, extra=1)


class BackgroundImageForm(forms.ModelForm):

    def clean_image(self):
        image = self.cleaned_data['image']
        width, height = '1000', '190'
        # if image.image.size != (width, height):
        #     raise forms.ValidationError(f'Выберите изображение с разрешением {width}x{height}')
        return image

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = BackgroundImage
        fields = ('image', 'is_active')
        labels = {
            'is_active': 'Картинка на фоне',
        }


BackgroundImageFormSet = modelformset_factory(BackgroundImage, form=BackgroundImageForm, extra=1, max_num=1)


class NewsBannerForm(forms.ModelForm):

    class Meta:
        model = TopBanner
        fields = ('image', 'is_active')
        labels = {
            'image': 'Баннер',
            'is_active': 'Вкл/Выкл.',
        }
        widgets = {}


NewsBannerFormSet = modelformset_factory(NewsBanner, form=NewsBannerForm, extra=1)
# endregion Banners
