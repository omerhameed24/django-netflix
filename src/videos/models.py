from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
from djangoflix.db.models import PublishStateOptions
from djangoflix.db.receivers import publish_state_pre_save, slugify_pre_save

class VideoQueryset(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state = PublishStateOptions.PUBLISH,
            publish_timestamp__lte = now
        )
    


class VideoManager(models.Manager):

    def get_queryset(self):
        return VideoQueryset(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()

# class PublishStateOptions(models.TextChoices):
#     # CONSTANT = DB_VALUE, USER_DISPLAY_VA
#     PUBLISH = 'PU', 'Published'
#     DRAFT = 'DR', 'Draft'
#     # UNLISTED = 'UN', 'Unlisted'
#     # PRIVATE = 'PR', 'Private'


class Video(models.Model):

    # class VideoStateOptions(models.TextChoices):
    #     # CONSTANT = DB_VALUE, USER_DISPLAY_VA
    #     PUBLISH = 'PU', 'Published'
    #     DRAFT = 'DR', 'Draft'
    #     # UNLISTED = 'UN', 'Unlisted'
    #     # PRIVATE = 'PR', 'Private'

    # VideoStateOptions = PublishStateOptions
    title = models.CharField(max_length= 220)
    description = models.TextField(blank=True, null = True)
    slug = models.SlugField(blank=True, null=True) 
    timestamp = models.DateTimeField(auto_now_add= True) # added in the database
    updated = models.DateTimeField(auto_now= True) # last saved in the database 
    video_id = models.CharField(max_length = 220, unique=True)
    active = models.BooleanField(default = True)
    state = models.CharField(max_length=2, choices = PublishStateOptions.choices, default= PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add= False, auto_now= False, blank=True, null=True )
    objects= VideoManager()

    @property
    def is_published(self):
        return self.active

    # def save(self, *args, **kwargs):
    #     if self.state == self.VideoStateOptions.PUBLISH and self.publish_timestamp is None:
    #         print("save as published")
    #         self.publish_timestamp = timezone.now()
    #     elif self.state == self.VideoStateOptions.DRAFT:
    #         self.publish_timestamp = None
        
    #     if self.slug is None:
    #         self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)
    
class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All Video'
        verbose_name_plural = 'All Videos'

class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'

    
pre_save.connect(publish_state_pre_save, sender=Video)
pre_save.connect(slugify_pre_save, sender=Video)