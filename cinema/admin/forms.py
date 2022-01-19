import json

from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from user.forms import UserUpdateForm
from main.models import *
from django.forms import modelformset_factory

from django.template.loader import render_to_string
from django.utils.html import strip_tags


# region Additional
class DateInput(forms.DateInput):
    def __init__(self, *args, **kwargs):
        super(DateInput, self).__init__(*args, format='%Y-%m-%d', **kwargs)

    input_type = 'date'


class ImageValidationMixin:
    cleaned_data = Meta = None

    def clean_image(self):
        image, required_size = self.cleaned_data['image'], self.Meta.model.required_size

        if isinstance(image, InMemoryUploadedFile):
            image_size = image.image.size
        else:
            image_size = (image.width, image.height)

        if image_size != required_size:
            width, height = required_size
            raise forms.ValidationError(f'Выберите изображение с разрешением {width}x{height}', code='invalid')
        return image


# endregion Additional

# region User
class ExtendedUserUpdateForm(UserUpdateForm):
    UserUpdateForm.Meta.fields += ('is_staff', 'is_superuser')


# endregion User


# region Banners
class TopBannerForm(ImageValidationMixin, forms.ModelForm):
    class Meta:
        model = TopBanner
        fields = ('image', 'is_active')


TopBannerFormSet = modelformset_factory(TopBannerForm.Meta.model, form=TopBannerForm,
                                        extra=0, can_delete=True)


class BackgroundImageForm(ImageValidationMixin, forms.ModelForm):
    is_active = forms.TypedChoiceField(
        label='',
        coerce=lambda x: x == 'True',
        choices=((True, 'Изображение на фоне'), (False, 'Цвет на фоне')),
        widget=forms.RadioSelect
    )

    class Meta:
        model = BackgroundImage
        fields = ('image', 'is_active')


class NewsBannerForm(ImageValidationMixin, forms.ModelForm):
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
        exclude = ('date_created', 'seo')
        widgets = {
            'release_date': DateInput(),
        }

    movie_type = forms.MultipleChoiceField(
        label='Тип кино',
        choices=Meta.model.TYPES,
        widget=forms.CheckboxSelectMultiple(),
    )


class MovieFrameForm(ImageValidationMixin, forms.ModelForm):
    class Meta:
        model = MovieFrame
        exclude = ('card',)


MovieFrameFormset = modelformset_factory(MovieFrameForm.Meta.model, form=MovieFrameForm,
                                         extra=0, can_delete=True)


# endregion Movies

# region News
class NewsCardForm(ImageValidationMixin, forms.ModelForm):
    class Meta:
        model = NewsCard
        exclude = ('date_created',)
        widgets = {
            'is_active': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',
            }),
            'publication_date': DateInput(),

        }


class NewsGalleryForm(ImageValidationMixin, forms.ModelForm):
    class Meta:
        model = NewsGallery
        exclude = ('news',)


NewsGalleryFormset = modelformset_factory(NewsGalleryForm.Meta.model, form=NewsGalleryForm,
                                          extra=0, can_delete=True)


# endregion News

# region Promotion
class PromotionCardForm(ImageValidationMixin, forms.ModelForm):
    class Meta:
        model = PromotionCard
        exclude = ('date_created',)
        widgets = {
            'is_active': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',
            }),
            'publication_date': DateInput(),

        }


class PromotionGalleryForm(ImageValidationMixin, forms.ModelForm):
    class Meta:
        model = PromotionGallery
        exclude = ('promotion',)


PromotionGalleryFormset = modelformset_factory(PromotionGalleryForm.Meta.model, form=PromotionGalleryForm,
                                               extra=0, can_delete=True)


# endregion Promotion

# region Pages
class MainPageCardForm(forms.ModelForm):
    class Meta:
        model = MainPageCard
        exclude = ('date_created',)
        widgets = {
            'is_active': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',
            }),
        }


class PageCardForm(ImageValidationMixin, forms.ModelForm):
    class Meta:
        model = PageCard
        exclude = ('date_created',)
        widgets = {
            'is_active': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',
            }),
        }


class PageGalleryForm(ImageValidationMixin, forms.ModelForm):
    class Meta:
        model = PageGallery
        exclude = ('page',)


PageGalleryFormset = modelformset_factory(PageGalleryForm.Meta.model, form=PageGalleryForm,
                                          extra=0, can_delete=True)


class ContactsPageCardForm(forms.ModelForm):
    class Meta:
        model = ContactsPageCard
        exclude = ('date_created',)
        widgets = {
            'is_active': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',
            }),
        }


ContactsPageCardFormset = modelformset_factory(ContactsPageCardForm.Meta.model, form=ContactsPageCardForm,
                                               extra=0, can_delete=True)


# endregion Pages

# region SEO
class SEOForm(forms.ModelForm):
    class Meta:
        model = SEO
        exclude = ('movie', 'news', 'promotion', 'main_page', 'page', 'contacts_page')


# endregion SEO

# region Mailing
class SendSMSForm(forms.Form):
    prefix = 'SMS'
    mailing_type = forms.TypedChoiceField(
        label='Выберите тип рассылки',
        coerce=lambda x: x == 'True',
        choices=((True, 'Все пользователи'), (False, 'Выборочно')),
        widget=forms.RadioSelect(),
        required=True,
        initial=True,
    )
    message = forms.CharField(label='Текст SMS', widget=forms.Textarea(attrs={
        'class': 'textarea form-control'
    }))
    checked_users = forms.CharField(widget=forms.HiddenInput(), required=False)


class SendEmailForm(forms.Form):
    prefix = 'email'

    mailing_type = forms.TypedChoiceField(
        label='Выберите тип рассылки',
        coerce=lambda x: x == 'True',
        choices=((True, 'Все пользователи'), (False, 'Выборочно')),
        widget=forms.RadioSelect,
        required=True,
        initial=True,
    )
    message = forms.FileField(label='Загрузить HTML-письмо', widget=forms.FileInput(attrs={'accept': '.html'}),
                              required=False)

    checked_users = forms.CharField(widget=forms.HiddenInput(), required=False)
    checked_html_message = forms.CharField(widget=forms.HiddenInput(), required=False)
    html_messages_on_delete = forms.CharField(widget=forms.HiddenInput(attrs={'value': []}), required=False)

    def clean_message(self):
        def delete_html_messages():
            on_delete_list = json.loads(self.data[f'{self.prefix}-html_messages_on_delete'])
            for pk in on_delete_list:
                EmailMailingHTMLMessage.objects.get(pk=int(pk)).delete()

        use_cached_message = self.data[f'{self.prefix}-checked_html_message']

        if use_cached_message:
            message = EmailMailingHTMLMessage.objects.get(pk=int(use_cached_message)).message
            delete_html_messages()
        else:
            message = self.cleaned_data['message']
            html_messages_cache = EmailMailingHTMLMessage.objects.all()

            if not message and not html_messages_cache.exists():
                raise forms.ValidationError('Загрузите хотя бы один html-файл', code='invalid')
            else:
                if not message:
                    raise forms.ValidationError('Загрузите html-файл или выберите один из недавних', code='invalid')
                delete_html_messages()

                files_limit = 5
                cached_files_count = len(html_messages_cache)

                while cached_files_count >= files_limit:
                    EmailMailingHTMLMessage.objects.first().delete()
                    cached_files_count -= 1

            message = EmailMailingHTMLMessage.objects.create(name=message.name.replace('.html', ''),
                                                             message=message).message
        html_message = render_to_string(message.path)

        return html_message


# endregion Mailing
