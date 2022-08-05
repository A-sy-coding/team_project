from django.db import models

# POST를 통해 얻은 데이를 이용해 squat count를 세고, 데이터베이스에 저장하도록 한다.
class Count_Post(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return self.text
