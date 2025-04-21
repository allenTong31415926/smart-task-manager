from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task
from .models import Tag
from .utils import extract_tags_from_title

@receiver(post_save, sender=Task)
def auto_tag_task(sender, instance, created, **kwargs):
    # Get tags from the current title
    tag_names = extract_tags_from_title(instance.title)
    
    # Clear existing tags if this is an update
    if not created:
        instance.tags.clear()
    
    # Add new tags
    for name in tag_names:
        tag, _ = Tag.objects.get_or_create(name=name)
        tag.tasks.add(instance)
