import flet as ft
import sys

sys.path.insert(
    0,
    r"C:\Users\Aluno\Documents\SISTEMA BIBLIOTECA\Database"
)

from db import criar_tabelas
from View.loguin import Login

def main(page: ft.Page):

    page.window.maximized = True
    page.window.maximizable = True
    page.window.resizable = True

    criar_tabelas()

    Login(page)

ft.app(target=main)