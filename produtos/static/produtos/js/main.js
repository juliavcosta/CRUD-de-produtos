const BASE_URL = "/produtos/";

document.addEventListener("DOMContentLoaded", function () {
    const tabela = document.getElementById("tabela-produtos");
    const inputBusca = document.getElementById("busca");
    let timeoutBusca = null;

    function getCookie(nome) {
        const valor = document.cookie
            .split("; ")
            .find((linha) => linha.startsWith(nome + "="));
        return valor ? decodeURIComponent(valor.split("=")[1]) : null;
    }

    function formatarPreco(valor) {
        return new Intl.NumberFormat("pt-BR", {
            style: "currency",
            currency: "BRL",
        }).format(valor);
    }

    function escapeHtml(texto) {
        const div = document.createElement("div");
        div.textContent = texto ?? "";
        return div.innerHTML;
    }

    function carregarProdutos(termo = "") {
        const url = termo
            ? `${BASE_URL}api/?q=${encodeURIComponent(termo)}`
            : `${BASE_URL}api/`;

        tabela.innerHTML = `<tr><td colspan="5" class="text-center text-muted">Carregando...</td></tr>`;

        fetch(url)
            .then((resp) => {
                if (!resp.ok) throw new Error("Erro ao carregar produtos.");
                return resp.json();
            })
            .then((dados) => renderizarTabela(dados.produtos))
            .catch((erro) => {
                tabela.innerHTML = `<tr><td colspan="5" class="text-center text-danger">${escapeHtml(erro.message)}</td></tr>`;
            });
    }

    function renderizarTabela(produtos) {
        if (!produtos.length) {
            tabela.innerHTML = `<tr><td colspan="5" class="text-center text-muted">Nenhum produto encontrado.</td></tr>`;
            return;
        }

        tabela.innerHTML = produtos
            .map(
                (p) => `
            <tr data-id="${p.id}">
                <td>${p.id}</td>
                <td>${escapeHtml(p.nome)}</td>
                <td>${formatarPreco(p.preco)}</td>
                <td>${p.quantidade}</td>
                <td class="text-end">
                    <a href="${BASE_URL}${p.id}/" class="btn btn-sm btn-outline-secondary">Ver</a>
                    <a href="${BASE_URL}${p.id}/editar/" class="btn btn-sm btn-outline-primary">Editar</a>
                    <button type="button" class="btn btn-sm btn-outline-danger btn-excluir" data-id="${p.id}" data-nome="${escapeHtml(p.nome)}">
                        Excluir
                    </button>
                </td>
            </tr>`
            )
            .join("");
    }

    tabela.addEventListener("click", function (evento) {
        const botao = evento.target.closest(".btn-excluir");
        if (!botao) return;

        const id = botao.dataset.id;
        const nome = botao.dataset.nome;

        const confirmou = confirm(
            `Tem certeza que deseja excluir o produto "${nome}"? Essa ação não pode ser desfeita.`
        );
        if (!confirmou) return;

        fetch(`${BASE_URL}api/${id}/excluir/`, {
            method: "DELETE",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
        })
            .then((resp) => {
                if (!resp.ok) throw new Error("Não foi possível excluir o produto.");
                return resp.json();
            })
            .then(() => carregarProdutos(inputBusca.value))
            .catch((erro) => alert(erro.message));
    });

    if (inputBusca) {
        inputBusca.addEventListener("input", function () {
            clearTimeout(timeoutBusca);
            timeoutBusca = setTimeout(() => carregarProdutos(inputBusca.value.trim()), 300);
        });
    }

    carregarProdutos();
});
