from django.db import models

from users.models import CustomUser
from utils.models import AbstractUUID, AbstractTimeTracker


class Product(AbstractUUID, AbstractTimeTracker):
    name = models.CharField(max_length=100, verbose_name='' )
    description = models.CharField(max_length=100, blank=True)
    cost = models.IntegerField(default=0)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Владелец'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductAttachment(AbstractUUID, AbstractTimeTracker):
    file = models.FileField(verbose_name='Файлы')

    class Meta:
        verbose_name = 'Yeah'
        verbose_name_plural = 'Yeahs'
