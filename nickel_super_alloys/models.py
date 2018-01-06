from unidecode import unidecode
from django.db import models
from django.template.defaultfilters import slugify


class Alloy(models.Model):
    """Nickel-based super alloy model"""
    name = models.CharField(verbose_name="Наименование", max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    balance = models.CharField(verbose_name="Основа", default="Ni", blank=True, max_length=3)
    type_of_alloy = models.CharField(verbose_name="Тип сплава", blank=True, max_length=70)
    type_of_structure = models.CharField(verbose_name="Тип структуры", blank=True, max_length=70)
    work_temp = models.IntegerField(verbose_name="Рабочая температура", blank=True, null=True)
    created_date = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        if not self.type_of_alloy:
            self.type_of_alloy = "-"
        if not self.type_of_structure:
            self.type_of_structure = "-"
        super(Alloy, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "сплав"
        verbose_name_plural = "сплавы"

class CharacteristicAbstract(models.Model):
    """ An abstract base class model that provides self-
        updating ``alloy`` fields.
    """
    alloy = models.ForeignKey(Alloy, verbose_name="Сплав")

    class Meta:
        abstract = True

class AlloyingElement(CharacteristicAbstract):
    """
    Alloying element of alloy
    Легирующий элемент
    """
    element = models.CharField(verbose_name="Элемент",max_length=10)
    value = models.FloatField()

    def __str__(self):
        return "%s: %.3g - (%s)" % (self.element, self.value, self.alloy)

    class Meta:
        verbose_name = "легирующий элемент"
        verbose_name_plural = "легирующие элементы"

class LongTimeStressRupture(CharacteristicAbstract):
    """
    Long-time stress-rupture properties
    Значение предельной длительной прочности
    """
    temperature = models.IntegerField(verbose_name="Температура, С")
    life  = models.IntegerField(verbose_name="Время испытания, ч", default=100)
    stress = models.IntegerField(verbose_name="Предел длительной прочности, МПа")

    def __str__(self):
        return "σ%s(%s) = %d - (%s)" % (self.life, self.temperature, self.stress, self.alloy)

    class Meta:
        ordering = ['temperature']
        verbose_name = "длительная прочность"
        verbose_name_plural = "длительная прочность"

class OtherProperties(CharacteristicAbstract):
    """
    Дополнительные данные о сплаве
    """
    name = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.alloy)

    class Meta:
        verbose_name = "свойства"
        verbose_name_plural = "характеристики"
