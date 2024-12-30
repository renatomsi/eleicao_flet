import flet as ft
from pages.urna import TelaUrna
from pages.home import HomePage
from pages.backoffice import Backoffice

def route_change(e):
    page = e.page
    page.views.clear()
    if page.route == "/":
        home = HomePage(page)
        page.views.append(
            ft.View(route="/", controls=[home.build()])
        )
    elif page.route == "/urna":
        urna = TelaUrna(page)
        page.views.append(
            ft.View(route="/urna", controls=[urna.build()])
        )
    elif page.route == "/backoffice":
        backoffice = Backoffice(page)
        page.views.append(
            ft.View(route="/backoffice", controls=[backoffice.build()])
        )

    page.update()

def main(page: ft.Page):
    page.theme_mode = "white"
    page.on_route_change = route_change
    page.go("/")

ft.app(main)
