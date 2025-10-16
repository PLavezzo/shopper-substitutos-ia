"""
Script de teste rápido dos componentes principais
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("="*60)
print("Teste dos Componentes")
print("="*60)

# Teste 1: FileManager
print("\n1. Testando FileManager...")
try:
    from src.file_manager import FileManager
    fm = FileManager("Base_Fazer.csv")
    
    total = fm.get_total_items()
    print(f"   ✅ Base_Fazer carregado: {total} itens")
    
    item = fm.get_item_by_iteration(1)
    if item:
        print(f"   ✅ Item 1: {item.get('nome', 'N/A')[:50]}...")
    
except Exception as e:
    print(f"   ❌ Erro: {e}")

# Teste 2: DataProcessor
print("\n2. Testando DataProcessor...")
try:
    from src.data_processor import DataProcessor
    dp = DataProcessor("Itens_Ativos.csv")
    
    print(f"   ✅ Itens_Ativos carregado: {len(dp.df_ativos)} produtos")
    
    # Teste de busca
    results = dp.search_products(["queijo ralado"], max_results=5)
    print(f"   ✅ Busca teste retornou {len(results)} resultados")
    
except Exception as e:
    print(f"   ❌ Erro: {e}")

# Teste 3: AIAgent (sem fazer chamada real)
print("\n3. Testando AIAgent...")
try:
    from src.ai_agent import AIAgent
    agent = AIAgent()
    
    # Testar fallback (sem chamar API)
    terms = agent._fallback_search_terms("QUEIJO RALADO PARMESÃO 50G")
    print(f"   ✅ Fallback gera {len(terms)} termos")
    print(f"   Exemplo: {terms[0]}")
    
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n" + "="*60)
print("✅ Testes básicos concluídos!")
print("\nPara iniciar o programa completo:")
print("  python start.py")
print("\nOu diretamente:")
print("  cd src && python main.py")
print("="*60)
