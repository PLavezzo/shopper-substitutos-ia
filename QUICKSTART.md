# 🚀 Guia Rápido de Início

## ⚡ Instalação em 3 Passos

### 1️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar chave da OpenAI

Edite o arquivo `.env` e coloque sua chave:

```
OPENAI_API_KEY=sk-proj-sua-chave-real-aqui
```

**Como obter a chave:**

- Vá em: https://platform.openai.com/api-keys
- Faça login
- Clique em "Create new secret key"
- Copie a chave e cole no arquivo `.env`

### 3️⃣ Iniciar o programa

```bash
python start.py
```

Ou manualmente:

```bash
cd src
python main.py
```

---

## 💡 Como Usar

### Interface

```
┌─────────────────────────────────────────┐
│      PRODUTO ORIGINAL                   │
│  QUEIJO RALADO FAIXA AZUL PARMESÃO 50G  │
│         Preço: R$ 10,99                 │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  ◀ Anterior  [Iteração: 1] Ir  Próximo ▶│
│  Progresso: 0/1126 (0.0%)               │
│  Busca manual: [_______] Buscar  Pular  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│   SUBSTITUTOS ENCONTRADOS (10 resultados)│
│                                          │
│  ☐ SHOP001 | QUEIJO RALADO... | 11,50   │
│  ☐ SHOP002 | QUEIJO RALADO... | 18,90   │
│  ☐ SHOP003 | QUEIJO RALADO... |  9,99   │
│  ...                                     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  Selecionados: 0/5                      │
│                [💾 Salvar] [✓ Salvar e Avançar] │
└─────────────────────────────────────────┘
```

### Workflow

1. **Produto aparece** automaticamente
2. **IA gera termos** de busca e mostra resultados
3. **Marque até 5** checkboxes dos melhores substitutos
4. **Clique "Salvar e Avançar"** para ir ao próximo
5. **Repita** até completar todos os 1126 itens!

### Atalhos e Dicas

- ⌨️ **Enter** no campo de iteração = ir para número específico
- ⌨️ **Enter** no campo de busca = buscar manualmente
- 🔙 Use **setas** para voltar e revisar
- ⏭️ Clique **Pular** se não encontrar substitutos adequados
- 💾 O sistema **salva automaticamente** backups

---

## 📊 Arquivo de Saída

Os substitutos são salvos em: **`data/substituicoes.csv`**

Formato:
| n_iteracao | sub1_cod_produto | sub1_nome | sub1_preco | sub2_cod_produto | ... |
|------------|------------------|-----------|------------|------------------|-----|
| 1 | SHOP001 | QUEIJO... | 11,50 | SHOP002 | ... |
| 2 | SHOP010 | OVO... | 15,99 | | |

---

## 🎯 Legenda de Scores

- 🟢 **90-100**: Match perfeito (mesma categoria, características similares)
- 🟡 **70-89**: Match bom (categoria correta, algumas diferenças)
- 🔴 **<70**: Match aproximado (verifique com cuidado)

---

## ⚠️ Problemas Comuns

### "API key not found"

➡️ Edite o arquivo `.env` e adicione sua chave real da OpenAI

### "Arquivo CSV não encontrado"

➡️ Certifique-se de que `Base_Fazer.csv` e `Itens_Ativos.csv` estão no diretório raiz

### Nenhum resultado aparece

➡️ Use a **busca manual** com termos mais simples (ex: "queijo", "pão")

### Interface não abre

➡️ Verifique se instalou todas as dependências:

```bash
pip install -r requirements.txt
```

---

## 📁 Estrutura de Pastas

```
Subs_Cadastro/
├── 📄 Base_Fazer.csv          ← Produtos para processar
├── 📄 Itens_Ativos.csv        ← Catálogo disponível
├── 🔑 .env                    ← Sua chave da OpenAI (EDITE ESTE!)
├── 🚀 start.py                ← Inicie por aqui
├── src/
│   └── main.py                ← Ou inicie por aqui
├── data/
│   ├── substituicoes.csv      ← Resultado final
│   ├── cache.json             ← Cache da IA
│   └── backups/               ← Backups automáticos
└── logs/                      ← Logs de erro
```

---

## 💰 Custos da API OpenAI

- **GPT-4o**: ~$0.005 por produto
- **1126 produtos**: ~$5.63 total
- **Cache**: Produtos repetidos não custam nada!

**Dica**: A IA só é chamada uma vez por produto. Se você voltar para revisar, usa o cache.

---

## ✅ Checklist Antes de Começar

- [ ] Instalei as dependências (`pip install -r requirements.txt`)
- [ ] Coloquei minha chave da OpenAI no arquivo `.env`
- [ ] Os arquivos `Base_Fazer.csv` e `Itens_Ativos.csv` estão presentes
- [ ] Testei executando `python start.py`

---

## 🆘 Precisa de Ajuda?

1. **Verifique os logs**: `logs/main.log`, `logs/ai_agent.log`
2. **Rode o teste**: `python test_components.py`
3. **Consulte o README.md** completo

---

**Bom trabalho! 🛒✨**
