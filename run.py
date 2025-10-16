#!/usr/bin/env python3
"""
Script simples de inicialização - sem verificações
Use este para iniciar rapidamente quando tudo já estiver configurado
"""

import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importa e executa
from main import main

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Shopper - Buscador de Substitutos")
    print("=" * 60)
    print()
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Aplicação encerrada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
