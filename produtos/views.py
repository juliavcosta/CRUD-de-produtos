from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ProdutoForm
from .models import Produto



def produto_list_page(request):
    return render(request, "produtos/list.html")


def produto_detail_page(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, "produtos/detail.html", {"produto": produto})


def produto_create(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto criado com sucesso!")
            return redirect("produtos:list_page")
    else:
        form = ProdutoForm()
    return render(request, "produtos/form.html", {"form": form, "titulo": "Novo Produto"})


def produto_update(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso!")
            return redirect("produtos:list_page")
    else:
        form = ProdutoForm(instance=produto)
    return render(request, "produtos/form.html", {"form": form, "titulo": "Editar Produto"})




def produto_list_api(request):
    termo = request.GET.get("q", "").strip()
    produtos = Produto.objects.all()
    if termo:
        produtos = produtos.filter(nome__icontains=termo)
    return JsonResponse({"produtos": [p.to_dict() for p in produtos]})


def produto_detail_api(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return JsonResponse(produto.to_dict())


@require_http_methods(["DELETE", "POST"])
def produto_delete_api(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    produto.delete()
    return JsonResponse({"sucesso": True, "mensagem": "Produto excluído com sucesso."})
