"""
Exemplos de uso avançado do sistema
"""

# Exemplo 1: Testar apenas a IA sem iniciar interface
def test_ai_only():
    """Testa geração de termos pela IA"""
    from src.ai_agent import AIAgent
    
    agent = AIAgent()
    
    produtos_teste = [
        "QUEIJO RALADO FAIXA AZUL PARMESÃO 50G",
        "PÃO DE FORMA WICKBOLD INTEGRAL 450G",
        "OVO BRANCO MANTIQUEIRA C/ 12UN",
        "MANTEIGA COM SAL AVIAÇÃO LATA 200G"
    ]
    
    print("\n" + "="*60)
    print("TESTE DE GERAÇÃO DE TERMOS PELA IA")
    print("="*60)
    
    for produto in produtos_teste:
        print(f"\n📦 Produto: {produto}")
        print("   Termos gerados:")
        
        try:
            terms = agent.generate_search_terms(produto)
            for i, term in enumerate(terms, 1):
                print(f"   {i}. {term}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")


# Exemplo 2: Buscar produtos sem interface
def test_search_only():
    """Testa busca de produtos"""
    from src.data_processor import DataProcessor
    
    processor = DataProcessor("Itens_Ativos.csv")
    
    termos_teste = [
        ["queijo ralado parmesão 50g", "queijo ralado parmesão"],
        ["pão integral", "pão"],
        ["ovo branco", "ovo"]
    ]
    
    print("\n" + "="*60)
    print("TESTE DE BUSCA DE PRODUTOS")
    print("="*60)
    
    for termos in termos_teste:
        print(f"\n🔍 Buscando: {termos[0]}")
        
        results = processor.search_products(termos, max_results=5)
        
        if len(results) > 0:
            print(f"   Encontrados {len(results)} resultados:")
            for _, row in results.iterrows():
                print(f"   • {row['cod_produto']} - {row['nome'][:50]}... - R$ {row['preco_loja_programada']}")
        else:
            print("   ❌ Nenhum resultado encontrado")


# Exemplo 3: Processar lote de produtos automaticamente
def process_batch_auto(start_iteration: int, end_iteration: int, auto_select_top: int = 5):
    """
    Processa lote de produtos automaticamente
    Seleciona automaticamente os N melhores resultados
    
    ATENÇÃO: Use com cuidado! Revise os resultados depois.
    """
    from src.file_manager import FileManager
    from src.data_processor import DataProcessor
    from src.ai_agent import AIAgent
    
    fm = FileManager("Base_Fazer.csv")
    dp = DataProcessor("Itens_Ativos.csv")
    ai = AIAgent()
    
    print("\n" + "="*60)
    print(f"PROCESSAMENTO EM LOTE: Iterações {start_iteration} a {end_iteration}")
    print("="*60)
    
    for i in range(start_iteration, end_iteration + 1):
        print(f"\n[{i}/{end_iteration}] Processando...")
        
        # Pegar produto
        product = fm.get_item_by_iteration(i)
        if not product:
            print(f"   ⚠️  Iteração {i} não encontrada")
            continue
        
        product_name = product.get('nome', '')
        print(f"   📦 {product_name[:60]}...")
        
        # Verificar se já tem subs salvos
        saved = fm.get_saved_substitutes(i)
        if saved:
            print(f"   ℹ️  Já tem {len(saved)} subs salvos, pulando...")
            continue
        
        try:
            # Gerar termos
            terms = ai.generate_search_terms(product_name)
            print(f"   🤖 Termos: {', '.join(terms[:3])}...")
            
            # Buscar
            results = dp.search_products(
                terms,
                original_product_code=product.get('cod_produto'),
                max_results=20
            )
            
            if len(results) == 0:
                print("   ⚠️  Nenhum resultado, pulando...")
                fm.save_substitutes(i, [])
                continue
            
            # Selecionar top N automaticamente
            top_results = results.head(auto_select_top).to_dict('records')
            
            # Formatar para salvar
            subs_to_save = [
                {
                    'cod_produto': r['cod_produto'],
                    'nome': r['nome'],
                    'preco_loja_programada': r['preco_loja_programada']
                }
                for r in top_results
            ]
            
            # Salvar
            fm.save_substitutes(i, subs_to_save)
            print(f"   ✅ Salvos {len(subs_to_save)} subs")
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            continue
    
    print("\n" + "="*60)
    print("✅ Processamento em lote concluído!")
    print(f"Progresso total: {fm.get_completed_count()}/{fm.get_total_items()}")
    print("="*60)


