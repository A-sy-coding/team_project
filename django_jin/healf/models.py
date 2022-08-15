from django.db import models
from users.models import Profile
class userinfo(models.Model):
    id = models.BigAutoField(help_text="Comment ID", primary_key=True)
    email = models.ForeignKey(Profile, related_name="info", on_delete=models.CASCADE, db_column="post_id")
# Create your models here.
