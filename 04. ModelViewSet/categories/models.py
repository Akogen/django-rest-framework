from django.db import models
from common.models import AbstractTimeStamp


class Category(AbstractTimeStamp):
    """Categories Model Definition"""

    class CatogoryTypeChoices(models.TextChoices):
        ROOM = ("rooms", "Rooms")
        EXPERIENCE = ("experiences", "Experiences")

    name = models.CharField(max_length=250)
    category_type = models.CharField(
        max_length=15,
        choices=CatogoryTypeChoices.choices,
    )

    def __str__(self) -> str:
        return f"{self.category_type} - {self.name}"

    class Meta:
        verbose_name_plural = "Categories"
