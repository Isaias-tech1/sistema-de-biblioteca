import flet as ft
import sys

from datetime import date

sys.path.insert(
    0,
    r"C:\Users\Aluno\Documents\SISTEMA BIBLIOTECA\Database"
)

from db import get_conn


def tl_emprestimo(page: ft.Page):

    dd_aluno = ft.Dropdown(
        label="Aluno",
        expand=True
    )

    dd_livro = ft.Dropdown(
        label="Livro",
        expand=True
    )

    dt_retirada = ft.TextField(
        label="Data de Retirada",
        value=str(date.today()),
        expand=True
    )

    dt_devolucao = ft.TextField(
        label="Data de Devolução",
        expand=True
    )

    lista = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    def mensagem(texto, cor="green"):

        snack = ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=cor
        )

        page.overlay.append(snack)
        snack.open = True
        page.update()

    def carregar_dropdowns():

        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT ID_ALUNO, NOME
            FROM ALUNO
            ORDER BY NOME
        """)

        alunos = cur.fetchall()

        cur.execute("""
            SELECT ID_LIVRO, NOME_LIVRO
            FROM LIVRO
            ORDER BY NOME_LIVRO
        """)

        livros = cur.fetchall()

        conn.close()

        dd_aluno.options = [
            ft.DropdownOption(
                key=str(id_aluno),
                text=nome
            )
            for id_aluno, nome in alunos
        ]

        dd_livro.options = [
            ft.DropdownOption(
                key=str(id_livro),
                text=nome
            )
            for id_livro, nome in livros
        ]

    def carregar():

        lista.controls.clear()

        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                E.ID_EMPRESTIMO,
                A.NOME,
                L.NOME_LIVRO,
                E.DATA_RETIRADA,
                E.DATA_DEVOLUCAO

            FROM EMPRESTIMO E

            JOIN ALUNO A
            ON E.ID_ALUNO = A.ID_ALUNO

            JOIN LIVRO L
            ON E.ID_LIVRO = L.ID_LIVRO

            ORDER BY E.ID_EMPRESTIMO DESC
        """)

        emprestimos = cur.fetchall()

        conn.close()

        if not emprestimos:

            lista.controls.append(
                ft.Text(
                    "Nenhum empréstimo registrado.",
                    color="grey"
                )
            )

        for row in emprestimos:

            id_emp, aluno, livro, retirada, devolucao = row

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
                                f"#{id_emp} | "
                                f"{aluno} | "
                                f"{livro} | "
                                f"{retirada} → "
                                f"{devolucao or 'Não informada'}",
                                expand=True
                            ),

                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color="red",
                                tooltip="Excluir",
                                on_click=lambda e,
                                i=id_emp: deletar(i)
                            )
                        ]
                    )
                )
            )

        page.update()

    def salvar(e):

        if not dd_aluno.value:

            mensagem(
                "Selecione um aluno.",
                "red"
            )

            return

        if not dd_livro.value:

            mensagem(
                "Selecione um livro.",
                "red"
            )

            return

        if not dt_retirada.value.strip():

            mensagem(
                "Informe a data de retirada.",
                "red"
            )

            return

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO EMPRESTIMO
            (
                ID_ALUNO,
                ID_LIVRO,
                DATA_RETIRADA,
                DATA_DEVOLUCAO
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                dd_aluno.value,
                dd_livro.value,
                dt_retirada.value,
                dt_devolucao.value
            )
        )

        conn.commit()
        conn.close()

        dd_aluno.value = None
        dd_livro.value = None

        mensagem(
            "Empréstimo registrado com sucesso!"
        )

        carregar_dropdowns()
        carregar()

    def deletar(id_emp):

        conn = get_conn()

        conn.execute(
            """
            DELETE FROM EMPRESTIMO
            WHERE ID_EMPRESTIMO=?
            """,
            (id_emp,)
        )

        conn.commit()
        conn.close()

        mensagem(
            "Empréstimo excluído."
        )

        carregar()

    carregar_dropdowns()
    carregar()

    return ft.Container(
        expand=True,
        padding=20,

        content=ft.Column(
            [
                ft.Text(
                    "Gerenciar Empréstimos",
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Row(
                    [
                        dd_aluno,
                        dd_livro
                    ]
                ),

                ft.Row(
                    [
                        dt_retirada,
                        dt_devolucao
                    ]
                ),

                ft.ElevatedButton(
                    "Registrar Empréstimo",
                    icon=ft.Icons.SWAP_HORIZ,
                    on_click=salvar
                ),

                ft.Divider(),

                ft.Text(
                    "Empréstimos registrados",
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),

                lista
            ],
            expand=True
        )
    )