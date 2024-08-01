from pytils.translit import slugify
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (CreateView, ListView, DetailView,
                                  UpdateView, DeleteView)

from materials.models import Material


class MaterialCreateView(CreateView):
    model = Material
    fields = ('title', 'body', 'is_published', 'img', 'date_creation')
    success_url = reverse_lazy('materials:list')

    def form_valid(self, form):
        if form.is_valid():
            new_material = form.save()
            new_material.slug = slugify(new_material.title)
            new_material.save()

        return super().form_valid(form)


class MaterialUpdateView(UpdateView):
    model = Material
    fields = ('title', 'body')
#   success_url = reverse_lazy('materials:list')

    def form_valid(self, form):
        if form.is_valid():
            new_material = form.save()
            new_material.slug = slugify(new_material.title)
            new_material.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('materials:view', args=[self.kwargs.get('pk')])


class MaterialListView(ListView):
    model = Material

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter()
        return queryset


class MaterialDetailView(DetailView):
    model = Material

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class MaterialDeleteView(DeleteView):
    model = Material
    success_url = reverse_lazy('materials:list')


def published(request, pk):
    item = get_object_or_404(Material, pk=pk)
    if item.is_published:
        item.is_published = False
    else:
        item.is_published = True

    item.save()

    return redirect(reverse('materials:list'))
