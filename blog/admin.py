from django.contrib import admin
from blog.models import Post, BlogComment
from django.contrib.auth.models import Group
import csv
from django.http import HttpResponse

admin.site.site_header = "Xtreme-Coder Admin";
admin.site.site_title = "Xtreme-Coder Admin Panel";
admin.site.index_title = "Welcome to Xtreme-Coder Admin Panel";

# Register your models here.

admin.site.register(BlogComment);
admin.site.unregister(Group);

def make_rating(modeladmin, request, queryset):
    queryset.update(rating='Average')
make_rating.short_description = "Mark selected blog as Average"

def export_as_csv(self, request, queryset):
    pass
export_as_csv.short_description = "Export Selected"

def export_as_csv(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])
    return response


@admin.register(Post)


class PostAdmin(admin.ModelAdmin):
    ordering = ('title',)
    list_display = ('title','slug','author','timeStamp','rating')
    list_display_links = ('title','author')
    list_editable = ('slug','rating')
    search_fields = ('title','content','author')
    list_filter = ('timeStamp','author')
    prepopulated_fields = {'slug':('title',)}
    actions = [make_rating,export_as_csv]

    class Media:
        js = ('tinyInject.js',)

