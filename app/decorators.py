import functools

from django.contrib.admin import helpers
from django.template.response import TemplateResponse


def action_parser_form(form_class=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, queryset):
            form = form_class()
            context = dict(
                self.admin_site.each_context(request),
                title=form_class.title,
                action=func.__name__,
                opts=self.model._meta,
                queryset=queryset, form=form,
                action_checkbox_name=helpers.ACTION_CHECKBOX_NAME
            )

            return TemplateResponse(request, 'admin/parse.html', context)

        wrapper.short_description = form_class.title

        return wrapper

    return decorator


def action_malling_form(form_class=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, queryset):
            form = form_class()
            context = dict(
                self.admin_site.each_context(request),
                title=form_class.title,
                action=func.__name__,
                opts=self.model._meta,
                queryset=queryset, form=form,
                action_checkbox_name=helpers.ACTION_CHECKBOX_NAME
            )

            return TemplateResponse(request, 'admin/malling.html', context)

        wrapper.short_description = form_class.title

        return wrapper

    return decorator
 