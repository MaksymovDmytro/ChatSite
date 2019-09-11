from django.conf import settings
from django.db import models
from django.db.models import Q


class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(receiver=user) | Q(sender=user)
        qlookup2 = Q(receiver=user) & Q(sender=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2)
        return qs

    def get_or_new(self, user1, username2):
        username1 = user1.username
        # User can't have a chat with itself
        if username1 == username2:
            return None, False
        # Both queues are aming to find a thread combination of two users
        qlookup1 = Q(receiver__username=username1) & Q(sender__username=username2)
        qlookup2 = Q(receiver__username=username2) & Q(sender__username=username1)
        qs = self.get_queryset().filter(qlookup1 | qlookup2)
        # If only one result found, return it
        if qs.count() == 1:
            return qs.first(), False
        # If more than one result found, return latest one
        elif qs.count() > 1:
            return qs.order_by('timestamp').last(), False
        else:
            # If none found then create one
            user_class = user1.__class__
            user2 = user_class.objects.get(username=username2)
            # User can't send messages to himself
            if user1 != user2:
                obj = self.model(
                    receiver=user2,
                    sender=user1
                )
                obj.save()
                return obj, True
            return None, False


class Thread(models.Model):
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_receiver')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_sender')
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    def __str__(self):
        return f'Sent by {self.sender} to {self.receiver}'


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='sender', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
