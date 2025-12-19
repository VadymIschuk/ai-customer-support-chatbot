from django.contrib import admin
from .models import ChatSession, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'text', 'created_at')
    fields = ('sender', 'text', 'created_at')

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'tag', 'is_escalated', 'created_at')
    
    list_filter = ('tag', 'is_escalated', 'created_at')
    
    list_editable = ('tag',)
    
    search_fields = ('session_id',)
    
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'sender', 'text', 'created_at')
    list_filter = ('sender', 'created_at')
    list_select_related = ('session',)