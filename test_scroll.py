"""
Teste visual do scroll
Abre interface apenas com a lista de resultados para testar scroll
"""

import customtkinter as ctk
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ui import SubstituteFinderUI

print("="*60)
print("TESTE DE SCROLL - VERSÃO CORRIGIDA")
print("="*60)
print()
print("Abrindo interface de teste...")
print()

# Criar janela de teste
root = ctk.CTk()
app = SubstituteFinderUI(root)

# Produto de teste
test_product = {
    'nome': 'TESTE DE SCROLL - Mova o mouse sobre a lista e role com trackpad',
    'preco_loja_programada': '10,99'
}
app.display_product(test_product)

# Gerar 100 resultados para testar o scroll
print("Gerando 100 produtos de teste...")
test_results = []
for i in range(1, 101):
    test_results.append({
        'cod_produto': f'TEST{i:03d}',
        'nome': f'Produto de Teste #{i:03d} - ' + ('A' * 40) + f' - Linha {i}',
        'preco_loja_programada': f'{i % 50 + 1},{99 - (i % 100):02d}',
        'score': 95 - (i % 40)
    })

app.display_results(test_results)
app.update_progress(50, 100)

print("✅ Interface aberta com 100 itens")
print()
print("="*60)
print("INSTRUÇÕES DE TESTE:")
print("="*60)
print()
print("1. Mova o CURSOR DO MOUSE sobre a lista de resultados")
print("   (Isso é importante! O scroll só funciona com mouse sobre a lista)")
print()
print("2. Use o TRACKPAD com DOIS DEDOS para rolar")
print()
print("3. Se funcionar, você verá todos os 100 produtos!")
print("   - Primeiro: 'Produto de Teste #001'")
print("   - Último: 'Produto de Teste #100'")
print()
print("4. Feche a janela quando terminar o teste")
print()
print("="*60)
print()

root.mainloop()

print()
print("Teste finalizado!")
