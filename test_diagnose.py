#!/usr/bin/env python3
"""
Teste EXTREMO de debug - vamos descobrir o que está bloqueando!
"""

import customtkinter as ctk
from src.ui import SubstituteFinderUI
import pandas as pd

print("=" * 70)
print("🔍 DIAGNÓSTICO COMPLETO - Descobrindo o bloqueio")
print("=" * 70)

# Cria dados falsos
fake_data = []
for i in range(50):
    fake_data.append({
        'cod_produto': f'PROD{i:03d}',
        'nome': f'Produto {i}',
        'preco_loja_programada': 10.50 + i,
        'score': 100 - i
    })

# Cria interface
root = ctk.CTk()
root.title("DIAGNÓSTICO - Scroll")
root.geometry("1000x700")

ui = SubstituteFinderUI(root)

# Injeta dados
results = fake_data
ui.display_results(results, [])

canvas = ui.scrollable_results._parent_canvas

print("\n📊 INFORMAÇÕES DO CANVAS:")
print(f"Canvas: {canvas}")
print(f"Canvas class: {canvas.__class__.__name__}")
print(f"Scrollbar: {ui.scrollable_results._scrollbar}")

# Lista TODOS os bindings ativos
print("\n🔗 BINDINGS ATIVOS:")
all_bindings = canvas.bind()
print(f"Canvas bindings: {all_bindings}")

frame_bindings = ui.scrollable_results.bind()
print(f"Frame bindings: {frame_bindings}")

# Tenta descobrir quem está capturando eventos
def trace_event(event):
    print(f"\n🎯 EVENTO CAPTURADO!")
    print(f"   Widget: {event.widget}")
    print(f"   Type: {event.type}")
    print(f"   Delta: {event.delta}")
    print(f"   X: {event.x}, Y: {event.y}")
    
    # Tenta rolar manualmente
    try:
        canvas.yview_scroll(-1 * event.delta, "units")
        print(f"   ✅ Scroll manual executado")
    except Exception as e:
        print(f"   ❌ Erro no scroll: {e}")

# Bind em TUDO para ver onde eventos vão
root.bind_all("<MouseWheel>", trace_event, add="+")

print("\n" + "=" * 70)
print("🎮 TESTE AGORA:")
print("=" * 70)
print("1. Use o trackpad na lista")
print("2. Observe o terminal - deve imprimir eventos capturados")
print("3. Se NÃO imprimir = macOS não está enviando eventos")
print("4. Se imprimir MAS não rolar = problema na função yview_scroll")
print("=" * 70)

root.mainloop()
