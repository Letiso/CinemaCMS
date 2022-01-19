import json
from abc import abstractmethod

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, View
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Model

from .forms import *
from main.models import *

from datetime import date

from cinema.tasks import send_mail
# from user.tests import create_default_users


# region Mixins
class CustomAbstractView(View):
    template_name = None
    context = lambda self, request, *args, **kwargs: {}

    @staticmethod
    def try_to_bound(prefix, request) -> dict:
        return {'data': request.POST, 'files': request.FILES, } if prefix in request.POST else {}

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, self.template_name,
                      self.context(request, *args, **kwargs) if type(self.context) is not dict else self.context)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, self.template_name,
                      self.context(request, args, kwargs) if type(self.context) is not dict else self.context)


class CardView(CustomAbstractView):
    success_url = None
    contains_gallery = True

    @staticmethod
    def save(card, seo, gallery=None):
        if all([form.is_valid() for form in (card, seo, gallery) if form]):
            seo.save()

            card = card.save(commit=False)
            card.seo = seo.instance
            card.save()

            if gallery:
                for image in gallery:
                    if image.is_valid():
                        image = image.save(commit=False)
                        image.card = card
                gallery.save()

            return True

    def post(self, request, *args, **kwargs) -> HttpResponse:
        context = self.context = self.context(request, *args, **kwargs)

        to_save = (context['card']['form'], context['seo']['form'],
                   context['gallery']['formset'] if self.contains_gallery else None)

        if self.save(*to_save):
            return redirect(self.success_url)

        return super().post(request, pk, *args, **kwargs)


# endregion Mixins

# region Statistics
class StatisticsView(CustomAbstractView):
    template_name = 'admin/statistics.html'


# endregion Statistics

# region Banners
class BannersView(CustomAbstractView):
    template_name = 'admin/banners/index.html'

    context = lambda self, request: {
        'top_banners': {
            'required_size': TopBanner.required_size,
            'formset': TopBannerFormSet(**self.try_to_bound('top_banners', request), prefix='top_banners'),
            'carousel': BannersCarouselForm(**self.try_to_bound('top_banners', request),
                                            instance=BannersCarousel.objects.get_or_create(pk=1)[0],
                                            prefix='top_banners')
        },
        'background_image': {
            'required_size': BackgroundImage.required_size,
            'form': BackgroundImageForm(**self.try_to_bound('background_image', request),
                                        instance=BackgroundImage.objects.get_or_create(pk=1)[0],
                                        prefix='background_image'),
        },
        'news_banners': {
            'required_size': NewsBanner.required_size,
            'formset': NewsBannerFormSet(**self.try_to_bound('news_banners', request), prefix='news_banners'),
            'carousel': BannersCarouselForm(**self.try_to_bound('news_banners', request),
                                            instance=BannersCarousel.objects.get_or_create(pk=2)[0],
                                            prefix='news_banners')
        },
    }

    def get_posted_html_form(self, request) -> tuple:
        context = self.context
        for prefix in context.keys():
            if prefix in request.POST: return (
                (context[prefix]['formset'], context[prefix]['carousel']) if 'formset' in context[prefix]
                else (context[prefix]['form'], )
                )

    def post(self, request) -> HttpResponse:
        self.context = self.context(request)

        posted_forms = self.get_posted_html_form(request)
        if all([form.is_valid() for form in posted_forms]):
            for form in posted_forms:
                form.save()
            return HttpResponseRedirect('banners')

        return super().post(request)


# endregion Banners

# region Movies
class MoviesView(CustomAbstractView):
    template_name = 'admin/movies/index.html'

    order = '-date_created'
    context = lambda self, request: {
        'releases': MovieCard.objects.filter(
            is_active=True, release_date__lte=date.today()).order_by(self.order),
        'announcements': MovieCard.objects.filter(
            is_active=True, release_date__gt=date.today()).order_by(self.order),
        'inactive_cards': MovieCard.objects.exclude(
            is_active=True).order_by(self.order),
    }


class MovieCardView(CardView):
    template_name = 'admin/movies/movie_card.html'
    success_url = 'movies'

    context = lambda self, request, pk: {
        'pk': pk,
        'card': {
            'form': MovieCardForm(request.POST or None, request.FILES or None,
                                  instance=get_object_or_404(MovieCard, pk=int(pk)) if pk.isdigit() else None,
                                  prefix='movie'),
            'required_size': MovieCard.required_size,
        },
        'gallery': {
            'formset': MovieFrameFormset(request.POST or None, request.FILES or None,
                                         prefix='movie_frames',
                                         queryset=MovieFrame.objects.filter(card_id=int(pk)) if pk.isdigit()
                                         else MovieFrame.objects.none()),
            'required_size': MovieFrame.required_size,
        },
        'seo': {
            'form': SEOForm(request.POST or None,
                            instance=get_object_or_404(SEO, movie=int(pk)) if pk.isdigit()
                            else None,
                            prefix='seo'),
        },
        'currentUrl': request.get_full_path(),
    }


