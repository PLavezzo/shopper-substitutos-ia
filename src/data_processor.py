"""
Módulo para processamento e busca de dados nos CSVs
Realiza buscas inteligentes nos Itens_Ativos usando os termos gerados pela IA
"""

import pandas as pd
import re
import unicodedata
import logging
from typing import List, Dict, Tuple
from fuzzywuzzy import fuzz

logging.basicConfig(
    filename='logs/data_processor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class DataProcessor:
    """Processa e busca dados nos CSVs"""
    
    def __init__(self, itens_ativos_path: str):
        """
        Inicializa o processador de dados
        
        Args:
            itens_ativos_path: Caminho para o CSV com itens disponíveis
        """
        self.itens_ativos_path = itens_ativos_path
        self.df_ativos = None
        self.load_itens_ativos()
        
    def load_itens_ativos(self):
        """Carrega o CSV de itens ativos e faz pré-processamento"""
        try:
            # Ler CSV
            self.df_ativos = pd.read_csv(self.itens_ativos_path)
            
            # Limpar colunas vazias no final
            self.df_ativos = self.df_ativos.dropna(how='all', axis=1)
            
            # Remover linhas completamente vazias
            self.df_ativos = self.df_ativos.dropna(how='all')
            
            # Garantir que as colunas necessárias existem
            required_cols = ['cod_produto', 'nome', 'preco_loja_programada']
            for col in required_cols:
                if col not in self.df_ativos.columns:
                    raise ValueError(f"Coluna '{col}' não encontrada no CSV")
            
            # Criar coluna normalizada para busca mais eficiente
            self.df_ativos['nome_normalizado'] = self.df_ativos['nome'].apply(
                lambda x: self.normalize_text(str(x)) if pd.notna(x) else ""
            )
            
            # Remover duplicatas por cod_produto (manter primeira ocorrência)
            self.df_ativos = self.df_ativos.drop_duplicates(subset=['cod_produto'], keep='first')
            
            logging.info(f"Carregados {len(self.df_ativos)} itens ativos")
            
        except Exception as e:
            logging.error(f"Erro ao carregar itens ativos: {e}")
            raise
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normaliza texto para busca: remove acentos, converte para minúscula,
        remove caracteres especiais
        
        Args:
            text: Texto para normalizar
            
        Returns:
            Texto normalizado
        """
        if not text:
            return ""
        
        # Converter para minúscula
        text = text.lower()
        
        # Remover acentos
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ASCII', 'ignore').decode('ASCII')
        
        # Manter apenas letras, números e espaços
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # Remover espaços múltiplos
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def search_products(
        self, 
        search_terms: List[str], 
        original_product_code: str = None,
        max_results: int = 50,
        min_similarity: int = 60
    ) -> pd.DataFrame:
        """
        Busca produtos usando os termos de pesquisa
        
        Args:
            search_terms: Lista de termos para buscar
            original_product_code: Código do produto original (para excluir da busca)
            max_results: Número máximo de resultados
            min_similarity: Similaridade mínima (0-100) para busca fuzzy
            
        Returns:
            DataFrame com resultados encontrados
        """
        all_results = []
        seen_codes = set()
        
        # Se tiver código original, adicionar ao set de códigos vistos
        if original_product_code:
            seen_codes.add(original_product_code)
        
        # Buscar com cada termo, do mais específico ao mais genérico
        for i, term in enumerate(search_terms):
            if not term:
                continue
                
            term_normalized = self.normalize_text(term)
            
            # Busca exata primeiro
            exact_matches = self.df_ativos[
                self.df_ativos['nome_normalizado'].str.contains(
                    term_normalized, 
                    case=False, 
                    na=False, 
                    regex=False
                )
            ].copy()
            
            # Adicionar score e termo usado
            exact_matches['score'] = 100 - (i * 5)  # Penalizar termos mais genéricos
            exact_matches['termo_usado'] = term
            exact_matches['tipo_match'] = 'exato'
            
            # Adicionar ao resultado se não foi visto antes
            for _, row in exact_matches.iterrows():
                if row['cod_produto'] not in seen_codes:
                    seen_codes.add(row['cod_produto'])
                    all_results.append(row)
            
            # Se já temos resultados suficientes, parar
            if len(all_results) >= max_results:
                break
        
        # Se não encontrou resultados suficientes, fazer busca fuzzy
        if len(all_results) < max_results and search_terms:
            fuzzy_results = self._fuzzy_search(
                search_terms[0],  # Usar termo mais específico
                seen_codes,
                max_results - len(all_results),
                min_similarity
            )
            all_results.extend(fuzzy_results)
        
        # Converter para DataFrame
        if all_results:
            df_results = pd.DataFrame(all_results)
            
            # Ordenar por score (maior primeiro)
            df_results = df_results.sort_values('score', ascending=False)
            
            # Limitar resultados
            df_results = df_results.head(max_results)
            
            # Selecionar apenas colunas relevantes
            columns_to_show = [
                'cod_produto', 
                'nome', 
                'preco_loja_programada',
                'score',
                'termo_usado',
                'tipo_match'
            ]
            df_results = df_results[columns_to_show]
            
            logging.info(f"Encontrados {len(df_results)} produtos para termos: {search_terms[:3]}")
            return df_results
        else:
            logging.warning(f"Nenhum produto encontrado para: {search_terms}")
            return pd.DataFrame(columns=[
                'cod_produto', 
                'nome', 
                'preco_loja_programada',
                'score',
                'termo_usado',
                'tipo_match'
            ])
    
    def _fuzzy_search(
        self,
        term: str,
        exclude_codes: set,
        max_results: int,
        min_similarity: int
    ) -> List:
        """
        Busca fuzzy (aproximada) quando busca exata não encontra resultados
        
        Args:
            term: Termo para buscar
            exclude_codes: Códigos de produtos já encontrados
            max_results: Número máximo de resultados
            min_similarity: Similaridade mínima (0-100)
            
        Returns:
            Lista de resultados encontrados
        """
        term_normalized = self.normalize_text(term)
        results = []
        
        # Amostrar subset para não processar tudo (performance)
        sample_size = min(1000, len(self.df_ativos))
        df_sample = self.df_ativos.sample(n=sample_size, random_state=42)
        
        for _, row in df_sample.iterrows():
            if row['cod_produto'] in exclude_codes:
                continue
            
            # Calcular similaridade
            similarity = fuzz.partial_ratio(term_normalized, row['nome_normalizado'])
            
            if similarity >= min_similarity:
                row_dict = row.to_dict()
                row_dict['score'] = similarity
                row_dict['termo_usado'] = term
                row_dict['tipo_match'] = 'fuzzy'
                results.append(row_dict)
        
        # Ordenar por similaridade
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:max_results]
    
    def get_product_by_code(self, cod_produto: str) -> Dict:
        """
        Busca um produto específico pelo código
        
        Args:
            cod_produto: Código do produto
            
        Returns:
            Dicionário com dados do produto ou None se não encontrado
        """
        result = self.df_ativos[self.df_ativos['cod_produto'] == cod_produto]
        
        if len(result) > 0:
            return result.iloc[0].to_dict()
        
        return None
    
    def filter_by_price_range(
        self,
        df: pd.DataFrame,
        reference_price: str,
        margin_percent: float = 30.0
    ) -> pd.DataFrame:
        """
        Filtra produtos por faixa de preço
        
        Args:
            df: DataFrame com produtos
            reference_price: Preço de referência (formato "10,99")
            margin_percent: Margem percentual aceitável (padrão 30%)
            
        Returns:
            DataFrame filtrado
        """
        try:
            # Converter preço de referência
            ref_price = float(reference_price.replace(',', '.'))
            
            # Calcular limites
            min_price = ref_price * (1 - margin_percent / 100)
            max_price = ref_price * (1 + margin_percent / 100)
            
            # Converter preços do DataFrame
            def parse_price(price_str):
                try:
                    if pd.isna(price_str):
                        return 0.0
                    return float(str(price_str).replace(',', '.'))
                except:
                    return 0.0
            
            df['preco_numerico'] = df['preco_loja_programada'].apply(parse_price)
            
            # Filtrar
            df_filtered = df[
                (df['preco_numerico'] >= min_price) & 
                (df['preco_numerico'] <= max_price)
            ].copy()
            
            # Remover coluna temporária
            df_filtered = df_filtered.drop(columns=['preco_numerico'])
            
            return df_filtered
            
        except Exception as e:
            logging.error(f"Erro ao filtrar por preço: {e}")
            return df


# Teste rápido
if __name__ == "__main__":
    processor = DataProcessor("../Itens_Ativos.csv")
    
    # Teste de busca
    terms = ["queijo ralado parmesão 50g", "queijo ralado parmesão", "queijo ralado"]
    results = processor.search_products(terms, max_results=10)
    
    print(f"\nEncontrados {len(results)} produtos:")
    print(results[['cod_produto', 'nome', 'preco_loja_programada', 'score']].to_string())
