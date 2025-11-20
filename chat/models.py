from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class ChatRoom(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='operator_rooms')
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-updated',)
    
    def __str__(self):
        return f'Chat with {self.user.username}'

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('timestamp',)
    
    def __str__(self):
        return f'Message from {self.user.username}'
