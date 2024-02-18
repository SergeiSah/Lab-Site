from plugins import db


# ---------- X-ray models ----------
class Element(db.Model):
    __bind_key__ = 'Elements'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Z = db.Column(db.Integer, nullable=False)
    Element = db.Column(db.String, nullable=False)
    Atomic_weight = db.Column(db.Float, nullable=False)
    Density = db.Column(db.Float)
    Melting_point = db.Column(db.Float)
    Boiling_point = db.Column(db.Float)

    def __repr__(self):
        return f"<Element {self.id}>"

    def __str__(self):
        return self.Element


class Compound(db.Model):
    __bind_key__ = 'Compounds'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    formula = db.Column(db.String)

    def __repr__(self):
        return f"<Compounds {self.id}>"

    def __str__(self):
        return self.Formula


class Density(db.Model):
    __bind_key__ = 'Density'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    compound_id = db.Column(db.Integer, db.ForeignKey('Compounds.id'), nullable=False)
    density = db.Column(db.Float)
    mol_weight = db.Column(db.Float)
    source_id = db.Column(db.Integer)
    id_in_source = db.Column(db.Integer)

    def __repr__(self):
        return f"<Density {self.id}>"

    def __str__(self):
        return self.source_name
