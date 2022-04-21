from django.contrib import admin

from .models import Category, Comment, Genre, Title, Review, User, GenreTitle


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    list_display_links = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "review", "pub_date")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    list_display_links = ("name",)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "category",
    )
    list_filter = (
        "category",
        "year",
    )
    search_fields = ("category__name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "score",
        "pub_date",
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "role",
    )
    list_editable = ("role",)


@admin.register(GenreTitle)
class GenreTitle(admin.ModelAdmin):
    list_display = (
        "genre",
        "title",
    )


admin.site.site_title = "YAMBD project"
admin.site.site_header = "YAMBD project"
