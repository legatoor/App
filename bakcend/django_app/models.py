from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_delete, post_save


def user_avatar_path(instance, filename):
    return f"user_images/{instance.pin}/{instance.pin}.{filename.split('.')[-1]}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )
    is_banned = models.BooleanField(default=False, verbose_name="Статус Блокировки")
    phonenumber = models.CharField(max_length=20, verbose_name="Номер телефона")
    last_login_ip = models.GenericIPAddressField(
        verbose_name="Последний IP-адрес входа", null=True, blank=True
    )
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        null=True,
        blank=True,
        verbose_name="Фото Пользователя",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
    )

    def __str__(self):
        return f"{self.user.username} Profile"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=UserProfile)
def update_user_active_status(sender, instance, **kwargs):
    if instance.is_banned:
        instance.user.is_active = False
    else:
        instance.user.is_active = True
    instance.user.save()


@receiver(post_delete, sender=UserProfile)
def delete_user_on_profile_delete(sender, instance, **kwargs):
    user = instance.user
    user.delete()


@receiver(post_save, sender=UserProfile)
@receiver(post_delete, sender=UserProfile)
def update_jwt_token(sender, instance, **kwargs):
    user = instance.user
    RefreshToken.for_user(user)


class Item(models.Model):
    author = models.ForeignKey(
        verbose_name="Автор",
        db_index=True,
        primary_key=False,
        editable=True,
        blank=True,
        null=False,
        default=None,
        to=User,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255, verbose_name="Наименование")
    image = models.ImageField(
        upload_to="product_pictures/",
        null=True,
        blank=True,
        editable=True,
        default=None,
        verbose_name="Фото Продукта",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])
        ],
    )
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.PositiveIntegerField(verbose_name="Цена")
    category = models.ForeignKey(
        "CategoryItem", on_delete=models.CASCADE, verbose_name="Категория"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активность объявления")
    tags = models.ManyToManyField("TagItem", blank=True, verbose_name="Тэги")
    discounted_price = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Скидочная цена",
        help_text="Цена со скидкой, если применена",
    )

    class Meta:
        ordering = (
            "is_active",
            "-title",
        )
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        status = "Активен" if self.is_active else "Отсутствует"
        return f"""Товар = id: {self.id},
        Название = {self.title},
        Цена = {self.price},
        Статус {status},
        Категория = {self.category.title}"""


class CategoryItem(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="Наименование",
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name="Ссылка",
        null=False,
        editable=True,
        unique=True,
    )

    class Meta:
        ordering = ("-title",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"Категория id: {self.id}, Название: {self.title}, Ссылка: {self.slug}"


class TagItem(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Наименование",
    )
    slug = models.SlugField(
        max_length=255, verbose_name="Ссылка", null=False, editable=True, unique=True
    )

    class Meta:
        ordering = ("-title",)
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return f"Тэг id: {self.id}, Название: {self.title}, Ссылка: {self.slug}"
