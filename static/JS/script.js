// Funções para abas
function openTab(tabName) {
    // Esconde todas as abas
    document.querySelectorAll('.tab-pane').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove classe active de todos os botões
    document.querySelectorAll('.nav-tab button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Mostra a aba selecionada
    document.getElementById(tabName).classList.add('active');
    
    // Ativa o botão correspondente
    event.target.classList.add('active');
    
    // Se for a aba de logs, atualiza automaticamente
    if (tabName === 'logs') {
        atualizarLogs();
    }
}

// Teste de extração
async function testarExtracao() {
    const url = document.getElementById('urlTeste').value.trim();
    const resultadoDiv = document.getElementById('resultadoTeste');
    const alertDiv = document.getElementById('alertResultado');
    
    if (!url) {
        alert('Por favor, digite uma URL para testar.');
        return;
    }
    
    // Mostra loading
    alertDiv.innerHTML = '<div class="loading"><div class="spinner"></div><p>Testando extração...</p></div>';
    resultadoDiv.classList.remove('hidden');
    
    try {
        const response = await fetch('/testar-extracao', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alertDiv.className = 'alert alert-success';
            alertDiv.innerHTML = `✅ ${data.message}`;
        } else {
            alertDiv.className = 'alert alert-error';
            alertDiv.innerHTML = `❌ ${data.message}`;
        }
    } catch (error) {
        alertDiv.className = 'alert alert-error';
        alertDiv.innerHTML = '❌ Erro de conexão com o servidor';
    }
}

// Monitoramento
async function iniciarMonitoramento() {
    const listaProdutos = document.getElementById('listaProdutos').value.trim();
    
    if (!listaProdutos) {
        alert('Por favor, adicione pelo menos um produto para monitorar.');
        return;
    }
    
    try {
        const produtos = JSON.parse(listaProdutos);
        
        const response = await fetch('/iniciar-monitoramento', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ produtos: produtos })
        });
        
        const data = await response.json();
        
        if (data.success) {
            atualizarStatusMonitoramento();
            alert('✅ Monitoramento iniciado!');
        } else {
            alert('❌ ' + data.message);
        }
    } catch (error) {
        alert('❌ Erro no formato JSON. Verifique a sintaxe.');
    }
}

async function pararMonitoramento() {
    const response = await fetch('/parar-monitoramento', {
        method: 'POST'
    });
    
    const data = await response.json();
    
    if (data.success) {
        atualizarStatusMonitoramento();
        alert('⏹️ Monitoramento parado!');
    }
}

async function atualizarStatusMonitoramento() {
    const response = await fetch('/status');
    const status = await response.json();
    
    const statusDiv = document.getElementById('statusMonitoramento');
    const indicator = statusDiv.querySelector('.status-indicator');
    
    if (status.ativo) {
        indicator.className = 'status-indicator status-active';
        statusDiv.innerHTML = '<span class="status-indicator status-active"></span> Monitoramento ativo - ' + 
                            new Date(status.ultima_atualizacao).toLocaleString();
    } else {
        indicator.className = 'status-indicator status-inactive';
        statusDiv.innerHTML = '<span class="status-indicator status-inactive"></span> Monitoramento parado';
    }
}

function carregarExemplo() {
    fetch('/produtos-exemplo')
        .then(response => response.json())
        .then(data => {
            document.getElementById('listaProdutos').value = JSON.stringify(data.produtos, null, 2);
        });
}

// Logs
async function atualizarLogs() {
    const response = await fetch('/logs');
    const data = await response.json();
    
    const logContainer = document.getElementById('logContainer');
    logContainer.innerHTML = '';
    
    data.logs.slice().reverse().forEach(log => {
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        logEntry.textContent = log;
        logContainer.appendChild(logEntry);
    });
}

function limparLogs() {
    if (confirm('Tem certeza que deseja limpar os logs?')) {
        const logContainer = document.getElementById('logContainer');
        logContainer.innerHTML = '<div class="log-entry">Logs limpos</div>';
    }
}

// Atualiza status a cada 10 segundos
setInterval(atualizarStatusMonitoramento, 10000);

// Carrega exemplo ao abrir a página
window.onload = function() {
    carregarExemplo();
    atualizarStatusMonitoramento();
};