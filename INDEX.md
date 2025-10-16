# 📚 Índice de Documentação

Bem-vindo ao **Shopper - Buscador de Substitutos**!

Este documento te guia para a documentação certa de acordo com sua necessidade.

---

## 🚀 Eu Quero...

### ... Começar Rapidamente

➡️ **[QUICKSTART.md](QUICKSTART.md)**

- Instalação em 3 passos
- Como usar a interface
- Atalhos e dicas
- Problemas comuns

**Tempo de leitura**: 5 minutos

---

### ... Entender o Projeto Completo

➡️ **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**

- Visão geral completa
- Estrutura do projeto
- Como funciona (diagrama)
- Features e roadmap
- Custos estimados

**Tempo de leitura**: 10 minutos

---

### ... Ler a Documentação Técnica

➡️ **[README.md](README.md)**

- Instalação detalhada
- Funcionalidades completas
- Configurações avançadas
- Troubleshooting
- API e integração

**Tempo de leitura**: 15 minutos

---

### ... Entender a Arquitetura

➡️ **[ARCHITECTURE.md](ARCHITECTURE.md)**

- Módulos e responsabilidades
- Fluxo de dados
- Estrutura de arquivos
- Configurações técnicas
- Performance e segurança

**Tempo de leitura**: 20 minutos

---

## 🛠️ Eu Preciso...

### ... Instalar o Sistema

1. **Automático**: `bash setup.sh`
2. **Manual**: Veja [QUICKSTART.md](QUICKSTART.md) seção 1

### ... Configurar a Chave da OpenAI

1. Edite o arquivo `.env`
2. Coloque: `OPENAI_API_KEY=sk-proj-sua-chave-aqui`
3. Obtenha a chave em: https://platform.openai.com/api-keys

Veja detalhes em [QUICKSTART.md](QUICKSTART.md) seção 2

### ... Executar o Programa

```bash
# Opção 1: Script automático
python start.py

# Opção 2: Manual
cd src && python main.py

# Opção 3: Testar primeiro
python test_components.py
```

### ... Resolver um Problema

1. **Erros comuns**: [QUICKSTART.md](QUICKSTART.md) - Seção "Problemas Comuns"
2. **Troubleshooting**: [README.md](README.md) - Seção "Troubleshooting"
3. **Logs**: Verifique `logs/*.log`
4. **Debug**: [ARCHITECTURE.md](ARCHITECTURE.md) - Seção "Debugging"

### ... Usar Funcionalidades Avançadas

➡️ **[advanced_examples.py](advanced_examples.py)**

- Processar em lote
- Exportar estatísticas
- Validar arquivo de saída
- Testar componentes isoladamente

Execute: `python advanced_examples.py`

---

## 📖 Guia de Leitura Recomendado

### Para Iniciantes

1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** (5min) - Visão geral
2. **[QUICKSTART.md](QUICKSTART.md)** (5min) - Como usar
3. **Prática** - Executar o programa
4. **[README.md](README.md)** (15min) - Quando precisar de detalhes

### Para Desenvolvedores

1. **[ARCHITECTURE.md](ARCHITECTURE.md)** (20min) - Entender arquitetura
2. **Código-fonte** em `src/` - Ler módulos
3. **[advanced_examples.py](advanced_examples.py)** - Ver exemplos
4. **Experimentar** - Modificar e testar

### Para Usuários Avançados

1. **[README.md](README.md)** - Configurações avançadas
2. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Otimizações
3. **[advanced_examples.py](advanced_examples.py)** - Processamento em lote
4. **Logs** - Análise de performance

---

## 📁 Estrutura de Arquivos

