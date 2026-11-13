import flet as ft
import sys

sys.path.insert(
    0,
    r"C:\Users\Aluno\Documents\SISTEMA BIBLIOTECA\Database"
)

from db import get_conn


def tl_livros(page: ft.Page):

    nome_field = ft.TextField(
        label="Nome do Livro",
        hint_text="Digite o nome do livro",
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
            SELECT ID_LIVRO, NOME_LIVRO
            FROM LIVRO
            ORDER BY NOME_LIVRO
        """)

        livros = cur.fetchall()

        conn.close()

        if not livros:

            lista.controls.append(
                ft.Text(
                    "Nenhum livro cadastrado.",
                    color="grey"
                )
            )

        for id_livro, nome in livros:

            lista.controls.append(
                ft.Container(
                    padding=8,
                    border=ft.Border.all(
                        1,
                        "#dddddd"
                    ),
                    border_radius=8,

                    content=ft.Row(
                        [
                            ft.Text(
                                f"{id_livro} - {nome}",
                                expand=True
                            ),

                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar",
                                on_click=lambda e,
                                i=id_livro,
                                n=nome: editar(i, n)
                            ),

                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color="red",
                                tooltip="Excluir",
                                on_click=lambda e,
                                i=id_livro: deletar(i)
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
                "Digite o nome do livro.",
                "red"
            )

            return

        conn = get_conn()
        cur = conn.cursor()

        if editando_id["id"] is None:

            cur.execute(
                """
                INSERT INTO LIVRO (NOME_LIVRO)
                VALUES (?)
                """,
                (nome,)
            )

            mensagem("Livro cadastrado com sucesso!")

        else:

            cur.execute(
                """
                UPDATE LIVRO
                SET NOME_LIVRO=?
                WHERE ID_LIVRO=?
                """,
                (
                    nome,
                    editando_id["id"]
                )
            )

            editando_id["id"] = None

            mensagem("Livro atualizado com sucesso!")

        conn.commit()
        conn.close()

        nome_field.value = ""

        carregar()

    def editar(id_livro, nome):

        editando_id["id"] = id_livro
        nome_field.value = nome

        page.update()

    def deletar(id_livro):

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT COUNT(*)
            FROM EMPRESTIMO
            WHERE ID_LIVRO=?
            """,
            (id_livro,)
        )

        quantidade = cur.fetchone()[0]

        if quantidade > 0:

            conn.close()

            mensagem(
                "Não é possível excluir um livro com empréstimos.",
                "red"
            )

            return

        cur.execute(
            """
            DELETE FROM LIVRO
            WHERE ID_LIVRO=?
            """,
            (id_livro,)
        )

        conn.commit()
        conn.close()

        mensagem("Livro excluído com sucesso!")

        carregar()

    carregar()

    return ft.Container(
        expand=True,
        padding=20,

        content=ft.Column(
            [
                ft.Text(
                    "Gerenciar Livros",
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
                    "Livros cadastrados",
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),

                lista
            ],
            expand=True
        )
    )