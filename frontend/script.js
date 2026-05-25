const API_URL = 'http://18.231.124.171:5000/pontos';

// Atualiza o relógio na tela
function atualizarRelogio() {
    const agora = new Date();
    document.getElementById('relogio').textContent = agora.toLocaleTimeString('pt-BR');
}
setInterval(atualizarRelogio, 1000);
atualizarRelogio();

// Busca os pontos no back-end (Python) e mostra na tabela
async function carregarPontos() {
    try {
        const resposta = await fetch(API_URL);
        const pontos = await resposta.json();
        const corpoTabela = document.getElementById('corpo-tabela');
        corpoTabela.innerHTML = ''; 

        pontos.forEach(ponto => {
            const linha = document.createElement('tr');
            // Formata a data que vem do banco
            const dataFormatada = new Date(ponto.data_hora).toLocaleString('pt-BR');
            linha.innerHTML = `
                <td>${ponto.id}</td>
                <td><strong>${dataFormatada}</strong></td>
                <td>${ponto.tipo}</td>
            `;
            corpoTabela.appendChild(linha);
        });
    } catch (erro) {
        console.error("Erro ao carregar pontos:", erro);
    }
}

// Envia o novo ponto para a API Python
async function registrarPonto(tipo) {
    try {
        await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tipo: tipo })
        });
        carregarPontos(); // Recarrega a tabela após salvar
    } catch (erro) {
        console.error("Erro ao registrar ponto:", erro);
    }
}

// Carrega os dados assim que a página abre
carregarPontos();