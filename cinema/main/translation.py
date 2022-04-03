from modeltranslation.translator import register, TranslationOptions
from .models import TopBanner


@register(TopBanner)
class TopBannerTranslationOptions(TranslationOptions):
    fields = ('image', )
