class Article:
    def __init__(self, id, titre, contenu):
        self.id = id
        self.titre = titre
        self.contenu = contenu

    categorie = "python"

    def __repr__(self):
        return f"Article(id={self.id}, titre='{self.titre}', contenu='{self.contenu}')"


class Categorie:
    def __init__(self, id, libelle):
        self.id = id
        self.libelle = libelle

    def __repr__(self):
        return f"Categorie(id={self.id}, libelle='{self.libelle}')"
