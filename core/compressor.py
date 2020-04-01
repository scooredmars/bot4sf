from compressor.filters.css_default import CssAbsoluteFilter

# pylint:disable=abstract-method,too-few-public-methods


class NonSuffixCSSAbsoluteFilter(CssAbsoluteFilter):

    def add_suffix(self, url):
        """ Prevent adding suffix to be able to preload certain resources """
        return url
