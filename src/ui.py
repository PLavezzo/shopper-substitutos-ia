"""
Interface gráfica com CustomTkinter
Gerencia interação do usuário para seleção de substitutos
"""

import customtkinter as ctk
from typing import List, Dict, Callable
import logging
from pathlib import Path

# Configurar logging - caminho relativo ao diretório raiz do projeto
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=log_dir / 'ui.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configurar tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SubstituteFinderUI:
    """Interface principal do aplicativo"""
    
    def __init__(self, root: ctk.CTk):
        """
        Inicializa a interface
        
        Args:
            root: Janela principal do CustomTkinter
        """
        self.root = root
        self.root.title("Shopper - Buscador de Substitutos")
        self.root.geometry("1400x900")
        
        # Callbacks para comunicação com backend
        self.on_load_iteration: Callable = None
        self.on_save_substitutes: Callable = None
        self.on_search_manual: Callable = None
        self.on_skip_iteration: Callable = None
        
        # Estado atual
        self.current_iteration = 1
        self.current_results = []
        self.checkboxes = []
        self.checkbox_vars = []
        
        # Guarda referência do handler de scroll para evitar múltiplos bindings
        self._scroll_handler = None
        
        # Criar interface
        self._create_widgets()
        
    def _create_widgets(self):
        """Cria todos os widgets da interface"""
        
        # ===== FRAME SUPERIOR: Informações do produto original =====
        self.top_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.top_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Título
        title_label = ctk.CTkLabel(
            self.top_frame,
            text="PRODUTO ORIGINAL",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(15, 5))
        
        # Nome do produto
        self.product_name_label = ctk.CTkLabel(
            self.top_frame,
            text="Carregando...",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4CAF50"
        )
        self.product_name_label.pack(pady=5)
        
        # Preço do produto
        self.product_price_label = ctk.CTkLabel(
            self.top_frame,
            text="Preço: R$ --",
            font=ctk.CTkFont(size=16),
            text_color="#FFC107"
        )
        self.product_price_label.pack(pady=(0, 15))
        
        # ===== FRAME CENTRAL: Controles e navegação =====
        self.control_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.control_frame.pack(fill="x", padx=20, pady=10)
        
        # Linha 1: Navegação
        nav_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        nav_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        # Botão anterior
        self.prev_button = ctk.CTkButton(
            nav_frame,
            text="◀ Anterior",
            command=self._on_previous,
            width=120
        )
        self.prev_button.pack(side="left", padx=5)
        
        # Campo de iteração
        iteration_container = ctk.CTkFrame(nav_frame, fg_color="transparent")
        iteration_container.pack(side="left", expand=True)
        
        ctk.CTkLabel(
            iteration_container,
            text="Iteração:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=(20, 10))
        
        self.iteration_entry = ctk.CTkEntry(
            iteration_container,
            width=80,
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        self.iteration_entry.pack(side="left", padx=5)
        self.iteration_entry.bind("<Return>", lambda e: self._on_go_to_iteration())
        
        ctk.CTkButton(
            iteration_container,
            text="Ir",
            command=self._on_go_to_iteration,
            width=60
        ).pack(side="left", padx=5)
        
        # Botão próximo
        self.next_button = ctk.CTkButton(
            nav_frame,
            text="Próximo ▶",
            command=self._on_next,
            width=120
        )
        self.next_button.pack(side="right", padx=5)
        
        # Linha 2: Progresso e ações
        actions_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # Progresso
        self.progress_label = ctk.CTkLabel(
            actions_frame,
            text="Progresso: 0/0 (0.0%)",
            font=ctk.CTkFont(size=13)
        )
        self.progress_label.pack(side="left", padx=5)
        
        # Espaçador
        ctk.CTkLabel(actions_frame, text="").pack(side="left", expand=True)
        
        # Busca manual
        ctk.CTkLabel(
            actions_frame,
            text="Busca manual:",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=(5, 10))
        
        self.manual_search_entry = ctk.CTkEntry(
            actions_frame,
            width=200,
            placeholder_text="Digite termo de busca..."
        )
        self.manual_search_entry.pack(side="left", padx=5)
        self.manual_search_entry.bind("<Return>", lambda e: self._on_manual_search())
        
        ctk.CTkButton(
            actions_frame,
            text="Buscar",
            command=self._on_manual_search,
            width=80
        ).pack(side="left", padx=5)
        
        # Botão pular
        self.skip_button = ctk.CTkButton(
            actions_frame,
            text="⏭ Pular",
            command=self._on_skip,
            width=80,
            fg_color="#FF9800",
            hover_color="#F57C00"
        )
        self.skip_button.pack(side="right", padx=5)
        
        # ===== FRAME PRINCIPAL: Lista de resultados =====
        self.results_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Título da lista
        results_title_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        results_title_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(
            results_title_frame,
            text="SUBSTITUTOS ENCONTRADOS",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(side="left")
        
        self.results_count_label = ctk.CTkLabel(
            results_title_frame,
            text="(0 resultados)",
            font=ctk.CTkFont(size=13),
            text_color="#888"
        )
        self.results_count_label.pack(side="left", padx=(10, 0))
        
        # Cabeçalho da tabela
        header_frame = ctk.CTkFrame(self.results_frame, height=40)
        header_frame.pack(fill="x", padx=15, pady=(0, 5))
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            header_frame,
            text="",
            width=40
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            header_frame,
            text="Código",
            width=100,
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            header_frame,
            text="Nome do Produto",
            width=600,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            header_frame,
            text="Preço",
            width=100,
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            header_frame,
            text="Score",
            width=80,
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=5)
        
        # Scrollable frame para resultados
        self.scrollable_results = ctk.CTkScrollableFrame(
            self.results_frame,
            fg_color="transparent"
        )
        self.scrollable_results.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Configurar scroll manualmente para macOS
        # CustomTkinter 5.2.2 tem bug de scroll no Mac
        self._setup_scroll()
        
        # ===== FRAME INFERIOR: Botões de ação =====
        self.bottom_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.bottom_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        bottom_controls = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        bottom_controls.pack(fill="x", padx=15, pady=15)
        
        # Label de selecionados
        self.selected_label = ctk.CTkLabel(
            bottom_controls,
            text="Selecionados: 0/5",
            font=ctk.CTkFont(size=13)
        )
        self.selected_label.pack(side="left", padx=5)
        
        # Botão salvar e avançar
        self.save_button = ctk.CTkButton(
            bottom_controls,
            text="✓ Salvar e Avançar",
            command=self._on_save_and_next,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.save_button.pack(side="right", padx=5)
        
        # Botão apenas salvar
        ctk.CTkButton(
            bottom_controls,
            text="💾 Salvar",
            command=self._on_save,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14)
        ).pack(side="right", padx=5)
    
    def _setup_scroll(self):
        """
        Configura scroll forçado para macOS.
        Usa a mesma técnica que funcionou no teste.
        """
        # Acessa o canvas interno do ScrollableFrame
        canvas = self.scrollable_results._parent_canvas
        
        # Handler de scroll SIMPLES (igual ao teste que funcionou)
        def on_mouse_wheel(event):
            # No macOS, delta é 1 ou -1 geralmente
            canvas.yview_scroll(-1 * event.delta, "units")
        
        # Vincula EXATAMENTE como no teste que funcionou
        canvas.bind("<MouseWheel>", on_mouse_wheel, add="+")
        self.scrollable_results.bind("<MouseWheel>", on_mouse_wheel, add="+")
        
        # Salva handler
        self._scroll_handler = on_mouse_wheel
        
        logging.info("Scroll configurado (modo teste - funcionou)")
    
    def set_callbacks(
        self,
        on_load_iteration: Callable,
        on_save_substitutes: Callable,
        on_search_manual: Callable = None,
        on_skip_iteration: Callable = None
    ):
        """
        Define callbacks para comunicação com backend
        
        Args:
            on_load_iteration: Callback(iteration_num) -> dict
            on_save_substitutes: Callback(iteration_num, selected_items) -> None
            on_search_manual: Callback(search_term) -> list
            on_skip_iteration: Callback(iteration_num) -> None
        """
        self.on_load_iteration = on_load_iteration
        self.on_save_substitutes = on_save_substitutes
        self.on_search_manual = on_search_manual
        self.on_skip_iteration = on_skip_iteration
    
    def load_iteration(self, iteration_num: int):
        """
        Carrega uma iteração específica
        
        Args:
            iteration_num: Número da iteração
        """
        self.current_iteration = iteration_num
        self.iteration_entry.delete(0, "end")
        self.iteration_entry.insert(0, str(iteration_num))
        
        if self.on_load_iteration:
            self.on_load_iteration(iteration_num)
    
    def display_product(self, product: Dict):
        """
        Exibe informações do produto original
        
        Args:
            product: Dicionário com dados do produto
        """
        name = product.get('nome', 'N/A')
        price = product.get('preco_loja_programada', 'N/A')
        
        self.product_name_label.configure(text=name)
        self.product_price_label.configure(text=f"Preço: R$ {price}")
    
    def display_results(self, results: List[Dict], preselected: List[str] = None):
        """
        Exibe resultados de busca
        
        Args:
            results: Lista de dicionários com produtos encontrados
            preselected: Lista de códigos de produtos já selecionados
        """
        # Limpar resultados anteriores
        for widget in self.scrollable_results.winfo_children():
            widget.destroy()
        
        self.checkboxes = []
        self.checkbox_vars = []
        self.current_results = results
        
        # Atualizar contador
        self.results_count_label.configure(text=f"({len(results)} resultados)")
        
        if preselected is None:
            preselected = []
        
        # Criar linha para cada resultado
        for i, item in enumerate(results):
            self._create_result_row(item, i, item.get('cod_produto') in preselected)
        
        # Atualizar contador de selecionados
        self._update_selected_count()
        
        # RE-CONFIGURA scroll após adicionar novos widgets
        # Importante: novos widgets podem interferir com os bindings
        self._setup_scroll()
    
    def _create_result_row(self, item: Dict, index: int, preselected: bool = False):
        """Cria uma linha na lista de resultados"""
        
        # Frame da linha
        row_frame = ctk.CTkFrame(
            self.scrollable_results,
            height=50,
            fg_color="#2b2b2b" if index % 2 == 0 else "#1f1f1f"
        )
        row_frame.pack(fill="x", pady=2)
        row_frame.pack_propagate(False)
        
        # Checkbox
        var = ctk.BooleanVar(value=preselected)
        checkbox = ctk.CTkCheckBox(
            row_frame,
            text="",
            variable=var,
            width=40,
            command=self._update_selected_count
        )
        checkbox.pack(side="left", padx=5)
        
        self.checkboxes.append(checkbox)
        self.checkbox_vars.append(var)
        
        # Código
        cod_label = ctk.CTkLabel(
            row_frame,
            text=item.get('cod_produto', 'N/A'),
            width=100,
            anchor="w"
        )
        cod_label.pack(side="left", padx=5)
        
        # Nome
        nome_label = ctk.CTkLabel(
            row_frame,
            text=item.get('nome', 'N/A'),
            width=600,
            anchor="w"
        )
        nome_label.pack(side="left", padx=5)
        
        # Preço
        preco = item.get('preco_loja_programada', 'N/A')
        preco_label = ctk.CTkLabel(
            row_frame,
            text=f"R$ {preco}",
            width=100,
            anchor="w"
        )
        preco_label.pack(side="left", padx=5)
        
        # Score
        score = item.get('score', 0)
        score_label = ctk.CTkLabel(
            row_frame,
            text=f"{score}",
            width=80,
            anchor="w",
            text_color=self._get_score_color(score)
        )
        score_label.pack(side="left", padx=5)
    
    def _get_score_color(self, score: float) -> str:
        """Retorna cor baseada no score"""
        if score >= 90:
            return "#4CAF50"  # Verde
        elif score >= 70:
            return "#FFC107"  # Amarelo
        else:
            return "#FF5722"  # Vermelho
    
    def _update_selected_count(self):
        """Atualiza contador de itens selecionados"""
        selected = sum(1 for var in self.checkbox_vars if var.get())
        self.selected_label.configure(text=f"Selecionados: {selected}/5")
        
        # Desabilitar checkboxes se já tem 5 selecionados
        if selected >= 5:
            for i, (cb, var) in enumerate(zip(self.checkboxes, self.checkbox_vars)):
                if not var.get():
                    cb.configure(state="disabled")
        else:
            for cb in self.checkboxes:
                cb.configure(state="normal")
    
    def update_progress(self, completed: int, total: int):
        """Atualiza informação de progresso"""
        percentage = (completed / total * 100) if total > 0 else 0
        self.progress_label.configure(
            text=f"Progresso: {completed}/{total} ({percentage:.1f}%)"
        )
    
    def _on_previous(self):
        """Handler para botão anterior"""
        if self.current_iteration > 1:
            self.load_iteration(self.current_iteration - 1)
    
    def _on_next(self):
        """Handler para botão próximo"""
        self.load_iteration(self.current_iteration + 1)
    
    def _on_go_to_iteration(self):
        """Handler para ir para iteração específica"""
        try:
            iteration = int(self.iteration_entry.get())
            if iteration > 0:
                self.load_iteration(iteration)
        except ValueError:
            pass
    
    def _on_manual_search(self):
        """Handler para busca manual"""
        term = self.manual_search_entry.get().strip()
        if term and self.on_search_manual:
            self.on_search_manual(term)
    
    def _on_skip(self):
        """Handler para pular iteração"""
        if self.on_skip_iteration:
            self.on_skip_iteration(self.current_iteration)
        self._on_next()
    
    def _on_save(self):
        """Handler para salvar selecionados"""
        selected_items = self._get_selected_items()
        
        if self.on_save_substitutes:
            self.on_save_substitutes(self.current_iteration, selected_items)
    
    def _on_save_and_next(self):
        """Handler para salvar e avançar"""
        self._on_save()
        self._on_next()
    
    def _get_selected_items(self) -> List[Dict]:
        """Retorna lista de itens selecionados"""
        selected = []
        
        for var, item in zip(self.checkbox_vars, self.current_results):
            if var.get():
                selected.append({
                    'cod_produto': item.get('cod_produto'),
                    'nome': item.get('nome'),
                    'preco_loja_programada': item.get('preco_loja_programada')
                })
        
        return selected
    
    def show_message(self, title: str, message: str):
        """Exibe mensagem para o usuário"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x200")
        
        ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=350
        ).pack(pady=30, padx=20)
        
        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            width=100
        ).pack(pady=10)
        
        # Centralizar
        dialog.transient(self.root)
        dialog.grab_set()
    
    def show_loading(self, message: str = "Processando..."):
        """Exibe tela de carregamento"""
        # Criar overlay
        self.loading_frame = ctk.CTkFrame(
            self.root,
            fg_color=("#DBDBDB", "#2B2B2B"),
            bg_color="transparent"
        )
        self.loading_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            self.loading_frame,
            text=message,
            font=ctk.CTkFont(size=16)
        ).pack(padx=40, pady=20)
        
        # Adicionar spinner (usando label animado)
        self.loading_label = ctk.CTkLabel(
            self.loading_frame,
            text="⏳",
            font=ctk.CTkFont(size=24)
        )
        self.loading_label.pack(padx=40, pady=(0, 20))
    
    def hide_loading(self):
        """Esconde tela de carregamento"""
        if hasattr(self, 'loading_frame'):
            self.loading_frame.destroy()


# Teste standalone
if __name__ == "__main__":
    root = ctk.CTk()
    app = SubstituteFinderUI(root)
    
    # Teste de exibição
    test_product = {
        'nome': 'QUEIJO RALADO FAIXA AZUL PARMESÃO 50G',
        'preco_loja_programada': '10,99'
    }
    app.display_product(test_product)
    
    test_results = [
        {'cod_produto': 'SHOP001', 'nome': 'QUEIJO RALADO PARMESÃO VIGOR 50G', 'preco_loja_programada': '11,50', 'score': 95},
        {'cod_produto': 'SHOP002', 'nome': 'QUEIJO RALADO PARMESÃO TIROLEZ 100G', 'preco_loja_programada': '18,90', 'score': 85},
        {'cod_produto': 'SHOP003', 'nome': 'QUEIJO RALADO PARMESÃO 50G', 'preco_loja_programada': '9,99', 'score': 90},
    ]
    app.display_results(test_results)
    app.update_progress(5, 100)
    
    root.mainloop()
