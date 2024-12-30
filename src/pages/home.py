import flet as ft
import asyncio
from services.eleitor_api import consulta_eleitor, retorna_candidatos_da_cidade

class HomePage:
    def __init__(self, page):
        self.page = page
        page.title = "Eleição 2024"
        page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        page.window.resizable = False
        page.window.maximizable = False
        page.window.height = 600
        page.window.width = 700
        page.bgcolor = ft.Colors.WHITE
        page.session.set('numeros_clicados', [])
        page.session.set('posicao_tecla', 0 )
        page.session.set('posicao_voto', 0)
        page.session.set('votacao', ["vereador", "prefeito"])
        page.session.set("lista_voto", [])
        self.dlg_modal = ft.AlertDialog(title=ft.Text("Atenção!", weight='bold'),modal=True, open=False )

    async def get_num_titulo(self, e):
        if self.num_titulo.value == "999999":
            self.page.go("/backoffice")
        else:
            response_eleitor = consulta_eleitor(self.num_titulo.value)
            if isinstance(response_eleitor, dict):
                print("Acesso Liberado")
                print(response_eleitor)
                votacao = self.page.session.get('votacao')
                candidatos = retorna_candidatos_da_cidade(response_eleitor['estado'], response_eleitor['cidade'], votacao)
                self.page.session.set("candidatos", candidatos)
                self.page.session.set("eleitor", response_eleitor )
                self.page.go("/urna")
            elif response_eleitor == 2:
                await self.open_dialog(e, "Titulo de eleitor não encontrado")
                print("Titulo de eleitor não encontrado")
                self.num_titulo.value = ""
                self.page.update()
            elif response_eleitor == 1:
                await self.open_dialog(e, "Eleitor já votou!")
                print("Eleitor já votou!")
                self.num_titulo.value = ""
                self.page.update()

    async def open_dialog(self,e, msg ):
        try:
            e.control.page.overlay.pop()
        except Exception as err:
            print(err)
        e.control.page.overlay.append(self.dlg_modal)
        self.dlg_modal.content = ft.Text(msg, size=20)
        self.dlg_modal.open = True
        e.control.page.update()
        await asyncio.sleep(3)
        self.dlg_modal.open = False
        e.control.page.update()
        
    def build(self):
        btn_inicio = ft.CupertinoFilledButton(
            text="Começar",
            on_click=self.get_num_titulo
        )

        self.num_titulo = ft.TextField(
            autofocus=True,
            width=300,
            helper_text="Informe seu titulo de eleitor\nOu 999999 para acessar Backoffice",
            #on_submit=lambda e: self.page.go("/urna")
            on_submit=self.get_num_titulo
        )

        coluna_entrada = ft.Column(
            controls=
            [   
                ft.Image(
                    src="logo.jpg",
                    width=450,
                ),
                ft.Container(
                    content=ft.Row([self.num_titulo,], alignment=ft.MainAxisAlignment.CENTER),
                    width= 450
                ),
                ft.Container(
                    content=ft.Row([btn_inicio,], alignment=ft.MainAxisAlignment.CENTER),
                    width= 450
                )
                
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=25,
        )

        return ft.Container(
            content=coluna_entrada,
            alignment=ft.alignment.center,
            padding=0,
            expand=True
        )
            #ft.Text("Tela principal"),
            #ft.ElevatedButton("Acessar segunda pagina", on_click=lambda e: self.page.go("/urna") )
        