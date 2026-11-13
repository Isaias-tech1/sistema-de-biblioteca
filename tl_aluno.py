import flet as ft
import sys

sys.path.insert(
    0,
    r"C:\Users\Aluno\Documents\SISTEMA BIBLIOTECA\Database"
)

from db import get_conn


def tl_aluno(page: ft.Page):

    nome_field = ft.TextField(
        label="Nome do Aluno",
        hint_text="Digite o nome completo",
        expand=True
    )

    lista = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=5
    )

    editando_id = {"id": None}

    def mensagem(texto, cor="green"):
        snack = ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=cor
        )

        page.overlay.append(snack)
        snack.open = True
        page.update()

    def carregar():

        lista.controls.clear()

        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT ID_ALUNO, NOME
            FROM ALUNO
            ORDER BY NOME
        """)

        alunos = cur.fetchall()

        conn.close()

        if not alunos:
            lista.controls.append(
                ft.Text(
                    "Nenhum aluno cadastrado.",
                    color="grey"
                )
            )

        for id_aluno, nome in alunos:

            lista.controls.append(
                ft.Container(
                    padding=8,
                    border=ft.Border.all(1, "#dddddd"),
                    border_radius=8,
                    content=ft.Row(
                        [
                            ft.Text(
                                f"{id_aluno} - {nome}",
                                expand=True
                            ),

                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar",
                                on_click=lambda e,
                                i=id_aluno,
                                n=nome: editar(i, n)
                            ),

                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color="red",
                                tooltip="Excluir",
                                on_click=lambda e,
                                i=id_aluno: deletar(i)
                            )
                        ]
                    )
                )
            )

        page.update()

    def salvar(e):

        nome = nome_field.value.strip()

        if not nome:
            mensagem(
                "Digite o nome do aluno.",
                "red"
            )
            return

        conn = get_conn()
        cur = conn.cursor()

        if editando_id["id"] is None:

            cur.execute(
                "INSERT INTO ALUNO (NOME) VALUES (?)",
                (nome,)
            )

            mensagem("Aluno cadastrado com sucesso!")

        else:

            cur.execute(
                """
                UPDATE ALUNO
                SET NOME=?
                WHERE ID_ALUNO=?
                """,
                (
                    nome,
                    editando_id["id"]
                )
            )

            editando_id["id"] = None

            mensagem("Aluno atualizado com sucesso!")

        conn.commit()
        conn.close()

        nome_field.value = ""

        carregar()

    def editar(id_aluno, nome):

        editando_id["id"] = id_aluno
        nome_field.value = nome

        page.update()

    def deletar(id_aluno):

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "SELECT COUNT(*) FROM EMPRESTIMO WHERE ID_ALUNO=?",
            (id_aluno,)
        )

        quantidade = cur.fetchone()[0]

        if quantidade > 0:

            conn.close()

            mensagem(
                "Não é possível excluir um aluno com empréstimos.",
                "red"
            )

            return

        cur.execute(
            "DELETE FROM ALUNO WHERE ID_ALUNO=?",
            (id_aluno,)
        )

        conn.commit()
        conn.close()

        mensagem("Aluno excluído com sucesso!")

        carregar()

    carregar()

    return ft.Container(
        expand=True,
        padding=20,

        content=ft.Column(
            [
                ft.Text(
                    "Gerenciar Alunos",
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Row(
                    [
                        nome_field,

                        ft.ElevatedButton(
                            "Salvar",
                            icon=ft.Icons.SAVE,
                            on_click=salvar
                        )
                    ]
                ),

                ft.Divider(),

                ft.Text(
                    "Alunos cadastrados",
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),

                lista
            ],
            expand=True
        )
    )