# endregion Movies

# region Cinemas
class CinemasView(CustomAbstractView):
    template_name = 'admin/cinemas.html'


# endregion Cinemas

# region News
class NewsView(CustomAbstractView):
    template_name = 'admin/news/index.html'

    context = lambda self, request: {
        'news_list': NewsCard.objects.all(),
    }


class NewsCardView(CardView):
    template_name = 'admin/news/news_card.html'
    success_url = 'news_conf'

    context = lambda self, request, pk: {
        'pk': pk,
        'card': {
            'form': NewsCardForm(request.POST or None, request.FILES or None,
                                 instance=get_object_or_404(NewsCard, pk=int(pk)) if pk.isdigit() else None,
                                 prefix='news'),
            'required_size': NewsCard.required_size,
        },
        'gallery': {
            'formset': NewsGalleryFormset(request.POST or None, request.FILES or None,
                                          prefix='news_image',
                                          queryset=NewsGallery.objects.filter(card_id=int(pk)) if pk.isdigit()
                                          else NewsGallery.objects.none()),
            'required_size': NewsGallery.required_size,
        },
        'seo': {
            'form': SEOForm(request.POST or None,
                            instance=get_object_or_404(SEO, news=int(pk)) if pk.isdigit()
                            else None,
                            prefix='seo'),
        },
        'currentUrl': request.get_full_path(),
    }


class NewsCardDeleteView(View):
    @staticmethod
    def get(request, pk) -> HttpResponseRedirect:
        news_to_delete = get_object_or_404(NewsCard, pk=pk)
        news_to_delete.delete()
        return redirect('news_conf')


# endregion News

# region Promotion
class PromotionListView(CustomAbstractView):
    template_name = 'admin/promotion/index.html'

    context = lambda self, request: {
        'promotion_list': PromotionCard.objects.all(),
    }


class PromotionCardView(CardView):
    template_name = 'admin/promotion/promotion_card.html'
    success_url = 'promotion_conf'

    context = lambda self, request, pk: {
        'pk': pk,
        'card': {
            'form': PromotionCardForm(request.POST or None, request.FILES or None,
                                      instance=get_object_or_404(PromotionCard, pk=int(pk)) if pk.isdigit()
                                      else None,
                                      prefix='promotion'),
            'required_size': PromotionCard.required_size,
        },
        'gallery': {
            'formset': PromotionGalleryFormset(request.POST or None, request.FILES or None,
                                               prefix='promotion_image',
                                               queryset=PromotionGallery.objects.filter(card_id=int(pk)) if pk.isdigit()
                                               else PromotionGallery.objects.none()),
            'required_size': PromotionGallery.required_size,
        },
        'seo': {
            'form': SEOForm(request.POST or None,
                            instance=get_object_or_404(SEO, promotion=int(pk))if pk.isdigit()
                            else None,
                            prefix='seo'),
        },
        'currentUrl': request.get_full_path(),
    }


class PromotionCardDeleteView(View):
    @staticmethod
    def get(request, pk) -> HttpResponseRedirect:
        promotion_to_delete = get_object_or_404(PromotionCard, pk=pk)
        promotion_to_delete.delete()
        return redirect('promotion_conf')


# endregion Promotion

# region Pages
class PageListView(CustomAbstractView):
    template_name = 'admin/pages/index.html'

    primary_pages = ('О кинотеатре', 'Кафе - Бар', 'VIP - зал', 'Реклама', 'Детская комната', )

    context = lambda self, request: {
        'main_page': MainPageCard.objects.get_or_create(pk=1, title='Главная страница')[0],
        'primary_page_list': [
            PageCard.objects.get_or_create(pk=pk, title=title)[0] for pk, title in enumerate(self.primary_pages)
        ],
        'contacts_page': ContactsPageCard.objects.get_or_create(pk=1, title='Контакты')[0],
        'custom_page_list': PageCard.objects.exclude(id__in=list(range(
            len(self.primary_pages)
        ))), # exclude *primary_page_list* from queryset by creating [0, 1, 2, ...]
    }


class MainPageCardView(CardView):
    template_name = 'admin/pages/main_page_card.html'
    success_url = 'pages'
    contains_gallery = False

    context = lambda self, request, pk=1: {
        'card': {
            'form': MainPageCardForm(request.POST or None, instance=get_object_or_404(MainPageCard, pk=pk),
                                     prefix='main_page'),
        },
        'seo': {
            'form': SEOForm(request.POST or None,
                            instance=instance if (instance :=
                                                  SEO.objects.filter(main_page=pk).first()) else None,
                            prefix='seo'),
        },
        'currentUrl': request.get_full_path(),
    }


