import flet as ft
import asyncio
from services.eleitor_api import add_eleitor_votante, retorna_candidato_voto, salva_voto_banco_dados, retorna_cod_cidade

class TelaUrna:
    def __init__(self, page):
        self.page = page
        page.title = "Urna Eletronica"
        page.window.height = 500
        page.window.width = 900
        self.container_display = self.__create_container_display()
        self.lista_candidatos = self.page.session.get("candidatos")
        self.lista_voto = self.page.session.get("lista_voto")
        self.dlg_modal_urna = ft.AlertDialog(title=ft.Text("", weight='bold'),modal=True )

    def __create_teclado_urna(self):
        
        lista_tecla1 = []
        lista_tecla2 = []
        lista_tecla3 = []
        lista_tecla4 = []
        lista_tecla5 = [
            ft.Container(content=ft.Text("BRANCO", color="black", size="15", text_align="center", weight="bold"), width=100, height=50, bgcolor=ft.Colors.WHITE, alignment=ft.alignment.center, on_click=self.__click_branco),
            ft.Container(content=ft.Text("CORRIGE", color="black", size="15", text_align="center", weight="bold"), width=100, height=50, bgcolor=ft.Colors.ORANGE_700, alignment=ft.alignment.center, on_click=self.__click_corrigir),  
            ft.Container(content=ft.Text("CONFIRMA", color="black", size="15", text_align="center", weight="bold"), width=100, height=50, bgcolor=ft.Colors.GREEN_700, alignment=ft.alignment.center, on_click=self.__click_confirma), 
        ]

        for i in range (10):
            if i in [1, 2, 3]:
                lista_tecla1.append(ft.Container(content=ft.Text(str(i), color="white", size="30", text_align="center", weight='bold'),width=80,height=50, bgcolor=ft.Colors.GREY_800, on_click=self.__computa_click))
            elif i in [4, 5, 6]:
                lista_tecla2.append(ft.Container(content=ft.Text(str(i),color="white", size="30", text_align="center", weight='bold'), width=80, height=50, bgcolor=ft.Colors.GREY_800, on_click=self.__computa_click))
            elif i in [7, 8, 9]:
                lista_tecla3.append(ft.Container(content=ft.Text(str(i), color="white",size="30", text_align="center", weight='bold'), width=80, height=50, bgcolor=ft.Colors.GREY_800, on_click=self.__computa_click))
            elif i in [ 0 ]:
                lista_tecla4.append(ft.Container(content=ft.Text(str(i),color="white", size="30", text_align="center", weight='bold'), width=80, height=50, bgcolor=ft.Colors.GREY_800, on_click=self.__computa_click))

        lista = [
            ft.Row(lista_tecla1, alignment=ft.MainAxisAlignment.CENTER), 
            ft.Row(lista_tecla2, alignment=ft.MainAxisAlignment.CENTER), 
            ft.Row(lista_tecla3, alignment=ft.MainAxisAlignment.CENTER), 
            ft.Row(lista_tecla4, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(lista_tecla5, alignment=ft.MainAxisAlignment.CENTER), 
        ]

        return lista

    def __content_container_display(self):
        votacao = self.page.session.get('votacao')
        posicao_votacao = self.page.session.get("posicao_voto")
        container_tela_urna = ft.Container(
            content=ft.Image(
                src="tse1.jpg",
                width=400
            ),
            width=500,
            expand=True,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(2, ft.Colors.BLACK),
        )

        return ft.Column([ft.Container(content=ft.Text(f"{str(votacao[posicao_votacao]).capitalize()}(a)", size=30, key="tipoVoto" ) ,height=60, width=500), container_tela_urna], spacing=5)

    def __create_container_display(self):
        container_display = ft.Container(
            content=self.__content_container_display(),
            width=500,
            expand=True,
        )
        
        return container_display

    def __create_conainter_numeros(self):
        container_teclado = ft.Container(
            content=ft.Column(self.__create_teclado_urna()),
            width=350,
            bgcolor=ft.Colors.GREY_900,
            expand=True,
            padding=ft.padding.only(top=50)
        )

        container_logo_teclado = ft.Container(
            content=ft.Row([ft.Image(src="tse3.png", width=150)], alignment=ft.MainAxisAlignment.END),
            width=350,
            height=60,
        )

        container_numeros = ft.Container(
            content=ft.Column([
                container_logo_teclado,
                container_teclado
            ], spacing=5),
            width=350,
            padding=0,
        )
        
        return container_numeros

    def __computa_click(self, e):
        self.page.session.set("nome_candidato","")
        __click = e.control.content.value
        __numeros_clicados = self.page.session.get('numeros_clicados')
        __lista_votacao = self.page.session.get('votacao')
        __posicao_voto = self.page.session.get('posicao_voto')
        __eleitor = self.page.session.get("eleitor")
        cidade = __eleitor['cidade']
        estado = __eleitor['estado']
        cod_cidade = retorna_cod_cidade(estado, cidade)

        if __lista_votacao[__posicao_voto] == "prefeito":
            tamanho_voto = 2
        elif __lista_votacao[__posicao_voto] == "vereador":
            tamanho_voto = 5

        if len(__numeros_clicados) < tamanho_voto:
            __numeros_clicados.append(__click)
            self.page.session.set('numeros_clicados', __numeros_clicados)
            if len(__numeros_clicados) == tamanho_voto:
                candidato = retorna_candidato_voto(self.lista_candidatos, "".join(__numeros_clicados), estado, cidade, cod_cidade)
                self.page.session.set("candidato", candidato)
                self.__apresenta_candidato_tela()
            else:
                self.__update_tela_candidato()

    async def __click_confirma(self, e ):
        __numeros_clicados = self.page.session.get("numeros_clicados")
        __posicao_voto = self.page.session.get("posicao_voto")
        __votacao = self.page.session.get("votacao")

        if __votacao[__posicao_voto] == "prefeito":
            self.page.session.set("tamanho_voto", 2)
        elif __votacao[__posicao_voto] == "vereador":
            self.page.session.set("tamanho_voto", 5)

        if (__numeros_clicados != [] and len(__numeros_clicados) == self.page.session.get("tamanho_voto")) or self.page.session.get("voto_branco"):
            __eleitor = self.page.session.get("eleitor")
            cidade = __eleitor['cidade']
            estado = __eleitor['estado']
            cod_cidade = retorna_cod_cidade(estado, cidade)

            if self.page.session.get("voto_branco"):
                id_voto_branco = []
                for i in range(self.page.session.get("tamanho_voto")):
                    id_voto_branco.append("8")
                candidato = {"id":"".join(id_voto_branco), "numero":"0", "nome": "branco", "cod_cidade":cod_cidade, "estado": estado, "cidade": cidade, "partido": "branco" }
            else:
                candidato = retorna_candidato_voto(self.lista_candidatos, "".join(__numeros_clicados), estado, cidade, cod_cidade)
            self.page.session.set("voto_branco", False)
            self.lista_voto.append(candidato)
            self.page.session.set("posicao_tecla", 0)
            self.page.session.set("numeros_clicados", [])

            if (__posicao_voto + 1) == len(self.page.session.get('votacao')):
                add_eleitor_votante(__eleitor["titulo_eleitor"])
                salva_voto_banco_dados(self.lista_voto)
                await self.open_dialog(e, "Votação Encerrada!\n")
                self.page.go("/")
            else:
                await self.open_dialog(e, "Voto Salvo com sucesso!\n")
                self.page.session.set('posicao_voto', __posicao_voto + 1)
                self.container_display.content.clean()
                self.container_display.border = None
                self.container_display.content = self.__content_container_display()
                self.page.update()
        else:
            await self.open_dialog(e, "Voto Inválido!\nInforme um voto VÁLIDO, NULO ou BRANCO!")

    def __click_corrigir(self, e):
        self.page.session.set('numeros_clicados', [])
        self.container_display.content.clean()
        self.container_display.border = None
        self.dlg_modal_urna.open = False
        self.container_display.content = self.__content_container_display()
        self.page.update()

    def __click_branco(self, e):
        self.page.session.set("numeros_clicados", [])
        self.page.session.set("candidato", None)
        self.page.session.set("voto_branco", True)
        self.__apresenta_candidato_tela()

    def __update_tela_candidato(self):
        __numeros_clicados = self.page.session.get('numeros_clicados')
        __lista_votacao = self.page.session.get('votacao')
        __posicao_voto = self.page.session.get("posicao_voto")
        linha = []

        if __lista_votacao[__posicao_voto] == "prefeito":
            tamanho_voto = 2
        elif __lista_votacao[__posicao_voto] == "vereador":
            tamanho_voto = 5

        for i in range(tamanho_voto):
            linha.append(ft.Text("_", size=150))

        for i, num in enumerate(__numeros_clicados):
            linha[i].value = num

        self.container_display.content = None
        self.container_display.content = ft.Column(
            controls=[
                    ft.Row(linha, alignment=ft.MainAxisAlignment.CENTER),
            ],
        )

        self.container_display.border = ft.border.all(2, ft.Colors.BLACK)
        self.page.update()

    def __apresenta_candidato_tela(self):
        __candidato = self.page.session.get("candidato")
        __numeros_clicados = self.page.session.get('numeros_clicados')
        __lista_votacao = self.page.session.get('votacao')
        __posicao_voto = self.page.session.get("posicao_voto")
        linha = []

        if __candidato:
            img = ft.Image(src=f"https://divulgacandcontas.tse.jus.br/divulga/rest/arquivo/img/2045202024/{__candidato['id']}/{__candidato['cod_cidade']}", expand=True, width=200)
            nome_txt = __candidato['nome']
            partido = __candidato['partido']
        else:
            img = ft.Image(src=f"https://divulgacandcontas.tse.jus.br/divulga/rest/arquivo/img/2045202024/999/999", width=200)
            nome_txt = "BRANCO"
            partido = "BRANCO"

        self.container_display.content = None
        self.container_display.content = ft.Column(
            spacing=0,
            controls=[ft.Container(
                    content=ft.Row([
                        ft.Container(content=ft.Column(
                            controls=[
                                ft.Row([
                                    ft.Text(f"SEU VOTO PARA", size=18),
                                    ft.Text(f"{__lista_votacao[__posicao_voto].upper()}(A)", size=21, weight='bold'),
                                ]),
                                ft.Row([
                                    ft.Text(f"Número: ", size=18),
                                    ft.Text("".join(__numeros_clicados), size=21, weight='bold'),
                                ]),
                                ft.Row([
                                    ft.Text(f"Nome: ", size=18),
                                    ft.Column(controls=[ft.Text(nome_txt, size=21, weight='bold')], width=230) ,
                                    
                                ]),
                                ft.Row([
                                    ft.Text(f"Partido: ", size=18),
                                    ft.Text(partido, size=21, weight='bold'),
                                ]),
                            ]
                        ),height=240, expand=True, alignment=ft.alignment.center, padding=10),
                        ft.Container(content=img,width=180, height=300, border=ft.border.only(left=ft.border.BorderSide(2, ft.Colors.BLACK)))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN ),
                    
                ),
                 ft.Container(
                     content=ft.Column(
                        controls=[
                            ft.Text("Aperte a tecla:", size=22),
                            ft.Text("VERDE para CONFIRMAR", size=25, weight='bold'),
                            ft.Text("LARANJA para CORRIGIR", size=25,  weight='bold'), 
                        ],
                        spacing=0,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),  expand=True,width=555, border=ft.border.only(top=ft.border.BorderSide(2, ft.Colors.BLACK))
                 ),

            ],
        )
        self.page.update()

    async def open_dialog(self,e, msg ):
        try:
            e.control.page.overlay.pop()
        except Exception as err:
            print(err)
        e.control.page.overlay.append(self.dlg_modal_urna)
        self.dlg_modal_urna.content = ft.Text(msg, size=20, weight='bold')
        self.dlg_modal_urna.open = True
        e.control.page.update()
        await asyncio.sleep(3)
        self.dlg_modal_urna.open = False
        e.control.page.update()
        
    def build(self):
        return ft.Container(content=ft.Row([self.container_display, self.__create_conainter_numeros()]), expand=True, padding=5)

    