# 🔄 Notas de Atualização

## Versão 1.1 - 15/10/2025

### ✅ Correções Implementadas

#### 1. **Preço do Produto Original Agora Aparece**

- **Problema**: O preço do produto a ser analisado não estava sendo exibido
- **Causa**: O arquivo `Base_Fazer.csv` não contém a coluna de preço
- **Solução**: Sistema agora busca o preço automaticamente no `Itens_Ativos.csv` usando o código do produto
- **Arquivo**: `src/main.py` - função `load_iteration()`

**Como funciona agora:**

```python
1. Carrega produto do Base_Fazer (sem preço)
2. Busca o cod_produto nos Itens_Ativos
3. Puxa o preço de lá
4. Exibe na interface
```

#### 2. **Scroll do Trackpad no Mac Funcionando**

- **Problema**: Scroll com trackpad do Mac não funcionava na lista de resultados
- **Causa**: Bug no CustomTkinter 5.2.2 - eventos de scroll não são vinculados automaticamente no macOS
- **Solução**: Implementado sistema de vinculação manual de eventos ao canvas interno com detecção de plataforma
- **Arquivo**: `src/ui.py` - novo método `_setup_scroll()`

**Como funciona agora:**

```python
1. Detecta automaticamente o sistema operacional
2. Vincula eventos MouseWheel ao canvas interno do ScrollableFrame
3. Ativa/desativa scroll quando mouse entra/sai da área
4. Funciona em Mac (delta -1/1), Windows (delta 120/-120) e Linux (Button-4/5)
```

**⚠️ IMPORTANTE**: Mova o cursor do mouse SOBRE a lista de resultados antes de rolar!

- ✅ Trackpad com dois dedos funcionando

---

## Como Atualizar

Se você já estava usando a versão anterior:

```bash
# 1. Simplesmente execute novamente
python start.py

# Ou
cd src && python main.py
```

Não precisa reinstalar nada! As correções já estão no código.

---

## O Que Foi Modificado

### Arquivos Alterados:

1. **`src/main.py`**

   - Adicionada busca de preço no `Itens_Ativos`
   - Logs informativos sobre preço encontrado/não encontrado

2. **`src/ui.py`**
   - Adicionado método `_configure_mac_scroll()`
   - Configuração automática de eventos de scroll para macOS

---

## Testado e Funcionando

✅ Preço aparece corretamente no topo  
✅ Scroll com trackpad funciona perfeitamente  
✅ Testes automatizados passando  
✅ Compatível com Mac, Linux e Windows

---

## Próximas Melhorias Planejadas

- [ ] Filtro por faixa de preço
- [ ] Atalhos de teclado (Ctrl+S para salvar)
- [ ] Duplo clique para selecionar item
- [ ] Indicador visual de qual produto já foi processado
- [ ] Export para Excel além de CSV

---

## Reportar Problemas

Se encontrar algum bug:

1. Verifique os logs em `logs/main.log`
2. Execute `python test_components.py`
3. Anote o erro e os passos para reproduzir

---

**Versão**: 1.1  
**Data**: 15 de outubro de 2025  
**Status**: ✅ Estável e testado
