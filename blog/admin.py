from blog.models import Article, Category, Attachment, Comment
from django.contrib import admin
from django.contrib.auth.models import User

# set the Attachment class as the inline item of the Article

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline]
    date_hierarchy = 'pub_date'
    search_fields = ['title']
    list_display = ('title', 'author', 'pub_date', 'get_category')


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(ArticleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # set the default user as the current logged user.
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return field

    # get foreign key "Category" into the list_display.
    def get_category(self, obj):
        return '%s'%(obj.category.name)
    get_category.short_description = 'Category'

class CategorysAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    search_fields = ['name']
    list_display = ('name', 'pub_date')

class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    search_fields = ['name', 'comment']
    list_display = ('comment','name','pub_date')

admin.site.register(Category, CategorysAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
