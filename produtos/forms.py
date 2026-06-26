from django import forms

from .models import Produto


class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = ["nome", "descricao", "preco", "quantidade"]
        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: Teclado mecânico",
            }),
            "descricao": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Descrição opcional do produto",
            }),
            "preco": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0.01",
            }),
            "quantidade": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "1",
            }),
        }

    def clean_nome(self):
        nome = (self.cleaned_data.get("nome") or "").strip()
        if not nome:
            raise forms.ValidationError("O nome não pode estar vazio.")
        return nome

    def clean_preco(self):
        preco = self.cleaned_data.get("preco")
        if preco is None or preco <= 0:
            raise forms.ValidationError("O preço deve ser um número positivo.")
        return preco

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get("quantidade")
        if quantidade is None or quantidade <= 0:
            raise forms.ValidationError("A quantidade deve ser um número positivo.")
        return quantidade
