import flet as ft
import sys

sys.path.insert(
    0,
    r"C:\Users\Aluno\Documents\SISTEMA BIBLIOTECA\Database"
)

from db import get_conn


def Login(page: ft.Page):

    page.controls.clear()

    page.title = "Login"
    page.padding = 0
    page.bgcolor = "white"

    usuario = ft.TextField(
        label="Usuário",
        width=280,
        prefix_icon=ft.Icons.PERSON
    )

    senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=280,
        prefix_icon=ft.Icons.LOCK
    )

    def mensagem(texto):

        snack = ft.SnackBar(
            content=ft.Text(texto),
            bgcolor="red"
        )

        page.overlay.append(snack)
        snack.open = True

        page.update()

    def validacao(e):

        nome_usuario = usuario.value.strip()
        nome_senha = senha.value.strip()

        if not nome_usuario or not nome_senha:

            mensagem(
                "Informe usuário e senha."
            )

            return

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT ID_USUARIO, NOME
            FROM USUARIOS
            WHERE USUARIO=? AND SENHA=?
            """,
            (
                nome_usuario,
                nome_senha
            )
        )

        user = cur.fetchone()

        conn.close()

        if user:

            page.controls.clear()

            from View.tela_principal import tela_principal

            tela_principal(page)

        else:

            mensagem(
                "Usuário ou senha inválidos."
            )

    def ir_cadastro(e):

        page.controls.clear()

        from View.tl_cadastro import tl_cadastro

        tl_cadastro(page)

    formulario = ft.Container(
        width=450,
        expand=True,
        bgcolor="white",

        content=ft.Column(
            [
                ft.Text(
                    "Login",
                    size=32,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Sistema de Biblioteca",
                    color="grey"
                ),

                usuario,
                senha,

                ft.CupertinoButton(
                    "ENTRAR",
                    width=180,
                    height=50,
                    bgcolor="blue",
                    color="white",
                    on_click=validacao
                ),

                ft.TextButton(
                    "Não tem conta? Cadastre-se",
                    on_click=ir_cadastro
                )
            ],

            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,

            alignment=
            ft.MainAxisAlignment.CENTER,

            spacing=15
        ),

        alignment=ft.Alignment.CENTER
    )

    apresentacao = ft.Container(
        expand=True,
        bgcolor="blue",

        content=ft.Column(
            [
                ft.Image(
                    src="Assets\livro.png",
                    width=500,
                    height=350
                ),

                ft.Text(
                    "Entre páginas e silêncio,\n"
                    "encontro um mundo inteiro!",
                    color="white",
                    size=30,
                    text_align="center",
                    italic=True
                )
            ],

            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,

            alignment=
            ft.MainAxisAlignment.CENTER,

            spacing=40
        )
    )

    page.add(
        ft.Row(
            [
                formulario,
                apresentacao
            ],

            spacing=0,
            expand=True
        )
    )

    page.update()