"""
Módulo para gerenciamento de arquivos CSV
Carrega Base_Fazer, salva seleções, gerencia backups
"""

import pandas as pd
import os
import shutil
import logging
from datetime import datetime
from typing import Dict, List, Tuple
from pathlib import Path

# Configurar logging - caminho relativo ao diretório raiz do projeto
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=log_dir / 'file_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class FileManager:
    """Gerencia operações com arquivos CSV"""
    
    def __init__(
        self,
        base_fazer_path: str,
        output_path: str = "data/substituicoes.csv",
        backup_dir: str = "data/backups"
    ):
        """
        Inicializa o gerenciador de arquivos
        
        Args:
            base_fazer_path: Caminho para Base_Fazer.csv
            output_path: Caminho para arquivo de saída
            backup_dir: Diretório para backups
        """
        self.base_fazer_path = base_fazer_path
        self.output_path = output_path
        self.backup_dir = backup_dir
        
        self.df_base_fazer = None
        self.df_output = None
        
        os.makedirs(backup_dir, exist_ok=True)
        
        self.load_base_fazer()
        self.load_or_create_output()
    
    def load_base_fazer(self):
        """Carrega o CSV Base_Fazer"""
        try:
            # Tentar ler pulando a primeira linha (metadados)
            self.df_base_fazer = pd.read_csv(self.base_fazer_path, skiprows=1)
            
            # Garantir que n_iteracao existe e está preenchido
            if 'n_iteracao' not in self.df_base_fazer.columns:
                raise ValueError("Coluna 'n_iteracao' não encontrada em Base_Fazer")
            
            # Converter n_iteracao para int
            self.df_base_fazer['n_iteracao'] = pd.to_numeric(
                self.df_base_fazer['n_iteracao'], 
                errors='coerce'
            ).fillna(0).astype(int)
            
            # Remover linhas sem n_iteracao válido
            self.df_base_fazer = self.df_base_fazer[self.df_base_fazer['n_iteracao'] > 0]
            
            logging.info(f"Base_Fazer carregado: {len(self.df_base_fazer)} itens")
            
        except Exception as e:
            logging.error(f"Erro ao carregar Base_Fazer: {e}")
            raise
    
    def load_or_create_output(self):
        """Carrega arquivo de saída ou cria um novo"""
        if os.path.exists(self.output_path):
            try:
                self.df_output = pd.read_csv(self.output_path)
                logging.info(f"Arquivo de saída carregado: {len(self.df_output)} linhas")
            except Exception as e:
                logging.error(f"Erro ao carregar arquivo de saída: {e}")
                self._create_new_output()
        else:
            self._create_new_output()
    
    def _create_new_output(self):
        """Cria novo arquivo de saída vazio com estrutura correta"""
        # Criar DataFrame com todas as linhas de Base_Fazer
        max_iteracao = self.df_base_fazer['n_iteracao'].max()
        
        # Inicializar com n_iteracao
        data = {'n_iteracao': range(1, max_iteracao + 1)}
        
        # Adicionar 5 colunas para cada substituto (cod, nome, preco)
        for i in range(1, 6):
            data[f'sub{i}_cod_produto'] = [None] * max_iteracao
            data[f'sub{i}_nome'] = [None] * max_iteracao
            data[f'sub{i}_preco_loja_programada'] = [None] * max_iteracao
        
        self.df_output = pd.DataFrame(data)
        
        # Salvar arquivo inicial
        self.save_output()
        
        logging.info(f"Novo arquivo de saída criado com {max_iteracao} linhas")
    
    def get_item_by_iteration(self, n_iteracao: int) -> Dict:
        """
        Retorna item da Base_Fazer por número de iteração
        
        Args:
            n_iteracao: Número da iteração
            
        Returns:
            Dicionário com dados do item ou None
        """
        result = self.df_base_fazer[self.df_base_fazer['n_iteracao'] == n_iteracao]
        
        if len(result) > 0:
            return result.iloc[0].to_dict()
        
        return None
    
    def get_saved_substitutes(self, n_iteracao: int) -> List[Dict]:
        """
        Retorna substitutos já salvos para uma iteração
        
        Args:
            n_iteracao: Número da iteração
            
        Returns:
            Lista de dicionários com substitutos salvos
        """
        if self.df_output is None or n_iteracao < 1:
            return []
        
        # Buscar linha correspondente (n_iteracao -1 porque index começa em 0)
        if n_iteracao > len(self.df_output):
            return []
        
        row = self.df_output[self.df_output['n_iteracao'] == n_iteracao]
        
        if len(row) == 0:
            return []
        
        row = row.iloc[0]
        substitutes = []
        
        # Extrair até 5 substitutos
        for i in range(1, 6):
            cod_key = f'sub{i}_cod_produto'
            nome_key = f'sub{i}_nome'
            preco_key = f'sub{i}_preco_loja_programada'
            
            if cod_key in row and pd.notna(row[cod_key]):
                substitutes.append({
                    'cod_produto': row[cod_key],
                    'nome': row[nome_key] if pd.notna(row[nome_key]) else '',
                    'preco_loja_programada': row[preco_key] if pd.notna(row[preco_key]) else ''
                })
        
        return substitutes
    
    def save_substitutes(self, n_iteracao: int, substitutes: List[Dict]):
        """
        Salva substitutos selecionados para uma iteração
        
        Args:
            n_iteracao: Número da iteração
            substitutes: Lista com até 5 substitutos (dicts com cod_produto, nome, preco)
        """
        if n_iteracao < 1 or n_iteracao > len(self.df_output):
            logging.error(f"Iteração inválida: {n_iteracao}")
            return
        
        # Criar backup antes de salvar
        self.create_backup()
        
        # Encontrar índice da linha (n_iteracao é 1-indexed, mas pode não corresponder ao index)
        row_index = self.df_output[self.df_output['n_iteracao'] == n_iteracao].index
        
        if len(row_index) == 0:
            logging.error(f"Linha não encontrada para iteração {n_iteracao}")
            return
        
        row_index = row_index[0]
        
        # Limpar substitutos existentes
        for i in range(1, 6):
            self.df_output.at[row_index, f'sub{i}_cod_produto'] = None
            self.df_output.at[row_index, f'sub{i}_nome'] = None
            self.df_output.at[row_index, f'sub{i}_preco_loja_programada'] = None
        
        # Salvar novos substitutos (até 5)
        for i, sub in enumerate(substitutes[:5], start=1):
            self.df_output.at[row_index, f'sub{i}_cod_produto'] = sub.get('cod_produto', '')
            self.df_output.at[row_index, f'sub{i}_nome'] = sub.get('nome', '')
            self.df_output.at[row_index, f'sub{i}_preco_loja_programada'] = sub.get('preco_loja_programada', '')
        
        # Salvar arquivo
        self.save_output()
        
        logging.info(f"Salvos {len(substitutes)} substitutos para iteração {n_iteracao}")
    
    def save_output(self):
        """Salva o arquivo de saída"""
        try:
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            self.df_output.to_csv(self.output_path, index=False)
            logging.info(f"Arquivo de saída salvo: {self.output_path}")
        except Exception as e:
            logging.error(f"Erro ao salvar arquivo de saída: {e}")
    
    def create_backup(self):
        """Cria backup do arquivo de saída"""
        if not os.path.exists(self.output_path):
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"substituicoes_backup_{timestamp}.csv"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            shutil.copy2(self.output_path, backup_path)
            
            # Manter apenas últimos 10 backups
            self._cleanup_old_backups(max_backups=10)
            
            logging.info(f"Backup criado: {backup_path}")
            
        except Exception as e:
            logging.error(f"Erro ao criar backup: {e}")
    
    def _cleanup_old_backups(self, max_backups: int = 10):
        """Remove backups antigos, mantendo apenas os mais recentes"""
        try:
            backups = [
                f for f in os.listdir(self.backup_dir) 
                if f.startswith('substituicoes_backup_') and f.endswith('.csv')
            ]
            
            if len(backups) <= max_backups:
                return
            
            # Ordenar por data de modificação
            backups.sort(
                key=lambda x: os.path.getmtime(os.path.join(self.backup_dir, x)),
                reverse=True
            )
            
            # Remover backups mais antigos
            for backup in backups[max_backups:]:
                os.remove(os.path.join(self.backup_dir, backup))
                logging.info(f"Backup antigo removido: {backup}")
                
        except Exception as e:
            logging.error(f"Erro ao limpar backups antigos: {e}")
    
    def get_total_items(self) -> int:
        """Retorna total de itens na Base_Fazer"""
        return len(self.df_base_fazer) if self.df_base_fazer is not None else 0
    
    def get_completed_count(self) -> int:
        """Retorna quantidade de iterações já preenchidas"""
        if self.df_output is None:
            return 0
        
        # Contar linhas que têm pelo menos 1 substituto
        count = 0
        for _, row in self.df_output.iterrows():
            if pd.notna(row.get('sub1_cod_produto')):
                count += 1
        
        return count
    
    def get_progress_percentage(self) -> float:
        """Retorna percentual de progresso"""
        total = self.get_total_items()
        completed = self.get_completed_count()
        
        if total == 0:
            return 0.0
        
        return (completed / total) * 100


# Teste rápido
if __name__ == "__main__":
    fm = FileManager("../Base_Fazer.csv")
    
    # Teste: pegar item da iteração 1
    item = fm.get_item_by_iteration(1)
    print(f"\nItem da iteração 1:")
    print(f"Nome: {item.get('nome')}")
    
    # Teste: progresso
    print(f"\nTotal: {fm.get_total_items()}")
    print(f"Completos: {fm.get_completed_count()}")
    print(f"Progresso: {fm.get_progress_percentage():.1f}%")
