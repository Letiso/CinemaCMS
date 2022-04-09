from modeltranslation.translator import register, TranslationOptions
from .models import TopBanner, BackgroundImage, NewsBanner, MovieCard, MovieFrame


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


@register(MovieFrame)
class MovieFrameTranslationOptions(RequiredLangsMixin, TranslationOptions):
    fields = ('image', )


# endregion Movies

