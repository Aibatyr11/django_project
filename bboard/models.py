from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.conf import settings

class Bb(models.Model):
    rubric = models.ForeignKey('Rubric',null=True,on_delete=models.PROTECT,verbose_name='Рубрика',)

    title = models.CharField(max_length=50,verbose_name='Товар',
        validators=[validators.RegexValidator(regex='^.{4,}$')],
        error_messages={'invalid': 'Введите 4 и более символа'},
    )

    content = models.TextField(null=True,blank=True,verbose_name='Описание',)

    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        default=0,
        verbose_name='Цена',
    )

    published = models.DateTimeField(auto_now_add=True,db_index=True,verbose_name='Опубликовано',)

    youtube_link = models.URLField(null=True, blank=True)

    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.title} ({self.rubric})'

    class Meta:
        ordering = ['-published', 'title']

        unique_together = ('title', 'rubric')
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'



class BbImage(models.Model):
    bb = models.ForeignKey('Bb', on_delete=models.CASCADE, related_name='images', verbose_name='Объявление')
    image = models.ImageField(upload_to='films_images/', verbose_name='Фото', blank=True, null=True)

    def __str__(self):
        return f'Изображение для {self.bb.title}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Rubric(models.Model):
    name = models.CharField(
        unique=True,
        max_length=20,
        db_index=True,
        verbose_name='Название',
    )

    order = models.SmallIntegerField(
        default=0,
        db_index=True,
        verbose_name = 'Порядок')

    image = models.ImageField(upload_to='films_images/', null=True, blank=True)

    slug = models.SlugField(unique=True, verbose_name='URL', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['order']


class Shop(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        db_index=True,
        verbose_name='Название магазина',
    )

    number = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name='Номер магазина',
        default='+7 (747) 777-70-70'
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        verbose_name='Рейтинг',
    )

    def __str__(self):
        return f'{self.name} — рейтинг {self.rating}'

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class ShopPrice(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Товар')
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Цена в магазине',
    )

    class Meta:
        unique_together = ('shop', 'bb')
        verbose_name = 'Цена товара в магазине'
        verbose_name_plural = 'Цены товаров в магазинах'

    def __str__(self):
        return f'{self.bb.title} в {self.shop.name} — {self.price}₸'


# class CartItem(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     shop_price = models.ForeignKey(ShopPrice, on_delete=models.CASCADE)
#     added_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.shop_price.product.title} - {self.shop_price.price} ₸"
