from django.db import models
from django.contrib.postgres.fields import ArrayField

class guest(models.Model):

    # Модель списка гостей

    ALCOHOL_CHOICES = [
        ("Красное вино", "Красное вино"),
        ("Белое вино", "Белое вино"),
        ("Шампанское", "Шампанское"),
        ("Водка", "Водка"),
        ("Коньяк", "Коньяк"),
    ]

    first_name = models.CharField(verbose_name='Имя', max_length=15)
    last_name = models.CharField(verbose_name='Фамилия', max_length=15)
    consent = models.BooleanField(verbose_name='Подтвердите свое присутвие', blank=False)
    alcohol = ArrayField(models.CharField(max_length=20, choices=ALCOHOL_CHOICES),
                         blank=True,
                         default=list,
                         verbose_name='Предпочитаемый алкоголь'
                         )
    
    class Meta:

        # Название модели в админ-панели и сортировка по имени

        db_table = 'guest'
        ordering = ['first_name']
        verbose_name = 'Гость'
        verbose_name_plural = 'Гости'


    def __str__(self):
        return f'{self.first_name} {self.last_name} | {self.consent} | {self.alcohol}'