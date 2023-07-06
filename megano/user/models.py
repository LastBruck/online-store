from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    fullName = models.CharField(max_length=150, null=False, blank=True)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"profile_{self.user.username}"


def profile_avatar_directory_path(instanse: "Avatar", filename):
    return f"avatars/avatar_user_id_{instanse.profile.pk}/{filename}"


class Avatar(models.Model):
    class Meta:
        verbose_name = "Profile image"
        verbose_name_plural = "Profile images"

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="avatar", verbose_name="profile"
    )
    image = models.FileField(upload_to=profile_avatar_directory_path)

    def src(self):
        return f"/media/{self.image}"

    def alt(self):
        return f"avatar_{self.profile.user.username}"

    def __str__(self):
        return f"avatar_{self.profile.user.username}"
