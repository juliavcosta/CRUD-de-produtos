import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Produto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=255, verbose_name="Nome")),
                ("descricao", models.TextField(blank=True, default="", verbose_name="Descrição")),
                (
                    "preco",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.01"), message="O preço deve ser positivo.")],
                        verbose_name="Preço",
                    ),
                ),
                (
                    "quantidade",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1, message="A quantidade deve ser positiva.")],
                        verbose_name="Quantidade",
                    ),
                ),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Produto",
                "verbose_name_plural": "Produtos",
                "ordering": ["-criado_em"],
            },
        ),
    ]
