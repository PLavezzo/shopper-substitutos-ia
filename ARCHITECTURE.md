# 🏗️ Arquitetura do Sistema

## Visão Geral

O sistema é composto por 5 módulos principais que trabalham em conjunto:

```
┌──────────────────────────────────────────────┐
│                   main.py                     │
│        (Orquestrador Principal)              │
└──────────┬───────────────────────────────────┘
           │
           ├─────► ai_agent.py (Geração de Termos)
           │
           ├─────► data_processor.py (Busca de Produtos)
           │
           ├─────► file_manager.py (Gerenciamento de Arquivos)
           │
           └─────► ui.py (Interface Gráfica)
```

---

## 📁 Módulos Detalhados

### 1. `main.py` - Orquestrador Principal

**Responsabilidade**: Integrar todos os módulos e gerenciar o fluxo da aplicação.

**Classes**:

- `SubstituteFinderApp`: Controlador principal

**Funções Principais**:

- `load_iteration()`: Carrega uma iteração específica
- `save_substitutes()`: Salva substitutos selecionados
- `manual_search()`: Realiza busca manual
- `_search_substitutes_with_ai()`: Busca usando IA (em thread separada)

**Fluxo**:

1. Inicializa todos os componentes
2. Carrega primeira iteração
3. Aguarda interação do usuário
4. Processa ações (salvar, navegar, buscar)
5. Atualiza interface

---

### 2. `ai_agent.py` - Geração de Termos com IA

**Responsabilidade**: Usar GPT-4o para gerar termos de busca inteligentes.

**Classes**:

- `AIAgent`: Integração com OpenAI

**Funções Principais**:

- `generate_search_terms()`: Gera 5 termos de busca
- `_create_prompt()`: Monta prompt para GPT-4o
- `_parse_response()`: Processa resposta da IA
- `_fallback_search_terms()`: Gera termos quando IA falha

**Cache**:

- Armazena termos já gerados em `data/cache.json`
- Evita chamadas repetidas à API
- Reduz custos

**Configuração**:

```python
temperature=0.3  # Precisão vs Criatividade
max_tokens=500   # Limite de resposta
model="gpt-4o"   # Modelo usado
```

---

### 3. `data_processor.py` - Busca de Produtos

**Responsabilidade**: Buscar substitutos no catálogo de 12 mil produtos.

**Classes**:

- `DataProcessor`: Processamento e busca de dados

**Funções Principais**:

- `search_products()`: Busca usando múltiplos termos
- `normalize_text()`: Normaliza texto (remove acentos, etc)
- `_fuzzy_search()`: Busca aproximada quando exata falha
- `filter_by_price_range()`: Filtra por faixa de preço

**Algoritmo de Busca**:

1. **Busca Exata**: Procura termo no nome do produto
2. **Penalização por Generalidade**: Termos mais genéricos têm score menor
3. **Busca Fuzzy**: Se não achar, usa similaridade aproximada
4. **Score Final**: Combina relevância + especificidade

**Normalização**:

```python
"QUEIJO RALADO PARMESÃO 50G"
     ↓
"queijo ralado parmesao 50g"  # Sem acentos, minúscula
```

---

### 4. `file_manager.py` - Gerenciamento de Arquivos

**Responsabilidade**: Ler CSVs, salvar seleções, criar backups.

**Classes**:

- `FileManager`: Gerenciador de arquivos

**Funções Principais**:

- `load_base_fazer()`: Carrega produtos a processar
- `get_item_by_iteration()`: Busca produto por iteração
- `save_substitutes()`: Salva substitutos selecionados
- `get_saved_substitutes()`: Recupera substitutos salvos
- `create_backup()`: Cria backup automático

**Estrutura do Arquivo de Saída**:

```csv
n_iteracao,sub1_cod_produto,sub1_nome,sub1_preco,sub2_cod_produto,...
1,SHOP001,QUEIJO...,11.50,SHOP002,...
2,SHOP010,OVO...,15.99,,,
```

**Backups**:

- Criado antes de cada salvamento
- Formato: `substituicoes_backup_YYYYMMDD_HHMMSS.csv`
- Mantém últimos 10 backups
- Armazenado em `data/backups/`

---

### 5. `ui.py` - Interface Gráfica

**Responsabilidade**: Interface visual com CustomTkinter.

**Classes**:

- `SubstituteFinderUI`: Interface principal

**Componentes**:

1. **Frame Superior**: Produto original

   - Nome do produto (verde, destaque)
   - Preço (amarelo)

2. **Frame de Controle**: Navegação

   - Botões anterior/próximo
   - Campo de iteração
   - Busca manual
   - Botão pular

3. **Frame de Resultados**: Lista de produtos

   - Checkboxes para seleção
   - Código, nome, preço, score
   - Scrollable (suporta muitos resultados)

4. **Frame Inferior**: Ações
   - Contador de selecionados
   - Botões salvar / salvar e avançar

**Callbacks**:

```python
ui.set_callbacks(
    on_load_iteration=...,
    on_save_substitutes=...,
    on_search_manual=...,
    on_skip_iteration=...
)
```

**Threading**:

- Chamadas à IA executam em threads separadas
- Evita travar a interface
- Mostra tela de loading durante processamento

---

## 🔄 Fluxo de Dados

### Fluxo Normal (Automático)

