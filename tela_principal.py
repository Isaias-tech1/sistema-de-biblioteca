import flet as ft

from View.tl_aluno import tl_aluno
from View.tl_deshiboar import tl_deshiboar
from View.tl_emprestimo import tl_emprestimo
from View.tl_livros import tl_livros


def tela_principal(page: ft.Page):

    page.controls.clear()

    page.title = "Sistema de Biblioteca"
    page.padding = 0
    page.bgcolor = "#f5f6fa"

    area = ft.Container(
        expand=True,
        padding=20
    )

    def mostrar(tela_nome):

        if tela_nome == "dashboard":

            area.content = tl_deshiboar(page)

        elif tela_nome == "aluno":

            area.content = tl_aluno(page)

        elif tela_nome == "livros":

            area.content = tl_livros(page)

        elif tela_nome == "emprestimos":

            area.content = tl_emprestimo(page)

        area.update()

    def sair(e):

        page.controls.clear()

        from View.loguin import Login

        Login(page)

    menu = ft.Container(
        width=200,
        bgcolor="blue",
        padding=15,

        content=ft.Column(
            [
                ft.Container(
                    padding=10,

                    content=ft.Image(
                        src="assets/livros.png",
                        width=150,
                        height=100
                    )
                ),

                ft.Text(
                    "BIBLIOTECA",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="white"
                ),

                ft.Divider(
                    color="white"
                ),

                ft.ElevatedButton(
                    "Dashboard",
                    icon=ft.Icons.DASHBOARD,
                    width=170,
                    on_click=lambda e:
                        mostrar("dashboard")
                ),

                ft.ElevatedButton(
                    "Alunos",
                    icon=ft.Icons.PEOPLE,
                    width=170,
                    on_click=lambda e:
                        mostrar("aluno")
                ),

                ft.ElevatedButton(
                    "Livros",
                    icon=ft.Icons.BOOK,
                    width=170,
                    on_click=lambda e:
                        mostrar("livros")
                ),

                ft.ElevatedButton(
                    "Empréstimos",
                    icon=ft.Icons.SWAP_HORIZ,
                    width=170,
                    on_click=lambda e:
                        mostrar("emprestimos")
                ),

                ft.Container(
                    expand=True
                ),

                ft.ElevatedButton(
                    "Sair",
                    icon=ft.Icons.EXIT_TO_APP,
                    width=170,
                    on_click=sair
                )
            ],

            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,

            expand=True
        )
    )

    layout = ft.Row(
        [
            menu,
            area
        ],

        spacing=0,
        expand=True
    )

    page.add(layout)

    mostrar("dashboard")

    page.update()