class Biblioteca_settings:
    def __init__(self, base_url, username, parametro = ''):
        self.base_url: str = base_url 
        self.username: str = username
        self.parametro: str = parametro

    def __repr__(self):
        return f'{self.base_url}/{self.username}/{self.parametro}'