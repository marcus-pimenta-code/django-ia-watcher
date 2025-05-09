from django.contrib import admin
from .models import Document, DocumentChunk, Comment, Note

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'processing_status', 'created_at')
    list_filter = ('processing_status', 'source', 'tags')
    search_fields = ('title', 'original_url', 'extracted_text')
    readonly_fields = ('content_hash', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'source', 'original_url', 'file_path', 'tags')
        }),
        ('Processamento', {
            'fields': ('processing_status', 'extracted_text', 'content_hash')
        }),
        ('Metadados', {
            'fields': ('metadata', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    filter_horizontal = ('tags',)

@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ('document', 'chunk_index')
    list_filter = ('document',)
    search_fields = ('text_content',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('document', 'user', 'created_at')
    list_filter = ('document', 'user')
    search_fields = ('content',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('user', 'tags')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('documents', 'tags')


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    actions = ['enviar_relatorio_email']

    @admin.action(description="Enviar relatório deste tema por e-mail")
    def enviar_relatorio_email(self, request, queryset):
        for tema in queryset:
            enviar_relatorio_por_email.delay(request.user.id, tema.id)

    @admin.action(description="Enviar relatório personalizado (favoritos + anotações)")
    def enviar_relatorio_email_personalizado(self, request, queryset):
        for tema in queryset:
            enviar_relatorio_por_email.delay(request.user.id, tema.id)

        user = request.user
        for tema in queryset:
            enviar_relatorio_por_email.delay(user.id, tema.id)
