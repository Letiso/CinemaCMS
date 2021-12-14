from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from user.forms import UserUpdateForm
from main.models import TopBanner, BackgroundImage, NewsBanner, BannersCarousel, MovieCard, MovieFrame, SEO
from django.forms import modelformset_factory


# region User
class ExtendedUserUpdateForm(UserUpdateForm):
    UserUpdateForm.Meta.fields += ('is_staff', 'is_superuser')


# endregion User


# region Banners
def clean_image(form):
    image, required_size = form.cleaned_data['image'], form.Meta.model.required_size

    if isinstance(image, InMemoryUploadedFile):
        image_size = image.image.size
    else:
        image_size = (image.width, image.height)

    if image_size != required_size:
        width, height = required_size
        raise forms.ValidationError(f'Выберите изображение с разрешением {width}x{height}', code='invalid')
    return image


class TopBannerForm(forms.ModelForm):
    def clean_image(self):
        return clean_image(self)

    class Meta:
        model = TopBanner
        fields = ('image', 'is_active')


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
        return clean_image(self)

    class Meta:
        model = BackgroundImage
        fields = ('image', 'is_active')


class NewsBannerForm(forms.ModelForm):
    def clean_image(self):
        return clean_image(self)

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


# region Movies
class MovieCardForm(forms.ModelForm):
    def clean_movie_type(self):
        return self.cleaned_data['movie_type'][0]

    class Meta:
        model = MovieCard
        exclude = ('seo', )

    movie_type = forms.MultipleChoiceField(
        choices=Meta.model.TYPES,
        widget=forms.CheckboxSelectMultiple(),
    )


class MovieFrameForm(forms.ModelForm):
    def clean_image(self):
        return clean_image(self)

    class Meta:
        model = MovieFrame
        exclude = ('movie',)


MovieFrameFormset = modelformset_factory(MovieFrameForm.Meta.model, form=MovieFrameForm,
                                         extra=0, can_delete=True)


# endregion Movies

# region SEO
class SEOForm(forms.ModelForm):
    class Meta:
        model = SEO
        fields = '__all__'


# endregion SEO
