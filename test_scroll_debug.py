#!/usr/bin/env python3
"""
Teste de DEBUG do Scroll - Mostra eventos em tempo real
"""

import customtkinter as ctk
from src.ui import SubstituteFinderUI
import pandas as pd

print("=" * 70)
print("🐛 TESTE DE DEBUG - Scroll com Eventos em Tempo Real")
print("=" * 70)

# Cria dados falsos
fake_data = []
for i in range(100):
    fake_data.append({
        'cod_produto': f'PROD{i:03d}',
        'nome': f'Produto Teste Número {i} - Item de Exemplo para Scroll',
        'preco_loja_programada': 10.50 + (i * 0.15),
        'score': 100 - i
    })

df = pd.DataFrame(fake_data)

# Cria interface
root = ctk.CTk()
root.title("DEBUG - Eventos de Scroll")
root.geometry("1000x700")

ui = SubstituteFinderUI(root)

# Injeta dados de teste - converte DataFrame para dict
results = df.to_dict('records')
ui.display_results(results, [])

# ===== ADICIONA DEBUG VISUAL =====
debug_label = ctk.CTkLabel(
    root,
    text="⏳ Aguardando scroll... Tente usar trackpad!",
    font=ctk.CTkFont(size=16, weight="bold"),
    text_color="#FFA500"
)
debug_label.pack(pady=10)

event_counter = {'count': 0}

def debug_scroll(event):
    """Intercepta e mostra eventos de scroll"""
    event_counter['count'] += 1
    debug_label.configure(
        text=f"🎯 Evento #{event_counter['count']}: delta={event.delta}, x={event.x}, y={event.y}",
        text_color="#00FF00"
    )
    print(f"📊 Scroll Event: delta={event.delta}, type={event.type}, widget={event.widget}")

# Vincula debug ao canvas
canvas = ui.scrollable_results._parent_canvas
canvas.bind("<MouseWheel>", debug_scroll, add="+")
ui.scrollable_results.bind("<MouseWheel>", debug_scroll, add="+")

print("\n" + "=" * 70)
print("🎮 INSTRUÇÕES:")
print("=" * 70)
print("1. A janela vai abrir com 100 produtos")
print("2. Mova o mouse SOBRE a lista")
print("3. Use o trackpad com DOIS DEDOS para cima/baixo")
print("4. Você verá mensagens em VERDE quando eventos forem detectados")
print("5. Se NÃO aparecer nada verde = eventos não estão chegando")
print("=" * 70)
print()

root.mainloop()
