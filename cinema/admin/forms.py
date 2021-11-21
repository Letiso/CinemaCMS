from django import forms
from user.forms import UserUpdateForm
from main.models import TopBanner, BackgroundImage

from copy import copy


# region User
class ExtendedUserUpdateForm(UserUpdateForm):

    Meta = copy(UserUpdateForm.Meta)
    Meta.fields += ('is_staff', 'is_superuser')
# endregion User


# region Banners
# class TopBannerForm(forms.ModelForm):
#
#     class Meta:
#         model = TopBanner
#         fields = ('image', 'is_active')
#         labels = {
#             'image': 'Баннер',
#             'is_active': 'Вкл/Выкл.',
#         }
#         widgets = {}


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
            'image': 'Баннер',
            'is_active': 'Вкл/Выкл.',
        }
# endregion Banners
