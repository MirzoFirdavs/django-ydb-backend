from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    id = models.AutoField(primary_key=True)
    is_man = models.BooleanField(null=True)
    about = models.TextField(blank=True, default="")
    age = models.PositiveBigIntegerField()

    def __str__(self):
        return (
            f"{self.first_name} "
            f"{self.last_name} "
            f"{self.id} {self.is_man} "
            f"{self.about} {self.age}"
        )


class Tag(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return f"{self.name}"


class MultiKeyModel(models.Model):
    key_1 = models.CharField(max_length=255, primary_key=True)
    key_2 = models.IntegerField()
    key_3 = models.CharField(max_length=255)

    class Meta:
        unique_together = ("key_1", "key_2", "key_3")

    def __str__(self):
        return f"{self.key_1}, {self.key_2}, {self.key_3}"
