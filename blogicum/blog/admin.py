from django.contrib import admin
from .models import Post, Category, Location, Comment
from django.template.defaultfilters import truncatewords

admin.site.empty_value_display = 'Не задано'


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'view_short_text',
        'author',
        'location',
        'category',
        'is_published',
    )

    @admin.display(empty_value="Пост в процессе разработки")
    def view_short_text(self, obj):
        return truncatewords(obj.text, 7)
    view_short_text.short_description = "Начало поста"

    list_editable = (
        'author',
        'location',
        'category',
        'is_published',
    )
    search_fields = ('title', 'text',)
    list_filter = ('is_published', 'category', 'location',)
    list_display_links = ('title', 'view_short_text',)


class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = ['is_published', 'title', 'author', 'location']
    list_display_links = ('title')


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )

    list_display = (
        'title',
    )


class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'name',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment, CommentAdmin)