class PageCardView(CardView):
    template_name = 'admin/pages/page_card.html'
    success_url = 'pages'

    context = lambda self, request, pk: {
            'pk': pk,
            'card': {
                'form': PageCardForm(request.POST or None, request.FILES or None,
                                     instance=get_object_or_404(PageCard, pk=int(pk)) if pk.isdigit() else None,
                                     prefix='page'),
                'required_size': PageCard.required_size,
            },
            'gallery': {
                'formset': PageGalleryFormset(request.POST or None, request.FILES or None,
                                              prefix='page_image',
                                              queryset=PageGallery.objects.filter(card_id=int(pk)) if pk.isdigit()
                                              else PageGallery.objects.none()),
                'required_size': PageGallery.required_size,
            },
            'seo': {
                'form': SEOForm(request.POST or None,
                                instance=instance if (instance :=
                                                      SEO.objects.filter(page=pk).first()) else None,
                                prefix='seo'),
            },
            'currentUrl': request.get_full_path(),
        }


class ContactsPageCardView(CustomAbstractView):
    template_name = 'admin/pages/contacts_page_card.html'

    context = lambda self, request, pk=1: {
            'title': 'Карточка страницы контактов',
            'card': {
                'formset': ContactsPageCardFormset(request.POST or None, request.FILES or None, prefix='contacts_page'),
                'required_size': ContactsPageCardFormset.model.required_size,
            },
            'seo': {
                'form': SEOForm(request.POST or None,
                                instance=instance if (instance :=
                                                      SEO.objects.filter(contacts_page=pk).first()) else None,
                                prefix='seo'),
            },
            'currentUrl': request.get_full_path(),
        }

    def post(self, request) -> HttpResponse:
        context = self.context = self.context(request)
        card, seo = context['card']['formset'], context['seo']['form']

        if all([card.is_valid(), seo.is_valid()]):
            seo.save()

            first_contacts_block = card[0].save(commit=False)
            first_contacts_block.seo = seo.instance
            first_contacts_block.save()
            card.save()

            return redirect('pages')

        return super().post(request)


class PageCardDeleteView(View):
    @staticmethod
    def get(request, pk) -> HttpResponseRedirect:
        model = PageCardForm.Meta.model
        page_to_delete = get_object_or_404(model, pk=pk)
        page_to_delete.delete()
        return redirect('pages')


# endregion Pages

# region User
class UsersView(View):
    @staticmethod
    def get_context():
        return {
            'title': 'Пользователи',
            'table_labels': ['ID', 'Логин', 'Email', 'Номер телефона',
                             'Имя', 'Фамилия', 'Пол', 'Язык', 'Дата рождения', 'Адрес', 'Был(а)',
                             'Регистрация', 'Сотрудник', 'Админ', 'Ред.'],
            'users': get_user_model().objects.all(),
        }

    def get(self, request) -> HttpResponse:
        return render(request, 'admin/users/users.html', self.get_context())


class UserUpdateView(UpdateView):
    model = get_user_model()
    success_url = '/admin/users'
    template_name = 'admin/users/update.html'

    form_class = ExtendedUserUpdateForm


class UserDeleteView(View):

    @staticmethod
    def get(request, pk) -> HttpResponseRedirect:
        model = get_user_model()
        user_to_delete = get_object_or_404(model, pk=pk)
        user_to_delete.delete()
        return redirect('users')


# endregion User

# region Mailing
class MailingView(View):
    @staticmethod
    def get_context(request):
        def try_to_bind(prefix):
            return {'data': request.POST, 'files': request.FILES} if prefix in request.POST else {}
        return {
            'forms': {
                'SMS': SendSMSForm(**try_to_bind('SMS')),
                'email': SendEmailForm(**try_to_bind('email'))
            },
            'users': get_user_model().objects.all(),
            'last_html_messages': EmailMailingHTMLMessage.objects.all(),
        }

    def get(self, request) -> HttpResponse:
        return render(request, 'admin/mailing/mailing.html', self.get_context(request))

    def post(self, request) -> HttpResponse:
        context = self.get_context(request)

        for prefix, form in context['forms'].items():
            if prefix in request.POST:
                if form.is_valid():
                    send_to_everyone, message, checked_users = (form.cleaned_data['mailing_type'],
                                                                form.cleaned_data['message'],
                                                                form.cleaned_data['checked_users'])
                    receivers_filter = {} if send_to_everyone else {'id__in': json.loads(checked_users)}
                    send_mail.delay(prefix, message, receivers_filter)

                    return redirect('mailing')
                return render(request, 'admin/mailing/mailing.html', context)


# endregion Mailing
