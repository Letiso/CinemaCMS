from modeltranslation.translator import register, TranslationOptions
from .models import (TopBanner, BackgroundImage, NewsBanner,
                     MovieCard, MovieFrame,
                     CinemaCard, CinemaHallCard,
                     NewsCard, NewsGallery,
                     PromotionCard, PromotionGallery,
                     MainPageCard, AboutTheCinemaPageCard, PageCard, ContactsPageCard,
                     )


class RequiredLangsMixin:
    required_languages = ('en', 'ru', 'uk')


# region Banners
@register(TopBanner)
class TopBannerTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('image', )


@register(BackgroundImage)
class BackgroundImageTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('image', )


@register(NewsBanner)
class NewsBannerTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('image', )


# endregion Banners

# region Movies
@register(MovieCard)
class MovieCardTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('title', 'description', 'main_image', )


# endregion Movies

# region Cinemas
@register(CinemaCard)
class CinemaCardTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('name', 'description', 'amenities', )


@register(CinemaHallCard)
class CinemaHallCardTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('description', )


# endregion Cinemas

# region News
@register(NewsCard)
class NewsCardTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('title', 'description', 'main_image', )


# endregion News

# region Promotion
@register(PromotionCard)
class PromotionCardTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('title', 'description', 'main_image', )


# endregion News

# region Pages
@register(MainPageCard)
class MainPageCardTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('title', )


@register(AboutTheCinemaPageCard)
class AboutTheCinemaPageCardTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('title', 'description', )


@register(PageCard)
class PageCardTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('title', 'description', )


@register(ContactsPageCard)
class ContactsPageCardTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('title', 'address', )


# endregion Pages
