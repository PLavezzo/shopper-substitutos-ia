"""
Arquivo principal - Orquestra toda a aplicação
Integra IA, processamento de dados, gerenciamento de arquivos e interface
"""

import customtkinter as ctk
import sys
import os
import logging
import threading
from typing import List, Dict

# Adicionar diretório src ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_agent import AIAgent
from data_processor import DataProcessor
from file_manager import FileManager
from ui import SubstituteFinderUI

# Configurar logging principal
logging.basicConfig(
    filename='logs/main.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class SubstituteFinderApp:
    """Aplicação principal - controlador"""
    
    def __init__(self):
        """Inicializa a aplicação"""
        
        # Paths dos arquivos
        self.base_fazer_path = "Base_Fazer.csv"
        self.itens_ativos_path = "Itens_Ativos.csv"
        
        # Verificar se arquivos existem
        self._check_files()
        
        # Inicializar componentes
        logging.info("Inicializando componentes...")
        
        try:
            self.file_manager = FileManager(self.base_fazer_path)
            self.data_processor = DataProcessor(self.itens_ativos_path)
            self.ai_agent = AIAgent()
            
            logging.info("Componentes inicializados com sucesso")
            
        except Exception as e:
            logging.error(f"Erro ao inicializar componentes: {e}")
            print(f"ERRO: Não foi possível inicializar a aplicação: {e}")
            sys.exit(1)
        
        # Criar interface
        self.root = ctk.CTk()
        self.ui = SubstituteFinderUI(self.root)
        
        # Conectar callbacks
        self.ui.set_callbacks(
            on_load_iteration=self.load_iteration,
            on_save_substitutes=self.save_substitutes,
            on_search_manual=self.manual_search,
            on_skip_iteration=self.skip_iteration
        )
        
        # Carregar primeira iteração
        self.current_product = None
        self.current_search_results = []
        
        # Atualizar progresso inicial
        self._update_progress()
        
        # Carregar primeira iteração
        self.load_iteration(1)
    
    def _check_files(self):
        """Verifica se os arquivos CSV existem"""
        if not os.path.exists(self.base_fazer_path):
            print(f"ERRO: Arquivo '{self.base_fazer_path}' não encontrado!")
            print("Certifique-se de que o arquivo está no mesmo diretório do script.")
            sys.exit(1)
        
        if not os.path.exists(self.itens_ativos_path):
            print(f"ERRO: Arquivo '{self.itens_ativos_path}' não encontrado!")
            print("Certifique-se de que o arquivo está no mesmo diretório do script.")
            sys.exit(1)
    
    def load_iteration(self, iteration_num: int):
        """
        Carrega uma iteração específica
        
        Args:
            iteration_num: Número da iteração
        """
        logging.info(f"Carregando iteração {iteration_num}")
        
        # Buscar produto da Base_Fazer
        product = self.file_manager.get_item_by_iteration(iteration_num)
        
        if product is None:
            self.ui.show_message(
                "Aviso",
                f"Iteração {iteration_num} não encontrada."
            )
            return
        
        # Buscar preço do produto nos Itens_Ativos
        cod_produto = product.get('cod_produto')
        if cod_produto:
            product_details = self.data_processor.get_product_by_code(cod_produto)
            if product_details and 'preco_loja_programada' in product_details:
                product['preco_loja_programada'] = product_details['preco_loja_programada']
                logging.info(f"Preço encontrado: R$ {product['preco_loja_programada']}")
            else:
                logging.warning(f"Produto {cod_produto} não encontrado nos Itens_Ativos")
                product['preco_loja_programada'] = 'N/A'
        else:
            product['preco_loja_programada'] = 'N/A'
        
        self.current_product = product
        
        # Exibir produto na interface
        self.ui.display_product(product)
        
        # Verificar se já tem substitutos salvos
        saved_subs = self.file_manager.get_saved_substitutes(iteration_num)
        
        if saved_subs:
            # Já tem substitutos salvos, exibir eles
            logging.info(f"Carregando {len(saved_subs)} substitutos salvos")
            saved_codes = [sub['cod_produto'] for sub in saved_subs]
            self.ui.display_results(saved_subs, preselected=saved_codes)
            self.current_search_results = saved_subs
        else:
            # Não tem substitutos salvos, buscar com IA
            self._search_substitutes_with_ai(product)
    
    def _search_substitutes_with_ai(self, product: Dict):
        """
        Busca substitutos usando IA em thread separada
        
        Args:
            product: Dicionário com dados do produto
        """
        self.ui.show_loading("Analisando produto e gerando termos de busca...")
        
        def search_thread():
            try:
                # Gerar termos de busca com IA
                product_name = product.get('nome', '')
                product_price = str(product.get('preco_loja_programada', ''))
                
                logging.info(f"Gerando termos de busca para: {product_name}")
                search_terms = self.ai_agent.generate_search_terms(product_name, product_price)
                
                logging.info(f"Termos gerados: {search_terms}")
                
                # Buscar produtos
                results = self.data_processor.search_products(
                    search_terms,
                    original_product_code=product.get('cod_produto'),
                    max_results=50
                )
                
                # Converter DataFrame para lista de dicts
                if len(results) > 0:
                    results_list = results.to_dict('records')
                else:
                    results_list = []
                
                self.current_search_results = results_list
                
                # Atualizar interface (deve ser na thread principal)
                self.root.after(0, lambda: self._display_search_results(results_list))
                
            except Exception as e:
                logging.error(f"Erro ao buscar substitutos: {e}")
                self.root.after(0, lambda: self.ui.show_message(
                    "Erro",
                    f"Erro ao buscar substitutos: {str(e)}"
                ))
            finally:
                self.root.after(0, self.ui.hide_loading)
        
        # Executar em thread separada
        thread = threading.Thread(target=search_thread, daemon=True)
        thread.start()
    
    def _display_search_results(self, results: List[Dict]):
        """Exibe resultados na interface"""
        self.ui.display_results(results)
        
        if len(results) == 0:
            self.ui.show_message(
                "Aviso",
                "Nenhum substituto encontrado. Tente uma busca manual."
            )
    
    def manual_search(self, search_term: str):
        """
        Realiza busca manual com termo fornecido pelo usuário
        
        Args:
            search_term: Termo de busca
        """
        logging.info(f"Busca manual: {search_term}")
        
        self.ui.show_loading("Buscando...")
        
        def search_thread():
            try:
                # Buscar usando o termo fornecido
                results = self.data_processor.search_products(
                    [search_term],
                    original_product_code=self.current_product.get('cod_produto') if self.current_product else None,
                    max_results=50,
                    min_similarity=50  # Menor threshold para busca manual
                )
                
                if len(results) > 0:
                    results_list = results.to_dict('records')
                else:
                    results_list = []
                
                self.current_search_results = results_list
                self.root.after(0, lambda: self._display_search_results(results_list))
                
            except Exception as e:
                logging.error(f"Erro na busca manual: {e}")
                self.root.after(0, lambda: self.ui.show_message(
                    "Erro",
                    f"Erro na busca: {str(e)}"
                ))
            finally:
                self.root.after(0, self.ui.hide_loading)
        
        thread = threading.Thread(target=search_thread, daemon=True)
        thread.start()
    
    def save_substitutes(self, iteration_num: int, selected_items: List[Dict]):
        """
        Salva substitutos selecionados
        
        Args:
            iteration_num: Número da iteração
            selected_items: Lista de itens selecionados
        """
        if len(selected_items) == 0:
            self.ui.show_message(
                "Aviso",
                "Nenhum item selecionado!"
            )
            return
        
        if len(selected_items) > 5:
            self.ui.show_message(
                "Aviso",
                "Máximo de 5 substitutos permitidos!"
            )
            return
        
        logging.info(f"Salvando {len(selected_items)} substitutos para iteração {iteration_num}")
        
        try:
            self.file_manager.save_substitutes(iteration_num, selected_items)
            
            # Atualizar progresso
            self._update_progress()
            
            logging.info(f"Substitutos salvos com sucesso")
            
        except Exception as e:
            logging.error(f"Erro ao salvar substitutos: {e}")
            self.ui.show_message(
                "Erro",
                f"Erro ao salvar: {str(e)}"
            )
    
    def skip_iteration(self, iteration_num: int):
        """
        Pula uma iteração (salva vazio)
        
        Args:
            iteration_num: Número da iteração
        """
        logging.info(f"Pulando iteração {iteration_num}")
        
        # Salvar lista vazia
        self.file_manager.save_substitutes(iteration_num, [])
        self._update_progress()
    
    def _update_progress(self):
        """Atualiza informação de progresso na interface"""
        total = self.file_manager.get_total_items()
        completed = self.file_manager.get_completed_count()
        
        self.ui.update_progress(completed, total)
    
    def run(self):
        """Inicia a aplicação"""
        logging.info("Aplicação iniciada")
        self.root.mainloop()
        logging.info("Aplicação encerrada")


def main():
    """Função principal"""
    print("="*60)
    print("Shopper - Buscador de Substitutos")
    print("="*60)
    print()
    
    # Verificar se tem arquivo .env
    if not os.path.exists('.env'):
        print("AVISO: Arquivo .env não encontrado!")
        print("Crie um arquivo .env com sua chave da OpenAI:")
        print()
        print("OPENAI_API_KEY=sua_chave_aqui")
        print()
        
        response = input("Continuar mesmo assim? (s/n): ")
        if response.lower() != 's':
            sys.exit(0)
    
    try:
        app = SubstituteFinderApp()
        app.run()
    except KeyboardInterrupt:
        print("\nAplicação interrompida pelo usuário")
        logging.info("Aplicação interrompida pelo usuário")
    except Exception as e:
        print(f"\nERRO FATAL: {e}")
        logging.error(f"Erro fatal: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
