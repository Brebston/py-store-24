from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "core/index.html"


class ContactView(TemplateView):
    template_name = "core/contact.html"


class ReturnsView(TemplateView):
    template_name = "core/returns.html"


class ShippingView(TemplateView):
    template_name = "core/shipping.html"
