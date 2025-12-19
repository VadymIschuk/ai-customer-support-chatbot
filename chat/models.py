from django.db import models


class ChatSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_escalated = models.BooleanField(default=False)
    tag = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General Inquiry'),
            ('billing', 'Billing Issues'),
            ('tech', 'Technical Support'),
            ('complaint', 'Complaint')
        ],
        default='general'
    )

    def __str__(self):
        return f"Session {self.session_id}"


class Message(models.Model):
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('bot', 'Bot')])
    text = models.CharField(max_length=4096)
    created_at = models.DateTimeField(auto_now_add=True)
