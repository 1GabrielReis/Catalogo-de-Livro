from typing import Optional
from datetime import date

class Livro:
    def __init__(self, id: Optional[str],  titulo: str, autor: str, editora: str, sobre: str, data_criacao: date):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.sobre = sobre
        self.data_criacao = data_criacao

    def __repr__(self):
        return f"({self.id}, {self.titutlo}, {self.autor}, {self.editora}, {self.sobre})"

