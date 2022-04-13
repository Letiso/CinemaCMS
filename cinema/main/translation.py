from modeltranslation.translator import register, TranslationOptions
from .models import (TopBanner, BackgroundImage, NewsBanner,
                     MovieCard, MovieFrame,
                     CinemaCard, CinemaHallCard,
                     NewsCard, NewsGallery, )


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
class MovieCardTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('title', 'description', 'main_image', )


@register(NewsGallery)
class MovieCardTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('image', )

# endregion News
