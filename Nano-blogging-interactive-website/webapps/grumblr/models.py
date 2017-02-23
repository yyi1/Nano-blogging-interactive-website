from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    time = models.DateTimeField('date published')

    def comments(self):
        return Comment.objects.filter(post=self)

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.__unicode__()


class Comment(models.Model):
    post = models.ForeignKey(Post, null=True)
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    time = models.DateTimeField('date published')

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.__unicode__()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                              default=1, blank=True)
    bio = models.TextField(max_length=420, default="hey there", blank=True)
    picture = models.ImageField(upload_to="add-user-photo", blank=True)
    follower = models.ManyToManyField(User, related_name="follow")

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.__unicode__()

    @staticmethod
    def get_profiles(user):
        return Profile.objects.filter(user=user)


# reference to: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user")
    to_user = models.ManyToManyField(User, related_name="to_user")

    def __unicode__(self):
        return self.from_user.username