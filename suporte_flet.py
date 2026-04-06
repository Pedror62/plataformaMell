# suporte_flet.py
import flet as ft
import pandas as pd
import datetime
import os
import subprocess
import glob
from database.queries import get_db_cursor, registrar_log
import threading
import time

class SuporteFlet:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "PROSALES - Central de Controle"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.bgcolor = ft.Colors.BLUE_GREY_900
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.window_resizable = True
        self.page.window_center()
        
        # Cores do sistema
        self.cor_primaria = "#169fda"
        self.cor_secundaria = "#0d7ab3"
        self.cor_sucesso = "#4caf50"
        self.cor_erro = "#f44336"
        self.cor_aviso = "#ff9800"
        
        # Dados
        self.logs_data = []
        self.backups_data = []
        
        # Componentes de loading
        self.loading = ft.ProgressRing(visible=False, width=30, height=30)
        
    def build(self):
        """Constrói a interface completa"""
        
        # Cabeçalho
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(name=ft.Icons.SHIELD, size=40, color=self.cor_primaria),
                    ft.Column(
                        [
                            ft.Text("Central de Controle", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Text("Suporte Técnico", size=14, color=ft.Colors.BLUE_GREY_400),
                        ],
                        spacing=0,
                    ),
                ],
                spacing=15,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(20),
            bgcolor=ft.Colors.BLUE_GREY_800,
            border_radius=ft.border_radius.only(top_left=20, top_right=20),
        )
        
        # Tabs
        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="📢 Disparar Notificações",
                    icon=ft.Icons.NOTIFICATIONS,
                    content=self._build_notificacoes_tab(),
                ),
                ft.Tab(
                    text="📜 Logs de Auditoria",
                    icon=ft.Icons.HISTORY,
                    content=self._build_logs_tab(),
                ),
                ft.Tab(
                    text="🛠️ Manutenção",
                    icon=ft.Icons.SETTINGS,
                    content=self._build_manutencao_tab(),
                ),
                ft.Tab(
                    text="🔐 Gestão de Permissões",
                    icon=ft.Icons.SECURITY,
                    content=self._build_permissoes_tab(),
                ),
            ],
            expand=True,
        )
        
        # Rodapé
        footer = ft.Container(
            content=ft.Text(
                f"© {datetime.datetime.now().year} PROSALES - Gestão Profissional de Vendas | Desenvolvido pelo Suporte Interno",
                size=12,
                color=ft.Colors.BLUE_GREY_600,
                text_align=ft.TextAlign.CENTER,
            ),
            padding=ft.padding.all(15),
            alignment=ft.alignment.center,
        )
        
        # Layout principal
        self.page.add(
            ft.Column(
                [
                    header,
                    ft.Container(content=self.tabs, expand=True, padding=ft.padding.all(20)),
                    footer,
                ],
                spacing=0,
                expand=True,
            )
        )
    
    def _build_notificacoes_tab(self):
        """Constrói a aba de notificações"""
        
        self.titulo_notif = ft.TextField(
            label="Título do Alerta",
            hint_text="Digite o título da notificação",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_GREY_500,
            focused_border_color=self.cor_primaria,
            bgcolor=ft.Colors.BLUE_GREY_900,
            expand=True,
        )
        
        self.mensagem_notif = ft.TextField(
            label="Mensagem",
            hint_text="Digite a mensagem detalhada",
            multiline=True,
            min_lines=4,
            max_lines=6,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_GREY_500,
            focused_border_color=self.cor_primaria,
            bgcolor=ft.Colors.BLUE_GREY_900,
            expand=True,
        )
        
        self.destinatario_notif = ft.Dropdown(
            label="Destinatário",
            hint_text="Selecione quem receberá",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Vendedores"),
                ft.dropdown.Option("Supervisores"),
                ft.dropdown.Option("Admins"),
                ft.dropdown.Option("Auditores"),
            ],
            value="Todos",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_GREY_500,
            focused_border_color=self.cor_primaria,
            bgcolor=ft.Colors.BLUE_GREY_900,
        )
        
        self.status_notif = ft.Text("", size=12, visible=False)
        
        btn_enviar = ft.ElevatedButton(
            content=ft.Text("🔔 DISPARAR ALERTA", size=14, weight=ft.FontWeight.BOLD),
            bgcolor=self.cor_primaria,
            color=ft.Colors.WHITE,
            width=300,
            height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
            on_click=self._enviar_notificacao,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("📢 Enviar aviso para o Sino", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Container(height=20),
                    ft.Row([self.titulo_notif], expand=True),
                    ft.Container(height=15),
                    ft.Row([self.mensagem_notif], expand=True),
                    ft.Container(height=15),
                    ft.Row([self.destinatario_notif], expand=True),
                    ft.Container(height=20),
                    ft.Row([btn_enviar], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=10),
                    ft.Row([self.status_notif], alignment=ft.MainAxisAlignment.CENTER),
                ],
                spacing=0,
                expand=True,
            ),
            padding=ft.padding.all(20),
            expand=True,
        )
    
    def _build_logs_tab(self):
        """Constrói a aba de logs"""
        
        self.filtro_logs = ft.TextField(
            label="Filtrar por ação",
            hint_text="Ex: LOGIN, VENDA, BACKUP",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_GREY_500,
            focused_border_color=self.cor_primaria,
            bgcolor=ft.Colors.BLUE_GREY_900,
            expand=True,
            on_change=self._filtrar_logs,
        )
        
        self.periodo_logs = ft.Dropdown(
            label="Período",
            options=[
                ft.dropdown.Option("Últimas 24h"),
                ft.dropdown.Option("Últimos 7 dias"),
                ft.dropdown.Option("Últimos 30 dias"),
                ft.dropdown.Option("Todos"),
            ],
            value="Últimas 24h",
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.BLUE_GREY_500,
            focused_border_color=self.cor_primaria,
            bgcolor=ft.Colors.BLUE_GREY_900,
            width=200,
            on_change=self._filtrar_logs,
        )
        
        self.btn_atualizar_logs = ft.IconButton(
            icon=ft.Icons.REFRESH,
            tooltip="Atualizar",
            on_click=self._carregar_logs,
        )
        
        self.logs_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Data/Hora", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Usuário", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ação", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Detalhes", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            heading_row_color=ft.Colors.BLUE_GREY_800,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_700),
            border_radius=10,
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLUE_GREY_800),
            column_spacing=20,
        )
        
        self.total_registros = ft.Text("Total: 0", size=12, color=ft.Colors.BLUE_GREY_400)
        self.acoes_unicas = ft.Text("Ações únicas: 0", size=12, color=ft.Colors.BLUE_GREY_400)
        self.backups_count = ft.Text("Backups: 0", size=12, color=ft.Colors.BLUE_GREY_400)
        
        # Carregar logs iniciais
        self._carregar_logs(None)
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("📜 Histórico de ações", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Container(expand=True),
                            self.btn_atualizar_logs,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=20),
                    ft.Row(
                        [
                            self.filtro_logs,
                            self.periodo_logs,
                        ],
                        expand=True,
                        spacing=15,
                    ),
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        self.total_registros,
                                        ft.Container(width=20),
                                        self.acoes_unicas,
                                        ft.Container(width=20),
                                        self.backups_count,
                                    ],
                                ),
                                ft.Container(height=10),
                                ft.Container(
                                    content=self.logs_table,
                                    height=450,
                                    overflow=ft.ScrollMode.AUTO,
                                ),
                            ],
                        ),
                        expand=True,
                    ),
                ],
                expand=True,
            ),
            padding=ft.padding.all(20),
            expand=True,
        )
    
    def _build_manutencao_tab(self):
        """Constrói a aba de manutenção"""
        
        self.status_backup = ft.Text("", size=12, visible=False)
        
        btn_backup = ft.ElevatedButton(
            content=ft.Text("📥 GERAR BACKUP AGORA", size=14, weight=ft.FontWeight.BOLD),
            bgcolor=self.cor_primaria,
            color=ft.Colors.WHITE,
            width=250,
            height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
            on_click=self._gerar_backup,
        )
        
        btn_limpar_backups = ft.ElevatedButton(
            content=ft.Text("🧹 LIMPAR BACKUPS ANTIGOS", size=12, weight=ft.FontWeight.BOLD),
            bgcolor=self.cor_aviso,
            color=ft.Colors.WHITE,
            width=250,
            height=40,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
            on_click=self._limpar_backups_antigos,
        )
        
        self.backups_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Arquivo", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Data", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Tamanho", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            heading_row_color=ft.Colors.BLUE_GREY_800,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_700),
            border_radius=10,
        )
        
        self._carregar_backups()
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("🛠️ Segurança e Backup", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ],
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "💾 Gere um backup completo (Dump) do banco de dados antes de realizar alterações estruturais.",
                        size=12,
                        color=ft.Colors.BLUE_GREY_400,
                    ),
                    ft.Container(height=20),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(f"Banco Ativo: {self._get_db_name()}", size=13, color=ft.Colors.BLUE_GREY_300),
                                        ft.Text(f"Servidor: {self._get_db_host()}", size=13, color=ft.Colors.BLUE_GREY_300),
                                    ],
                                    spacing=5,
                                ),
                                bgcolor=ft.Colors.BLUE_GREY_800,
                                padding=ft.padding.all(15),
                                border_radius=10,
                            ),
                            ft.Container(expand=True),
                        ],
                    ),
                    ft.Container(height=20),
                    ft.Row(
                        [
                            btn_backup,
                            ft.Container(width=20),
                            btn_limpar_backups,
                            ft.Container(expand=True),
                        ],
                    ),
                    ft.Container(height=10),
                    ft.Row([self.status_backup], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=20),
                    ft.Text("📋 Últimos Backups", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Container(height=10),
                    ft.Container(
                        content=self.backups_table,
                        height=300,
                        overflow=ft.ScrollMode.AUTO,
                    ),
                ],
                expand=True,
            ),
            padding=ft.padding.all(20),
            expand=True,
        )
    
    def _build_permissoes_tab(self):
        """Constrói a aba de permissões"""
        
        # Placeholder para gestão de permissões
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("🔐 Gestão de Permissões", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Container(height=20),
                    ft.Text(
                        "Funcionalidade em desenvolvimento para Flet",
                        size=14,
                        color=ft.Colors.ORANGE_400,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "A gestão de permissões está disponível na versão Streamlit.",
                        size=12,
                        color=ft.Colors.BLUE_GREY_400,
                    ),
                ],
                expand=True,
            ),
            padding=ft.padding.all(20),
            expand=True,
        )
    
    def _enviar_notificacao(self, e):
        """Envia notificação"""
        titulo = self.titulo_notif.value
        mensagem = self.mensagem_notif.value
        destinatario = self.destinatario_notif.value
        
        if not titulo or not mensagem:
            self.status_notif.value = "⚠️ Preencha o título e a mensagem!"
            self.status_notif.color = self.cor_aviso
            self.status_notif.visible = True
            self.page.update()
            return
        
        try:
            mapa = {
                "Todos": "todos",
                "Vendedores": "vendedor",
                "Supervisores": "supervisor",
                "Admins": "admin",
                "Auditores": "auditor",
            }
            dest = mapa.get(destinatario, destinatario.lower())
            
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    "INSERT INTO notificacoes (titulo, mensagem, destinatario, data_envio) VALUES (%s, %s, %s, NOW())",
                    (titulo, mensagem, dest)
                )
            
            registrar_log(26, "NOTIFICACAO_ENVIADA", f"Título: {titulo} | Para: {destinatario}")
            
            self.status_notif.value = "✅ Alerta enviado com sucesso!"
            self.status_notif.color = self.cor_sucesso
            self.status_notif.visible = True
            
            self.titulo_notif.value = ""
            self.mensagem_notif.value = ""
            
        except Exception as err:
            self.status_notif.value = f"❌ Erro: {str(err)}"
            self.status_notif.color = self.cor_erro
            self.status_notif.visible = True
        
        self.page.update()
        
        # Esconder mensagem após 3 segundos
        def hide_status():
            time.sleep(3)
            self.status_notif.visible = False
            self.page.update()
        
        threading.Thread(target=hide_status, start=True)
    
    def _carregar_logs(self, e):
        """Carrega logs do banco"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    SELECT l.data_hora, u.nome_usuario, l.acao, l.detalhes
                    FROM logs_sistema l
                    JOIN users u ON l.id_usuario = u.id_usuario
                    ORDER BY l.data_hora DESC 
                    LIMIT 500
                """)
                logs = cursor.fetchall()
            
            self.logs_data = logs
            
            # Aplicar filtro
            self._filtrar_logs(None)
            
        except Exception as e:
            print(f"Erro ao carregar logs: {e}")
    
    def _filtrar_logs(self, e):
        """Filtra logs"""
        filtro = self.filtro_logs.value.upper() if self.filtro_logs.value else ""
        periodo = self.periodo_logs.value
        
        dados_filtrados = self.logs_data
        
        # Aplicar filtro de ação
        if filtro:
            dados_filtrados = [log for log in dados_filtrados if filtro in log['acao'].upper()]
        
        # Aplicar filtro de período
        if periodo != "Todos":
            agora = datetime.datetime.now()
            if periodo == "Últimas 24h":
                limite = agora - datetime.timedelta(days=1)
            elif periodo == "Últimos 7 dias":
                limite = agora - datetime.timedelta(days=7)
            elif periodo == "Últimos 30 dias":
                limite = agora - datetime.timedelta(days=30)
            else:
                limite = None
            
            if limite:
                dados_filtrados = [log for log in dados_filtrados if log['data_hora'] >= limite]
        
        # Atualizar tabela
        self.logs_table.rows = []
        for log in dados_filtrados:
            data_str = log['data_hora'].strftime('%d/%m/%Y %H:%M:%S') if log['data_hora'] else ""
            self.logs_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data_str, size=12)),
                        ft.DataCell(ft.Text(log['nome_usuario'], size=12)),
                        ft.DataCell(ft.Text(log['acao'], size=12)),
                        ft.DataCell(ft.Text(log['detalhes'][:100] if log['detalhes'] else "", size=12)),
                    ]
                )
            )
        
        # Atualizar estatísticas
        acoes = set([log['acao'] for log in dados_filtrados])
        backups = len([log for log in dados_filtrados if 'BACKUP' in log['acao'].upper()])
        
        self.total_registros.value = f"Total: {len(dados_filtrados)}"
        self.acoes_unicas.value = f"Ações únicas: {len(acoes)}"
        self.backups_count.value = f"Backups: {backups}"
        
        self.page.update()
    
    def _gerar_backup(self, e):
        """Gera backup manual"""
        self.status_backup.visible = True
        self.status_backup.value = "🔄 Processando backup..."
        self.status_backup.color = self.cor_primaria
        self.page.update()
        
        try:
            db_user = st.secrets["mysql"]["user"]
            db_password = st.secrets["mysql"]["password"]
            db_host = st.secrets["mysql"]["host"]
            db_name = st.secrets["mysql"]["database"]
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
            nome_arquivo = f"backup_{db_name}_{timestamp}.sql"
            caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)

            mysqldump_exe = r'"C:\Program Files\MariaDB 12.2\bin\mysqldump.exe"'
            comando = f'{mysqldump_exe} -h {db_host} -u {db_user} -p"{db_password}" --ssl=0 {db_name} > "{caminho_arquivo}"'
            
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
            
            if resultado.returncode == 0 and os.path.exists(caminho_arquivo):
                registrar_log(26, "BACKUP_MANUAL", f"Backup gerado: {nome_arquivo}")
                self.status_backup.value = f"✅ Backup gerado com sucesso: {nome_arquivo}"
                self.status_backup.color = self.cor_sucesso
                self._carregar_backups()
            else:
                self.status_backup.value = f"❌ Erro ao gerar backup: {resultado.stderr}"
                self.status_backup.color = self.cor_erro
                
        except Exception as err:
            self.status_backup.value = f"❌ Erro: {str(err)}"
            self.status_backup.color = self.cor_erro
        
        self.page.update()
        
        # Esconder mensagem após 5 segundos
        def hide_status():
            time.sleep(5)
            self.status_backup.visible = False
            self.page.update()
        
        threading.Thread(target=hide_status, start=True)
    
    def _carregar_backups(self):
        """Carrega lista de backups"""
        backups = []
        for arquivo in os.listdir('.'):
            if arquivo.startswith('backup_') and arquivo.endswith('.sql'):
                caminho = os.path.join('.', arquivo)
                data_mod = datetime.datetime.fromtimestamp(os.path.getmtime(caminho))
                tamanho = os.path.getsize(caminho) / (1024*1024)
                backups.append({
                    'arquivo': arquivo,
                    'data': data_mod.strftime('%d/%m/%Y %H:%M'),
                    'tamanho': f'{tamanho:.2f} MB'
                })
        
        backups.sort(key=lambda x: x['data'], reverse=True)
        self.backups_data = backups[:10]
        
        self.backups_table.rows = []
        for b in self.backups_data:
            self.backups_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(b['arquivo'], size=12)),
                        ft.DataCell(ft.Text(b['data'], size=12)),
                        ft.DataCell(ft.Text(b['tamanho'], size=12)),
                    ]
                )
            )
        
        self.page.update()
    
    def _limpar_backups_antigos(self, e):
        """Remove backups antigos"""
        removidos = 0
        for backup in self.backups_data[10:]:
            try:
                os.remove(backup['arquivo'])
                removidos += 1
            except:
                pass
        
        self._carregar_backups()
        
        self.status_backup.visible = True
        self.status_backup.value = f"🧹 {removidos} backups antigos removidos!"
        self.status_backup.color = self.cor_sucesso
        self.page.update()
        
        def hide_status():
            time.sleep(3)
            self.status_backup.visible = False
            self.page.update()
        
        threading.Thread(target=hide_status, start=True)
    
    def _get_db_name(self):
        """Retorna nome do banco"""
        try:
            return st.secrets["mysql"]["database"]
        except:
            return "N/A"
    
    def _get_db_host(self):
        """Retorna host do banco"""
        try:
            return st.secrets["mysql"]["host"]
        except:
            return "N/A"


def main(page: ft.Page):
    """Função principal"""
    app = SuporteFlet(page)
    app.build()


if __name__ == "__main__":
    ft.app(target=main)