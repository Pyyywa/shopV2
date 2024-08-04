from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from catalog.models import Product, Version
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from catalog.forms import ProductForm, VersionForm
from pytils.translit import slugify
from django.forms import inlineformset_factory, modelform_factory
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductListView(ListView):
    model = Product

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter()
        return queryset


# def home(request):
#     product_list = Product.objects.all()
#     context = {
#         'object_list': product_list,
#         'title': 'Главная'
#     }
#     return render(request, 'catalog/material_list.html', context)


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["version"] = Version.objects.filter(name=self.object, current_version=True)
        return context_data


# def product(request, pk):
#     product_item = Product.objects.get(pk=pk)
#     context = {
#         'object_list': Product.objects.filter(id=pk),
#         'title': f'{product_item.product_name}'
#     }
#     return render(request, 'catalog/product_detail.html', context)


def contacts(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'catalog/contacts.html', context)


class ProductCreateView(CreateView,LoginRequiredMixin):
    model = Product
    form_class = modelform_factory(Product, form=ProductForm, exclude=['last_change_date', 'views_count', 'slug'])

    def form_valid(self, form):
        if form.is_valid():
            new_material = form.save()
            user = self.request.user
            new_material.owner = user
            new_material.slug = slugify(new_material.product_name)
            new_material.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Формирование формсета
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def get_success_url(self):
        return reverse('catalog:home')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    @transaction.atomic
    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        product_versions = Version.objects.all()
        active_v_counter = 0
        if formset.is_valid():
            self.object = form.save()
            self.object.slug = slugify(self.object.product_name)
            formset.instance = self.object
            formset.save()

        for product in product_versions:
            if product.name_id == self.object.id and product.current_version:
                active_v_counter += 1

        try:
            if active_v_counter > 1:
                raise
        except active_v_counter > 1:
            pass
        finally:
            if active_v_counter < 2:
                return super().form_valid(form)
            else:
                transaction.set_rollback(True)
                form.add_error(None, 'У продукта не может быть более одной активной версии.')
                return self.form_invalid(form)

    def get_success_url(self):
        return reverse('catalog:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Формирование формсета
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
