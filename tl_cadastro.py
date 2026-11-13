import flet as ft
import sys

sys.path.insert(
    0,
    r"C:\Users\Aluno\Documents\SISTEMA BIBLIOTECA\Database"
)

from db import get_conn


def tl_cadastro(page: ft.Page):

    page.controls.clear()

    nome = ft.TextField(
        label="Nome Completo",
        width=280
    )

    usuario = ft.TextField(
        label="Usuário",
        width=280
    )

    senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=280
    )

    confirmar = ft.TextField(
        label="Confirmar Senha",
        password=True,
        can_reveal_password=True,
        width=280
    )

    def mensagem(texto, cor="red"):

        snack = ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=cor
        )

        page.overlay.append(snack)
        snack.open = True

        page.update()

    def cadastrar(e):

        nome_value = nome.value.strip()
        usuario_value = usuario.value.strip()
        senha_value = senha.value.strip()
        confirmar_value = confirmar.value.strip()

        if not all([
            nome_value,
            usuario_value,
            senha_value,
            confirmar_value
        ]):

            mensagem(
                "Preencha todos os campos."
            )

            return

        if senha_value != confirmar_value:

            mensagem(
                "As senhas não coincidem."
            )

            return

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT ID_USUARIO
            FROM USUARIOS
            WHERE USUARIO=?
            """,
            (usuario_value,)
        )

        if cur.fetchone():

            conn.close()

            mensagem(
                "Esse usuário já existe."
            )

            return

        cur.execute(
            """
            INSERT INTO USUARIOS
            (
                NOME,
                USUARIO,
                SENHA
            )
            VALUES (?, ?, ?)
            """,
            (
                nome_value,
                usuario_value,
                senha_value
            )
        )

        conn.commit()
        conn.close()

        mensagem(
            "Cadastro realizado com sucesso!",
            "green"
        )

        voltar(None)

    def voltar(e):

        page.controls.clear()

        from View.loguin import Login

        Login(page)

    formulario = ft.Container(
        width=450,
        expand=True,
        bgcolor="white",

        content=ft.Column(
            [
                ft.Text(
                    "Cadastro",
                    size=32,
                    weight=ft.FontWeight.BOLD
                ),

                nome,
                usuario,
                senha,
                confirmar,

                ft.CupertinoButton(
                    "CADASTRAR",
                    width=180,
                    height=50,
                    bgcolor="blue",
                    color="white",
                    on_click=cadastrar
                ),

                ft.TextButton(
                    "Já tem conta? Voltar ao login",
                    on_click=voltar
                )
            ],

            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,

            alignment=
            ft.MainAxisAlignment.CENTER,

            spacing=12
        ),

        alignment=ft.Alignment.CENTER
    )

    apresentacao = ft.Container(
        expand=True,
        bgcolor="blue",

        content=ft.Column(
            [
                ft.Image(
                    src="Assets\handshake.png",
                    width=500,
                    height=250
                ),

                ft.Text(
                    "Bem Vindo!",
                    color="white",
                    size=50,
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