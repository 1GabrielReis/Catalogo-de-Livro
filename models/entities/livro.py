class Livro:
    def __init__(self, id: int,  titulo: str, autor: str, editora: str, sobre: str):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.sobre = sobre

    def __repr__(self):
        return f"({self.id}, {self.titutlo}, {self.autor}, {self.editora}, {self.sobre})"

