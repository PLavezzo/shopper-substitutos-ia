#!/usr/bin/env python3
"""
Script de inicialização rápida
Verifica dependências e inicia a aplicação
"""

import subprocess
import sys
import os

def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ é necessário")
        print(f"   Você está usando Python {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")

def check_dependencies():
    """Verifica e instala dependências"""
    print("\n📦 Verificando dependências...")
    
    required = {
        'pandas': 'pandas',
        'openai': 'openai',
        'customtkinter': 'customtkinter',
        'dotenv': 'python-dotenv',
        'fuzzywuzzy': 'fuzzywuzzy'
    }
    
    missing = []
    
    for module, package in required.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (faltando)")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Faltam {len(missing)} dependência(s)")
        print("   Execute: pip install -r requirements.txt")
        print("   Ou ative o ambiente virtual: source .venv/bin/activate")
        sys.exit(1)

def check_env_file():
    """Verifica arquivo .env"""
    print("\n🔑 Verificando configuração...")
    
    if not os.path.exists('.env'):
        print("   ⚠️  Arquivo .env não encontrado")
        print("\n   AVISO: A funcionalidade de IA não funcionará sem a chave OpenAI")
        print("   Para usar IA, crie um arquivo .env com:")
        print("   OPENAI_API_KEY=sua_chave_aqui")
        print("\n   Continuando em modo manual...")
    else:
        print("   ✅ .env encontrado")

def check_csv_files():
    """Verifica arquivos CSV"""
    print("\n📄 Verificando arquivos CSV...")
    
    files_ok = True
    
    if os.path.exists('Base_Fazer.csv'):
        print("   ✅ Base_Fazer.csv")
    else:
        print("   ❌ Base_Fazer.csv (não encontrado)")
        files_ok = False
    
    if os.path.exists('Itens_Ativos.csv'):
        print("   ✅ Itens_Ativos.csv")
    else:
        print("   ❌ Itens_Ativos.csv (não encontrado)")
        files_ok = False
    
    if not files_ok:
        print("\n❌ Arquivos CSV necessários não encontrados!")
        print("   Coloque os arquivos no diretório raiz do projeto")
        sys.exit(1)

def create_directories():
    """Cria diretórios necessários"""
    dirs = ['data', 'data/backups', 'logs']
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def start_app():
    """Inicia a aplicação"""
    print("\n" + "="*60)
    print("🚀 Iniciando Shopper - Buscador de Substitutos")
    print("="*60)
    print()
    
    try:
        os.chdir('src')
        subprocess.run([sys.executable, 'main.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Aplicação encerrada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar: {e}")
        sys.exit(1)

def main():
    """Função principal"""
    print("="*60)
    print("Shopper - Verificação de Sistema")
    print("="*60)
    
    check_python_version()
    check_dependencies()
    check_env_file()
    check_csv_files()
    create_directories()
    
    print("\n✅ Todas as verificações passaram!")
    
    start_app()

if __name__ == "__main__":
    main()
