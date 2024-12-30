import flet as ft
from services.eleitor_api import retorna_lista_cidade, retorna_candidatos_backoffice, retorna_nome_cidade_por_codigo

class Backoffice:
    def __init__(self, page: ft.Page):
        self.page = page
        page.title = "BackOffice Urna"
        page.window.height = 600
        page.window.width = 1000
        self.container_display_estados = self.__display_estados()
        self.text_consulta_votos = ft.Text("Consultar Votos", size=30, weight='bold', text_align='center')
        self.page.session.set("select_cidade","")
        self.page.session.set("select_voto","")
        self.estados = [
            {"sigla": "AC", "estado": "Acre", "regiao": "norte"},
            {"sigla": "AL", "estado": "Alagoas", "regiao": "nordeste"},
            {"sigla": "AP", "estado": "Amapá", "regiao": "norte"},
            {"sigla": "AM", "estado": "Amazonas", "regiao": "norte"},
            {"sigla": "BA", "estado": "Bahia", "regiao": "nordeste"},
            {"sigla": "CE", "estado": "Ceará", "regiao": "nordeste"},
            {"sigla": "DF", "estado": "Distrito Federal", "regiao": "centrooeste"},
            {"sigla": "ES", "estado": "Espírito Santo", "regiao": "sudeste"},
            {"sigla": "GO", "estado": "Goiás", "regiao": "centrooeste"},
            {"sigla": "MA", "estado": "Maranhão", "regiao": "nordeste"},
            {"sigla": "MT", "estado": "Mato Grosso", "regiao": "centrooeste"},
            {"sigla": "MS", "estado": "Mato Grosso do Sul", "regiao": "centrooeste"},
            {"sigla": "MG", "estado": "Minas Gerais", "regiao": "sudeste"},
            {"sigla": "PA", "estado": "Pará", "regiao": "norte"},
            {"sigla": "PB", "estado": "Paraíba", "regiao": "nordeste"},
            {"sigla": "PR", "estado": "Paraná", "regiao": "sul"},
            {"sigla": "PE", "estado": "Pernambuco", "regiao": "nordeste"},
            {"sigla": "PI", "estado": "Piauí", "regiao": "nordeste"},
            {"sigla": "RJ", "estado": "Rio de Janeiro", "regiao": "sudeste"},
            {"sigla": "RN", "estado": "Rio Grande do Norte", "regiao": "nordeste"},
            {"sigla": "RS", "estado": "Rio Grande do Sul", "regiao": "sul"},
            {"sigla": "RO", "estado": "Rondônia", "regiao": "norte"},
            {"sigla": "RR", "estado": "Roraima", "regiao": "norte"},
            {"sigla": "SC", "estado": "Santa Catarina", "regiao": "sul"},
            {"sigla": "SP", "estado": "São Paulo", "regiao": "sudeste"},
            {"sigla": "SE", "estado": "Sergipe", "regiao": "nordeste"},
            {"sigla": "TO", "estado": "Tocantins", "regiao": "norte"}
            ]

    def __linha_head(self):
        return ft.Container(
            content=ft.Row([
                ft.Container(content=ft.Image(src="tse3.png", width=150) ,width=150, height=100, ),
                ft.Container(content=self.text_consulta_votos, width=800, height=100,  alignment=ft.alignment.center)
            ]),
            #border_radius=ft.border_radius.all(10),
            border=ft.border.all(1, 'black'),
            bgcolor=ft.Colors.GREEN_600
        )

    def __create_table_candidatos(self, lista_candidatos):
        def bgcolor_situacao(situacao):
            if situacao.lower() in  ["eleito", "eleito por qp", "eleito por média"]:
                return ft.Colors.GREEN
            elif situacao.lower() in ["suplente"]:
                return ft.Colors.BLUE
            elif situacao.lower() in ["não eleito"]:
                return ft.Colors.RED
            elif situacao.lower() in ["concorrendo"]:
                return ft.Colors.AMBER
            else:
                return None

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nome Urna", weight='bold', size=15)),
                ft.DataColumn(ft.Text("Nome Completo", weight='bold', size=15)),
                ft.DataColumn(ft.Text("Partido", weight='bold', size=15)),
                ft.DataColumn(ft.Text("Situação", weight='bold', size=15)),
                ft.DataColumn(ft.Text("Número", weight='bold', size=15)),
            ],
            horizontal_lines=ft.border.BorderSide(1.5, "black"),


        )

        for candidato in lista_candidatos:
            table.rows.append(
                ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(candidato.get("nomeUrna"), size=15)),
                            ft.DataCell(ft.Text(candidato.get("nomeCompleto"), size=15)),
                            ft.DataCell(ft.Text(candidato.get("partido"), size=15)),
                            #ft.DataCell(ft.Text(candidato.get("descricaoTotalizacao"),  bgcolor=bgcolor_situacao(candidato.get("descricaoTotalizacao")) , no_wrap=True)),
                            ft.DataCell(ft.Container(width=25, height=25, bgcolor=bgcolor_situacao(candidato.get("descricaoTotalizacao")))),
                            ft.DataCell(ft.Text(candidato.get("numero"), size=15)),
                        ],
                        
                    ),
            )
        

        return ft.Column(controls=[table], scroll="auto", expand=True)

    def __acessar_candidatos(self, e):
        cod_cidade = self.page.session.get("select_cidade")
        voto = self.page.session.get("select_voto")
        nome_cidade = retorna_nome_cidade_por_codigo(cod_cidade)
        lista_candidatos = retorna_candidatos_backoffice(cod_cidade, voto)

        def busca_candidato(e):
            palavra_chave = e.data
            temp_lista = []
            for candidato in lista_candidatos:
                if palavra_chave.lower() in candidato.get("nomeUrna").lower() or palavra_chave in str(candidato.get("numero")):
                    temp_lista.append(candidato)


            self.container_display_estados.content.controls[1] = None
            self.container_display_estados.content.controls[1] = self.__create_table_candidatos(temp_lista)
            self.page.update()

        container_busca_candidato = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Text("Total de registros:", size=15, weight='bold'),
                    ft.Text(len(lista_candidatos), size=15)
                ]),
                ft.Row([
                    ft.Text("Buscar candidato:", size=15, weight='bold'),
                    ft.TextField(on_change=busca_candidato,width=270, height=40,autofocus=True, hint_text="Infome nome ou numero do candidato", hint_style=ft.TextStyle(size=13))
                ]),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            padding=ft.padding.only(left=10, right=10)
        )

        container_legenda = ft.Container(
            content=ft.Row([
                ft.Text("Legenda: ", size=15, weight='bold'),
                ft.Row([
                    ft.Container(width=15, height=15, bgcolor=ft.Colors.GREEN),
                    ft.Text("Eleito", size=15, weight='bold', text_align='center')
                ], spacing=5),
                ft.Row([
                    ft.Container(width=15, height=15, bgcolor=ft.Colors.RED),
                    ft.Text("Não Eleito", size=15, weight='bold', text_align='center')
                ], spacing=5),
                ft.Row([
                    ft.Container(width=15, height=15, bgcolor=ft.Colors.BLUE),
                    ft.Text("Suplente", size=15, weight='bold', text_align='center')
                ], spacing=5),
                ft.Row([
                    ft.Container(width=15, height=15, bgcolor=ft.Colors.AMBER),
                    ft.Text("Inapto", size=15, weight='bold', text_align='center')
                ], spacing=5)
            ]),
            height=20,
            padding=ft.padding.only(left=10, right=10)
        )

        self.container_display_estados.content = None
        self.container_display_estados.content = ft.Column(controls=[container_busca_candidato, self.__create_table_candidatos(lista_candidatos),container_legenda ])
        self.text_consulta_votos.value = f"Consultar Votos - {nome_cidade}"
        self.page.update()

    def __coluna_regioes(self):
        lista_regiao = ["brasil", "norte", "nordeste", "centro-oeste", "sudeste", "sul"]
        btns_regiao = []

        for regiao in lista_regiao:
            btns_regiao.append(ft.Container(
                content=ft.Text(regiao.capitalize(), size=18, weight='bold',),
                width=150,
                height=60,
                alignment=ft.alignment.center,
                on_click=self.__seleciona_regiao,
                key=regiao.replace('-',''),
                border=ft.border.all(1, 'black'),
                bgcolor=ft.Colors.BLUE_GREY_200
            ))


        return ft.Column(
            controls=btns_regiao,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            width=150,
        )

    def __display_estados(self):

        return ft.Container(
            content=ft.Text("Selecione a região ...", size=40, weight='bold', text_align='center'),
            #content=ft.Column(controls=[table], scroll="auto", expand=True),
            width=800,
            height=430, 
            alignment=ft.alignment.center,
            border=ft.border.all(1, 'black'),
            bgcolor=ft.Colors.BLUE_GREY_200

        )

    def __container_principal_backoffice(self):
        return ft.Container(
            content=ft.Column([
                self.__linha_head(),
                ft.Row([
                    self.__coluna_regioes(),
                    self.container_display_estados
                ],expand=True )
            ], spacing=0),
            expand=True,
        )

    def __seleciona_regiao(self, e):
        self.page.session.set("select_cidade","")
        self.page.session.set("select_voto","")
        self.text_consulta_votos.value = "Consultar Votos"
        regiao = e.control.key
        dropdown_estados = ft.Dropdown(disabled=False)
        dropdown_cidades = ft.Dropdown(disabled=True)
        dropdown_candidatos = ft.Dropdown(disabled=True)
        btn_acessar =  ft.Container(
                        content=ft.Text("Pesquisar", size=22, weight='bold', text_align=ft.TextAlign.CENTER),
                        bgcolor=ft.Colors.GREEN_600,
                        width=200,
                        height=50,
                        border_radius=ft.border_radius.all(10),
                        alignment=ft.alignment.center,
                        on_click=self.__acessar_candidatos ,
                        disabled=True
                    )

        def retorna_candidatos_por_cidade(e):
            self.page.session.set("select_cidade", e.control.key)
            dropdown_candidatos.options.clear()
            dropdown_candidatos.disabled = False
            dropdown_candidatos.options.append(
                ft.dropdown.Option(key="13", text="VEREADOR", on_click=retira_disable_btn_acessar)
            )   
            dropdown_candidatos.options.append(
                ft.dropdown.Option(key="11", text="PREFEITO", on_click=retira_disable_btn_acessar)
            ) 
            self.page.update()   

        def retorna_cidades_por_estado(e):
            dropdown_cidades.options.clear()
            dropdown_cidades.disabled = False
            cidades = retorna_lista_cidade(e.control.key)
            for cidade in cidades:     
                dropdown_cidades.options.append(
                    ft.dropdown.Option(key=cidade.get("cod_cidade") ,text=cidade.get("nome"), on_click=retorna_candidatos_por_cidade),
                )

            self.page.update()

        def retira_disable_btn_acessar(e):
            self.page.session.set("select_voto", e.control.key)
            btn_acessar.disabled = False
            self.page.update() 

        def retorna_lista_candidatos_estado_cidade(e):
            print("Chegou aqui ")

        for estado in self.estados:
            if estado.get("regiao") == regiao and regiao != "brasil":
                
                dropdown_estados.options.append(
                    ft.dropdown.Option(key=estado.get("sigla") ,text=estado.get("estado").upper(), on_click=retorna_cidades_por_estado),
                )
                
            elif regiao == "brasil":
                
                dropdown_estados.options.append(
                    ft.dropdown.Option(key=estado.get("sigla") ,text=estado.get("estado"), on_click=retorna_cidades_por_estado),
                )

        coluna_principal = ft.Column(
            controls=[
                ft.Row([
                    ft.Text("Estado: ", size=22, weight='bold'),
                    dropdown_estados
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("Cidade: ", size=22, weight='bold'),
                    dropdown_cidades
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("Cargo: ", size=22, weight='bold'),
                    dropdown_candidatos
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Container(
                        height=60
                    )
                ]),
                ft.Row([
                    btn_acessar
                ], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        container_coluna_dropdown = ft.Container(
            content=coluna_principal,
            width=420,
            padding=10,
            alignment=ft.alignment.center
        )

        self.container_display_estados.content = None
        self.container_display_estados.content = container_coluna_dropdown
        self.container_display_estados.alignment = ft.alignment.center
        self.page.update()

    def build(self):
        return self.__container_principal_backoffice()