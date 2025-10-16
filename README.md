# Shopper - Buscador de Substitutos 🛒

Sistema inteligente para catalogar substitutos de produtos usando IA (GPT-4o) e interface gráfica em Python.

## 📋 Funcionalidades

- ✅ **Análise por IA**: GPT-4o gera termos de busca inteligentes para cada produto
- ✅ **Busca Automática**: Encontra substitutos nos 12 mil produtos disponíveis
- ✅ **Interface Intuitiva**: CustomTkinter com tema moderno e escuro
- ✅ **Navegação Fácil**: Setas para avançar/voltar, campo para ir direto à iteração
- ✅ **Sistema de Checkboxes**: Selecione até 5 substitutos por produto
- ✅ **Busca Manual**: Campo adicional para busca personalizada
- ✅ **Auto-save**: Backup automático a cada salvamento
- ✅ **Cache Inteligente**: Evita chamadas repetidas à API da OpenAI
- ✅ **Progresso Visual**: Acompanhe quantos itens já foram processados

## 🚀 Instalação

### 1. Pré-requisitos

- Python 3.8 ou superior
- Chave da API OpenAI

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar chave da OpenAI

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua_chave_aqui
```

### 4. Verificar arquivos CSV

Certifique-se de que os arquivos estão no diretório raiz:

- `Base_Fazer.csv` - Produtos que precisam de substitutos
- `Itens_Ativos.csv` - Catálogo com 12 mil produtos disponíveis

## 📁 Estrutura do Projeto

```
Subs_Cadastro/
├── src/
│   ├── main.py              # Arquivo principal
│   ├── ui.py                # Interface CustomTkinter
│   ├── ai_agent.py          # Integração com GPT-4o
│   ├── data_processor.py    # Busca e processamento de dados
│   └── file_manager.py      # Gerenciamento de CSVs
├── data/
│   ├── cache.json           # Cache de termos da IA
│   ├── substituicoes.csv    # Arquivo de saída
│   └── backups/             # Backups automáticos
├── logs/                    # Logs da aplicação
├── Base_Fazer.csv           # Input: produtos a processar
├── Itens_Ativos.csv         # Input: catálogo disponível
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

## 💻 Como Usar

### Iniciar o programa

```bash
cd src
python main.py
```

### Fluxo de trabalho

1. **Produto Original**: Aparece destacado no topo com nome e preço
2. **Resultados**: IA gera termos e busca automaticamente
3. **Seleção**: Marque até 5 substitutos com checkboxes
4. **Salvar**: Clique em "Salvar" ou "Salvar e Avançar"
5. **Navegação**: Use setas ou digite número da iteração

### Atalhos

- `Enter` no campo de iteração: Ir para iteração
- `Enter` no campo de busca manual: Buscar
- Botão "Pular": Marca iteração como vazia e avança

## 📊 Arquivo de Saída

O arquivo `data/substituicoes.csv` contém:

| Coluna                     | Descrição                  |
| -------------------------- | -------------------------- |
| n_iteracao                 | Número da iteração (linha) |
| sub1_cod_produto           | Código do 1º substituto    |
| sub1_nome                  | Nome do 1º substituto      |
| sub1_preco_loja_programada | Preço do 1º substituto     |
| sub2_cod_produto           | Código do 2º substituto    |
| ...                        | (até 5 substitutos)        |

## 🤖 Como a IA Funciona

A IA (GPT-4o) analisa o nome do produto e gera 5 termos de busca em ordem de generalidade:

**Exemplo**: `QUEIJO RALADO FAIXA AZUL PARMESÃO 50G`

Termos gerados:

1. `queijo ralado parmesão 50g` (mais específico)
2. `queijo ralado parmesão`
3. `queijo parmesão ralado`
4. `queijo ralado`
5. `queijo` (mais genérico)

O sistema busca com cada termo até encontrar resultados relevantes.

## 🔍 Sistema de Busca

1. **Busca Exata**: Procura termos no nome do produto
2. **Busca Fuzzy**: Se não encontrar, usa similaridade aproximada
3. **Score**: Cada resultado tem um score de 0-100
   - 🟢 Verde (90+): Match excelente
   - 🟡 Amarelo (70-89): Match bom
   - 🔴 Vermelho (<70): Match aproximado

## 🛡️ Segurança e Backup

- ✅ Backup automático antes de cada salvamento
- ✅ Mantém últimos 10 backups em `data/backups/`
- ✅ Logs detalhados em `logs/`
- ✅ Cache local para reduzir custos de API

## ⚙️ Configurações Avançadas

### Ajustar número máximo de resultados

Em `src/data_processor.py`, linha ~70:

```python
max_results=50  # Altere para o valor desejado
```

### Ajustar temperatura da IA

Em `src/ai_agent.py`, linha ~90:

```python
temperature=0.3  # 0=preciso, 1=criativo
```

### Ajustar threshold de busca fuzzy

Em `src/data_processor.py`, linha ~150:

```python
min_similarity=60  # 0-100, quanto maior mais restritivo
```

## 🐛 Troubleshooting

### Erro: "Não foi possível resolver a importação"

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro: "OpenAI API key not found"

Verifique se o arquivo `.env` existe e contém a chave correta.

### Interface não aparece

Certifique-se de que está executando de dentro da pasta `src/`:

```bash
cd src
python main.py
```

### Resultados não aparecem

- Verifique os logs em `logs/`
- Teste busca manual com termos simples
- Verifique se `Itens_Ativos.csv` está correto

## 📝 Logs

Todos os logs são salvos em `logs/`:

- `main.log` - Log principal da aplicação
- `ai_agent.log` - Chamadas à API OpenAI
- `data_processor.log` - Buscas e processamento
- `file_manager.log` - Operações com arquivos
- `ui.log` - Interações na interface

## 🎯 Dicas de Uso

1. **Revise os resultados**: O score ajuda a identificar melhores matches
2. **Use busca manual**: Se a IA não encontrar, tente termos específicos
3. **Pule quando necessário**: Não perca tempo em produtos difíceis
4. **Acompanhe o progresso**: O percentual ajuda a planejar o trabalho
5. **Faça pausas**: O sistema salva automaticamente, pode retomar depois

## 📞 Suporte

Para problemas ou sugestões:

- Verifique os logs em `logs/`
- Consulte este README
- Revise as configurações dos módulos

## 🔄 Atualizações Futuras

Possíveis melhorias:

- [ ] Filtro por faixa de preço
- [ ] Ordenação personalizada
- [ ] Export para Excel
- [ ] Estatísticas detalhadas
- [ ] Modo de revisão batch
- [ ] Suporte a múltiplos usuários

---

**Desenvolvido com ❤️ para Shopper**