# Exemplo 4: Exportar estatísticas
def export_statistics():
    """Gera estatísticas sobre o progresso"""
    from src.file_manager import FileManager
    import pandas as pd
    
    fm = FileManager("Base_Fazer.csv")
    
    print("\n" + "="*60)
    print("ESTATÍSTICAS DO PROJETO")
    print("="*60)
    
    total = fm.get_total_items()
    completed = fm.get_completed_count()
    percentage = fm.get_progress_percentage()
    
    print(f"\n📊 Progresso Geral:")
    print(f"   Total de itens: {total}")
    print(f"   Completos: {completed}")
    print(f"   Pendentes: {total - completed}")
    print(f"   Percentual: {percentage:.1f}%")
    
    # Análise de quantos subs por item
    if fm.df_output is not None:
        subs_counts = []
        for _, row in fm.df_output.iterrows():
            count = sum(1 for i in range(1, 6) if pd.notna(row.get(f'sub{i}_cod_produto')))
            subs_counts.append(count)
        
        print(f"\n📈 Distribuição de Substitutos:")
        for i in range(6):
            count = subs_counts.count(i)
            if count > 0:
                print(f"   {i} subs: {count} itens ({count/total*100:.1f}%)")
    
    print("="*60)


# Exemplo 5: Validar arquivo de saída
def validate_output():
    """Valida o arquivo de saída"""
    import pandas as pd
    
    print("\n" + "="*60)
    print("VALIDAÇÃO DO ARQUIVO DE SAÍDA")
    print("="*60)
    
    try:
        df = pd.read_csv("data/substituicoes.csv")
        
        print(f"\n✅ Arquivo carregado: {len(df)} linhas")
        
        # Verificar linhas sem substitutos
        empty = 0
        partial = 0
        full = 0
        
        for _, row in df.iterrows():
            count = sum(1 for i in range(1, 6) if pd.notna(row.get(f'sub{i}_cod_produto')))
            
            if count == 0:
                empty += 1
            elif count < 5:
                partial += 1
            else:
                full += 1
        
        print(f"\n📊 Status:")
        print(f"   Vazias (0 subs): {empty}")
        print(f"   Parciais (1-4 subs): {partial}")
        print(f"   Completas (5 subs): {full}")
        
        # Verificar duplicatas
        all_codes = []
        for _, row in df.iterrows():
            for i in range(1, 6):
                code = row.get(f'sub{i}_cod_produto')
                if pd.notna(code):
                    all_codes.append(code)
        
        unique_codes = len(set(all_codes))
        print(f"\n🔍 Códigos únicos usados: {unique_codes}")
        
        if len(all_codes) != unique_codes:
            print(f"   ⚠️  Há códigos duplicados: {len(all_codes) - unique_codes} repetições")
        
    except FileNotFoundError:
        print("❌ Arquivo data/substituicoes.csv não encontrado")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("="*60)


# Menu principal
if __name__ == "__main__":
    print("\n" + "="*60)
    print("EXEMPLOS DE USO AVANÇADO")
    print("="*60)
    print("\n1. Testar geração de termos pela IA")
    print("2. Testar busca de produtos")
    print("3. Processar lote automaticamente (CUIDADO!)")
    print("4. Exportar estatísticas")
    print("5. Validar arquivo de saída")
    print("0. Sair")
    
    choice = input("\nEscolha uma opção: ")
    
    if choice == "1":
        test_ai_only()
    elif choice == "2":
        test_search_only()
    elif choice == "3":
        start = int(input("Iteração inicial: "))
        end = int(input("Iteração final: "))
        top_n = int(input("Quantos subs auto-selecionar (1-5): "))
        
        confirm = input(f"\n⚠️  ATENÇÃO: Isto irá processar {end-start+1} itens automaticamente.\n   Tem certeza? (sim/não): ")
        if confirm.lower() == "sim":
            process_batch_auto(start, end, top_n)
        else:
            print("Cancelado.")
    elif choice == "4":
        export_statistics()
    elif choice == "5":
        validate_output()
    else:
        print("Até logo!")
