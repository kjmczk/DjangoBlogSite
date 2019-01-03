# import os
# import random

# from django.conf import settings
# from django.core.mail import send_mail
from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# def get_filename_ext(filepath):
#     base_name = os.path.basename(filepath)
#     name, ext = os.path.splitext(base_name)
#     return name, ext


# def upload_post_image_path(instance, filename):
#     new_filename = random.randint(1000, 9999)
#     name, ext = get_filename_ext(filename)
#     final_filename = '%s%s' % (new_filename, ext)
#     return "post_images/%s" % (final_filename)


# def upload_post_content_image_path(instance, filename):
#     new_filename = random.randint(10000000, 99999999)
#     name, ext = get_filename_ext(filename)
#     final_filename = '%s%s' % (new_filename, ext)
#     return "post_content_images/%s" % (final_filename)


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='post_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.is_public and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ContentImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    content_image = models.ImageField(upload_to='post_content_images/')


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text

    # def send_email_notif(self):
    #     subject = "コメント投稿"
    #     message = "コメントが投稿されました。"
    #     from_email = settings.DEFAULT_FROM_EMAIL
    #     recipient_list = [settings.EMAIL_HOST_USER]
    #     send_email = send_mail(
    #         subject, message, from_email, recipient_list)
    #     return send_email


# @receiver(post_save, sender=Comment)
# def comment_create_receiver(sender, instance, created, **kwargs):
#     if created:
#         instance.send_email_notif()


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text

    # def send_email_notif(self):
    #     subject = "コメント返信"
    #     message = "コメントに返信がありました。"
    #     from_email = settings.DEFAULT_FROM_EMAIL
    #     recipient_list = [settings.EMAIL_HOST_USER]
    #     send_email = send_mail(
    #         subject, message, from_email, recipient_list)
    #     return send_email


# @receiver(post_save, sender=Reply)
# def comment_reply_receiver(sender, instance, created, **kwargs):
#     if created:
#         instance.send_email_notif()