```
📚 Documentação
├── 📄 INDEX.md              ← Você está aqui!
├── ⚡ QUICKSTART.md         ← Início rápido
├── 📋 PROJECT_SUMMARY.md    ← Visão geral
├── 📖 README.md             ← Documentação completa
└── 🏗️  ARCHITECTURE.md      ← Arquitetura técnica

🚀 Execução
├── start.py                 ← Iniciar programa (recomendado)
├── setup.sh                 ← Setup automático (bash)
├── test_components.py       ← Testar componentes
└── advanced_examples.py     ← Exemplos avançados

💻 Código-fonte
└── src/
    ├── main.py              ← Orquestrador principal
    ├── ui.py                ← Interface gráfica
    ├── ai_agent.py          ← Integração com IA
    ├── data_processor.py    ← Busca de produtos
    └── file_manager.py      ← Gerenciamento de arquivos

📊 Dados
├── Base_Fazer.csv           ← INPUT: Produtos a processar
├── Itens_Ativos.csv         ← INPUT: Catálogo disponível
└── data/
    ├── substituicoes.csv    ← OUTPUT: Resultados
    ├── cache.json           ← Cache da IA
    └── backups/             ← Backups automáticos

⚙️ Configuração
├── .env                     ← Chave da OpenAI (CONFIGURE!)
├── .env.example             ← Exemplo
├── requirements.txt         ← Dependências
└── .gitignore               ← Git ignore

📝 Logs
└── logs/
    ├── main.log
    ├── ai_agent.log
    ├── data_processor.log
    ├── file_manager.log
    └── ui.log
```

---

## 🔍 Busca Rápida

| Preciso de...       | Onde encontrar                        |
| ------------------- | ------------------------------------- |
| **Instalar**        | QUICKSTART.md ou `bash setup.sh`      |
| **Usar**            | QUICKSTART.md ou `python start.py`    |
| **Configurar IA**   | .env - adicionar OPENAI_API_KEY       |
| **Entender fluxo**  | PROJECT_SUMMARY.md - "Como Funciona"  |
| **Resolver erro**   | QUICKSTART.md - "Problemas Comuns"    |
| **Ajustar config**  | README.md - "Configurações Avançadas" |
| **Ver arquitetura** | ARCHITECTURE.md                       |
| **Processar lote**  | advanced_examples.py                  |
| **Ver logs**        | logs/\*.log                           |
| **Testar**          | `python test_components.py`           |

---

## ❓ FAQ Rápido

### Onde está a chave da OpenAI?

➡️ Arquivo `.env` na raiz do projeto

### Como obter a chave?

➡️ https://platform.openai.com/api-keys

### Como iniciar?

➡️ `python start.py`

### Onde ficam os resultados?

➡️ `data/substituicoes.csv`

### Como ver progresso?

➡️ Aparece na interface ou `python advanced_examples.py` → opção 4

### Posso processar em lote?

➡️ Sim! `python advanced_examples.py` → opção 3

### Onde vejo erros?

➡️ `logs/main.log` e outros em `logs/`

### Como voltar para iteração anterior?

➡️ Use as setas ◀ ▶ na interface

### Quanto custa?

➡️ ~$5.63 para 1.126 produtos (com cache)

### E se eu não tiver chave da OpenAI?

➡️ O sistema pode funcionar com fallback (termos genéricos), mas sem a inteligência da IA

---

## 📞 Precisa de Ajuda?

1. **Veja os logs**: `logs/*.log`
2. **Execute teste**: `python test_components.py`
3. **Leia FAQ**: Este arquivo, seção acima
4. **Troubleshooting**: [README.md](README.md)
5. **Debug**: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🎯 Checklist Inicial

Antes de começar a trabalhar, certifique-se:

- [ ] Li o [QUICKSTART.md](QUICKSTART.md)
- [ ] Instalei dependências (`pip install -r requirements.txt` ou `bash setup.sh`)
- [ ] Configurei `.env` com chave real da OpenAI
- [ ] CSVs estão no lugar (Base_Fazer.csv e Itens_Ativos.csv)
- [ ] Testei com `python test_components.py`
- [ ] Sei como navegar na interface

**Tudo OK?** → `python start.py` 🚀

---

## 📌 Links Rápidos

- **Código-fonte**: `src/main.py`
- **Configuração**: `.env`
- **Resultados**: `data/substituicoes.csv`
- **Logs**: `logs/`
- **Exemplos**: `advanced_examples.py`
- **Testes**: `test_components.py`

---

**Desenvolvido para Shopper - Outubro 2025**

_Boa sorte com seu trabalho! 💪✨_