```
1. Usuário abre programa
   ↓
2. FileManager carrega Base_Fazer.csv
   ↓
3. Primeira iteração é carregada
   ↓
4. Nome do produto vai para AIAgent
   ↓
5. GPT-4o gera 5 termos de busca
   ↓
6. DataProcessor busca nos Itens_Ativos
   ↓
7. Resultados aparecem na UI
   ↓
8. Usuário marca checkboxes (até 5)
   ↓
9. Clica "Salvar e Avançar"
   ↓
10. FileManager salva em substituicoes.csv
    ↓
11. Próxima iteração é carregada
    ↓
12. Repete até completar todos
```

### Fluxo Manual (Busca Personalizada)

```
1. Usuário digita termo no campo de busca
   ↓
2. DataProcessor busca diretamente
   (pula o AIAgent)
   ↓
3. Resultados aparecem na UI
   ↓
4. Continua normalmente...
```

---

## 🗄️ Estrutura de Dados

### Base_Fazer.csv (Input)

```csv
n_iteracao,id_modelo,cod_produto,nome,Fornecedor,Comprador,Responsável,Subcategoria
1,836,SHOP890,MANTEIGA COM SAL...,AVIAÇÃO,Geovanna,...,Refrigerados
```

**Colunas Usadas**:

- `n_iteracao`: Identificador único (1, 2, 3...)
- `nome`: Nome do produto para gerar termos
- `cod_produto`: Para excluir da busca de subs

### Itens_Ativos.csv (Catálogo)

```csv
id_modelo,cod_produto,nome,preco_loja_programada,preco_loja_fresh
3,SHOP01,ABSORVENTE...,10.99,,Jefferson
```

**Colunas Usadas**:

- `cod_produto`: Identificador único
- `nome`: Para busca textual
- `preco_loja_programada`: Preço de referência

### substituicoes.csv (Output)

```csv
n_iteracao,sub1_cod_produto,sub1_nome,sub1_preco,sub2_cod_produto,...
1,SHOP001,PRODUTO A,10.50,SHOP002,...
```

**Estrutura**:

- 1 linha por iteração
- Até 5 substitutos por linha
- Cada sub tem: código, nome, preço

### cache.json (Cache da IA)

```json
{
  "queijo ralado parmesão 50g": [
    "queijo ralado parmesao 50g",
    "queijo ralado parmesao",
    "queijo parmesao",
    "queijo ralado",
    "queijo"
  ]
}
```

---

## ⚙️ Configurações Importantes

### Temperatura da IA

`src/ai_agent.py`, linha ~90

```python
temperature=0.3  # 0=determinístico, 1=criativo
```

### Resultados Máximos

`src/data_processor.py`, linha ~70

```python
max_results=50  # Quantos produtos buscar
```

### Similaridade Mínima (Fuzzy)

`src/data_processor.py`, linha ~150

```python
min_similarity=60  # 0-100, threshold
```

### Backups Mantidos

`src/file_manager.py`, linha ~200

```python
max_backups=10  # Últimos N backups
```

---

## 🔐 Segurança e Performance

### Segurança

1. **API Key**: Armazenada em `.env` (não versionado)
2. **Backups**: Automáticos antes de cada salvamento
3. **Logs**: Registram todas as operações
4. **Validação**: Verifica arquivos antes de processar

### Performance

1. **Cache**: Evita chamadas repetidas à IA
2. **Threading**: IA não trava interface
3. **Normalização**: Texto pré-processado para busca rápida
4. **Sampling**: Fuzzy search em subset (não todo catálogo)
5. **Pandas**: Operações vetorizadas para velocidade

---

## 📊 Logs e Debug

### Estrutura de Logs

```
logs/
├── main.log           # Orquestração geral
├── ai_agent.log       # Chamadas à API, termos gerados
├── data_processor.log # Buscas, resultados
├── file_manager.log   # Operações com arquivos
└── ui.log            # Interações do usuário
```

### Formato

```
2025-10-15 14:32:01 - INFO - Carregando iteração 5
2025-10-15 14:32:02 - INFO - Termos gerados: ['queijo', 'ralado']
2025-10-15 14:32:03 - INFO - Encontrados 12 produtos
2025-10-15 14:32:10 - INFO - Salvos 3 substitutos para iteração 5
```

---

## 🚀 Otimizações Futuras

### Performance

- [ ] Indexação com Elasticsearch
- [ ] Cache distribuído (Redis)
- [ ] Processamento paralelo de lotes

### Funcionalidades

- [ ] Filtros avançados (marca, gramatura, categoria)
- [ ] Machine Learning para ranking
- [ ] Análise de histórico de vendas
- [ ] Sugestões baseadas em outros usuários

### Interface

- [ ] Modo escuro/claro
- [ ] Gráficos de progresso
- [ ] Export para Excel/PDF
- [ ] Atalhos de teclado personalizáveis

---

## 📞 Debugging

### Problema: IA não retorna resultados

**Verificar**: `logs/ai_agent.log`
**Possível causa**: API key inválida, limite de créditos

### Problema: Busca não encontra nada

**Verificar**: `logs/data_processor.log`
**Possível causa**: Termos muito específicos, normalização

### Problema: Arquivo não salva

**Verificar**: `logs/file_manager.log`
**Possível causa**: Permissões, disco cheio

### Problema: Interface trava

**Verificar**: Threading, logs de erro
**Possível causa**: Busca muito lenta, API timeout

---

**Desenvolvido para Shopper - Outubro 2025**
