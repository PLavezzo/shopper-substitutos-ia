#!/bin/bash

# Script de Setup Completo
# Execute: bash setup.sh

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  Shopper - Buscador de Substitutos                        ║"
echo "║  Setup Automático                                         ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Verificar Python
echo "🐍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "   Instale Python 3.8+ de: https://www.python.org/downloads/"
    exit 1
fi

python_version=$(python3 --version)
echo "✅ $python_version encontrado"
echo ""

# Criar ambiente virtual
echo "📦 Criando ambiente virtual..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Ambiente virtual criado"
else
    echo "ℹ️  Ambiente virtual já existe"
fi
echo ""

# Ativar ambiente virtual
echo "🔌 Ativando ambiente virtual..."
source .venv/bin/activate
echo "✅ Ambiente ativado"
echo ""

# Atualizar pip
echo "⬆️  Atualizando pip..."
pip install --upgrade pip --quiet
echo "✅ pip atualizado"
echo ""

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt --quiet
echo "✅ Dependências instaladas"
echo ""

# Verificar arquivos CSV
echo "📄 Verificando arquivos CSV..."
missing_files=0

if [ -f "Base_Fazer.csv" ]; then
    echo "✅ Base_Fazer.csv encontrado"
else
    echo "❌ Base_Fazer.csv NÃO encontrado"
    missing_files=1
fi

if [ -f "Itens_Ativos.csv" ]; then
    echo "✅ Itens_Ativos.csv encontrado"
else
    echo "❌ Itens_Ativos.csv NÃO encontrado"
    missing_files=1
fi
echo ""

if [ $missing_files -eq 1 ]; then
    echo "⚠️  ATENÇÃO: Alguns arquivos CSV estão faltando!"
    echo "   Coloque-os no diretório raiz antes de continuar"
    echo ""
fi

# Verificar/Criar .env
echo "🔑 Configurando .env..."
if [ ! -f ".env" ]; then
    echo "OPENAI_API_KEY=sk-proj-your-key-here" > .env
    echo "✅ Arquivo .env criado"
    echo ""
    echo "⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua chave da OpenAI!"
    echo ""
    echo "   Como obter a chave:"
    echo "   1. Acesse: https://platform.openai.com/api-keys"
    echo "   2. Faça login"
    echo "   3. Clique em 'Create new secret key'"
    echo "   4. Copie a chave"
    echo "   5. Cole no arquivo .env substituindo 'sk-proj-your-key-here'"
    echo ""
else
    echo "ℹ️  Arquivo .env já existe"
    
    # Verificar se a chave foi configurada
    if grep -q "your-key-here" .env; then
        echo "⚠️  ATENÇÃO: Chave da OpenAI ainda não foi configurada!"
        echo "   Edite o arquivo .env e adicione sua chave real"
        echo ""
    else
        echo "✅ Chave da OpenAI parece estar configurada"
    fi
fi
echo ""

# Criar diretórios
echo "📁 Criando diretórios necessários..."
mkdir -p data/backups
mkdir -p logs
echo "✅ Diretórios criados"
echo ""

# Executar teste
echo "🧪 Executando teste dos componentes..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python test_components.py
test_result=$?
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Resumo final
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  SETUP COMPLETO!                                          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Próximos passos:"
echo ""
echo "1. ✏️  Edite o arquivo .env com sua chave da OpenAI"
echo "      nano .env"
echo ""
echo "2. 🚀 Inicie a aplicação:"
echo "      python start.py"
echo ""
echo "   Ou manualmente:"
echo "      source .venv/bin/activate"
echo "      cd src"
echo "      python main.py"
echo ""
echo "📚 Documentação:"
echo "   • README.md         - Documentação completa"
echo "   • QUICKSTART.md     - Guia rápido"
echo "   • ARCHITECTURE.md   - Arquitetura técnica"
echo "   • PROJECT_SUMMARY.md - Resumo visual"
echo ""
echo "✨ Bom trabalho!"
echo ""
