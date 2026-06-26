from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Produto(models.Model):

    nome = models.CharField(
        max_length=255,
        verbose_name="Nome",
    )
    descricao = models.TextField(
        blank=True,
        default="",
        verbose_name="Descrição",
    )
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"), message="O preço deve ser positivo.")],
        verbose_name="Preço",
    )
    quantidade = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message="A quantidade deve ser positiva.")],
        verbose_name="Quantidade",
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self) -> str:
        return self.nome

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": float(self.preco),
            "quantidade": self.quantidade,
        }
