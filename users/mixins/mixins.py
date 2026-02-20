from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.http import HttpRequest, HttpResponseBase


class AnonymousRequiredMixin(View):

    def dispatch(
            self,
            request: HttpRequest,
            *args,
            **kwargs
    ) -> HttpResponseBase:
        if request.user.is_authenticated:
            return redirect(
                reverse("users:profile")
            )
        return super().dispatch(request, *args, **kwargs)
