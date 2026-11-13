import sqlite3
import os

DB = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "biblioteca1.db"
)

def get_conn():
    return sqlite3.connect(DB)


def criar_tabelas():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ALUNO (
            ID_ALUNO INTEGER PRIMARY KEY AUTOINCREMENT,
            NOME TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS LIVRO (
            ID_LIVRO INTEGER PRIMARY KEY AUTOINCREMENT,
            NOME_LIVRO TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS EMPRESTIMO (
            ID_EMPRESTIMO INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_ALUNO INTEGER,
            ID_LIVRO INTEGER,
            DATA_RETIRADA TEXT,
            DATA_DEVOLUCAO TEXT,
            FOREIGN KEY (ID_ALUNO) REFERENCES ALUNO(ID_ALUNO),
            FOREIGN KEY (ID_LIVRO) REFERENCES LIVRO(ID_LIVRO)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS USUARIOS (
            ID_USUARIO INTEGER PRIMARY KEY AUTOINCREMENT,
            NOME TEXT NOT NULL,
            USUARIO TEXT NOT NULL UNIQUE,
            SENHA TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def contar_livros():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM LIVRO")
    resultado = cur.fetchone()[0]
    conn.close()
    return resultado


def contar_alunos():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM ALUNO")
    resultado = cur.fetchone()[0]
    conn.close()
    return resultado


def contar_emprestimos():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM EMPRESTIMO")
    resultado = cur.fetchone()[0]
    conn.close()
    return resultado