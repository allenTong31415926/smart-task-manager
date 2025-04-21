from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task
from .models import Tag
from .utils import extract_tags_from_title

@receiver(post_save, sender=Task)
def auto_tag_task(sender, instance, created, **kwargs):
    if not created:
        return  # Only tag new tasks

    tag_names = extract_tags_from_title(instance.title)

    for name in tag_names:
        tag, _ = Tag.objects.get_or_create(name=name)
        tag.tasks.add(instance)
