"""
Módulo para integração com OpenAI GPT-4o
Gera termos de pesquisa inteligentes para encontrar substitutos de produtos
"""

import os
import json
import logging
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# Configurar logging - caminho relativo ao diretório raiz do projeto
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=log_dir / 'ai_agent.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()


class AIAgent:
    """Agente de IA para gerar termos de busca de substitutos"""
    
    def __init__(self, cache_file: str = "data/cache.json"):
        """
        Inicializa o agente de IA
        
        Args:
            cache_file: Caminho para arquivo de cache
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.cache_file = cache_file
        self.cache = self._load_cache()
        
    def _load_cache(self) -> Dict:
        """Carrega cache de termos já processados"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Erro ao carregar cache: {e}")
                return {}
        return {}
    
    def _save_cache(self):
        """Salva cache em arquivo"""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Erro ao salvar cache: {e}")
    
    def generate_search_terms(self, product_name: str, price: str = "") -> List[str]:
        """
        Gera 5 termos de busca para encontrar substitutos do produto
        
        Args:
            product_name: Nome do produto original
            price: Preço do produto (opcional, para contexto)
            
        Returns:
            Lista com 5 termos de busca em ordem de generalidade
        """
        # Verificar cache primeiro
        cache_key = product_name.strip().lower()
        if cache_key in self.cache:
            logging.info(f"Usando cache para: {product_name}")
            return self.cache[cache_key]
        
        try:
            # Criar prompt para GPT-4o
            prompt = self._create_prompt(product_name, price)
            
            # Chamar API da OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """Você é um especialista em categorização de produtos de supermercado.
Sua tarefa é gerar termos de busca para encontrar substitutos de produtos.
Os substitutos devem ser da mesma categoria, podendo variar em marca, gramatura ou características específicas.
Retorne EXATAMENTE 5 termos, do mais específico ao mais genérico."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Processar resposta
            content = response.choices[0].message.content
            search_terms = self._parse_response(content)
            
            # Salvar no cache
            self.cache[cache_key] = search_terms
            self._save_cache()
            
            logging.info(f"Termos gerados para '{product_name}': {search_terms}")
            return search_terms
            
        except Exception as e:
            logging.error(f"Erro ao gerar termos para '{product_name}': {e}")
            # Fallback: gerar termos básicos
            return self._fallback_search_terms(product_name)
    
    def _create_prompt(self, product_name: str, price: str) -> str:
        """Cria o prompt para o GPT-4o"""
        prompt = f"""Produto: {product_name}"""
        if price:
            prompt += f"\nPreço: R$ {price}"
        
        prompt += """

Gere 5 termos de busca para encontrar substitutos deste produto em um catálogo de supermercado.

Regras:
1. Mantenha a categoria principal (ex: queijo, pão, ovo, etc)
2. Comece com termos mais específicos (incluindo marca, gramatura, características)
3. Vá generalizando gradualmente
4. O último termo deve ser o mais genérico possível (categoria + tipo)
5. NÃO inclua numeração, apenas liste os termos em linhas separadas
6. Mantenha informações importantes como: tipo do produto, gramatura aproximada, características especiais

Exemplo de saída (NÃO copie, apenas use como referência de formato):
queijo ralado parmesão 50g
queijo ralado parmesão
queijo parmesão ralado
queijo ralado
queijo

Agora gere os 5 termos para o produto acima:"""
        
        return prompt
    
    def _parse_response(self, content: str) -> List[str]:
        """
        Processa a resposta da IA e extrai os 5 termos
        
        Args:
            content: Resposta da API
            
        Returns:
            Lista com 5 termos de busca
        """
        lines = content.strip().split('\n')
        terms = []
        
        for line in lines:
            # Remover numeração, pontos, traços, etc
            cleaned = line.strip()
            cleaned = cleaned.lstrip('0123456789.-) ')
            
            if cleaned and len(cleaned) > 2:
                terms.append(cleaned.lower())
        
        # Garantir exatamente 5 termos
        if len(terms) < 5:
            # Se tiver menos, duplicar o mais genérico
            while len(terms) < 5:
                terms.append(terms[-1] if terms else "produto")
        elif len(terms) > 5:
            # Se tiver mais, pegar apenas os 5 primeiros
            terms = terms[:5]
        
        return terms
    
    def _fallback_search_terms(self, product_name: str) -> List[str]:
        """
        Gera termos básicos quando a IA falha
        
        Args:
            product_name: Nome do produto
            
        Returns:
            Lista com 5 termos básicos
        """
        # Limpar e separar palavras
        words = product_name.lower().split()
        
        # Remover palavras muito comuns
        stop_words = {'de', 'da', 'do', 'com', 'sem', 'para', 'c/', 'un', 'g', 'kg', 'ml', 'l'}
        meaningful_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        terms = []
        
        # Termo 1: produto completo
        terms.append(product_name.lower())
        
        # Termo 2: primeiras 4 palavras significativas
        if len(meaningful_words) >= 4:
            terms.append(' '.join(meaningful_words[:4]))
        else:
            terms.append(' '.join(meaningful_words))
        
        # Termo 3: primeiras 3 palavras significativas
        if len(meaningful_words) >= 3:
            terms.append(' '.join(meaningful_words[:3]))
        else:
            terms.append(' '.join(meaningful_words))
        
        # Termo 4: primeiras 2 palavras significativas
        if len(meaningful_words) >= 2:
            terms.append(' '.join(meaningful_words[:2]))
        else:
            terms.append(meaningful_words[0] if meaningful_words else product_name.lower())
        
        # Termo 5: primeira palavra significativa
        terms.append(meaningful_words[0] if meaningful_words else product_name.lower())
        
        # Garantir 5 termos únicos
        unique_terms = []
        for term in terms:
            if term not in unique_terms:
                unique_terms.append(term)
        
        while len(unique_terms) < 5:
            unique_terms.append(unique_terms[-1])
        
        return unique_terms[:5]


# Teste rápido
if __name__ == "__main__":
    agent = AIAgent()
    
    # Teste com exemplo
    test_product = "QUEIJO RALADO FAIXA AZUL PARMESÃO 50G"
    terms = agent.generate_search_terms(test_product, "10,99")
    
    print(f"\nProduto: {test_product}")
    print("\nTermos de busca gerados:")
    for i, term in enumerate(terms, 1):
        print(f"{i}. {term}")
