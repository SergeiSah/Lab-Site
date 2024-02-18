from sqlalchemy import MetaData, Table, create_engine, select, insert
from chemparse import parse_formula
from download_compound_properties import SpringerMaterialsManager
import pandas as pd


class CompoundsDB:

    def __init__(self):
        metadata = MetaData()
        self.engine = create_engine(f"sqlite+pysqlite:///./Compounds.db")
        self.connection = self.engine.connect()

        self.compounds = Table('Compound', metadata, autoload=True, autoload_with=self.engine)
        self.sources = Table('Source', metadata, autoload=True, autoload_with=self.engine)
        self.densities = Table('Density', metadata, autoload=True, autoload_with=self.engine)

    def add_record(self, properties: dict):
        """
        :param properties: must be a dict with structure
        {
         'name': name of a chemical compound (str),
         'formula': chemical formula of a compound (str),
         'density': float,
         'mol_weight': molecular weight of a compound (float),
         'source': the name of the source from which the data was taken (str),
         'id_in_source': identification number of the compound in the source (int)
         }
        :return: None, the function records data to the database 'Compounds.db'
        """
        if self.is_id_in_db(properties['id']):
            print('The record is already in the database')
            return

        if not self.is_source_in_db(properties['source']):
            self.connection.execute(insert(self.sources).values(name=properties['source']))

        query = select([self.sources.c.id]).select_from(self.sources).where(self.sources.c.name == properties['source'])
        source_id = self.connection.execute(query).fetchone()[0]

        if not self.is_compound_in_db(properties['formula']):
            self.connection.execute(insert(self.compounds).values(name=properties['name'],
                                                                  formula=properties['formula']))

        query = select([self.compounds.c.id, self.compounds.c.formula]).select_from(self.compounds)
        comps = pd.DataFrame(self.connection.execute(query).fetchall(), columns=['id', 'formula'])
        compound_id = comps[comps['formula'].apply(parse_formula) == parse_formula(properties['formula'])]['id'].values[0]

        self.connection.execute(insert(self.densities).values(compound_id=int(compound_id),
                                                              density=properties['density'],
                                                              mol_weight=properties['mol_weight'],
                                                              source_id=source_id,
                                                              id_in_source=properties['id']))

    def is_compound_in_db(self, compound) -> bool:
        query = select([self.compounds.c.formula]).select_from(self.compounds)
        chem_comp = pd.DataFrame(self.connection.execute(query).fetchall(), columns=['formula'])
        if chem_comp[chem_comp['formula'].apply(parse_formula) == parse_formula(compound)].empty:
            return False
        return True

    def is_source_in_db(self, source) -> bool:
        query = select([self.sources.c.name]).select_from(self.sources).where(self.sources.c.name == source)
        if len(self.connection.execute(query).fetchall()) > 0:
            return True
        return False

    def is_id_in_db(self, id_in_source) -> bool:
        query = select([self.densities.c.id_in_source]).select_from(self.densities)\
            .where(self.densities.c.id_in_source == id_in_source)
        if len(self.connection.execute(query).fetchall()) > 0:
            return True
        return False


if __name__ == '__main__':
    comp = SpringerMaterialsManager()
    sd = comp.search_sds('Cr2Ti')[0]
    p = comp.get_properties(sd)
    p['name'] = 'Chromium titanate'

    print(p)

    db = CompoundsDB()
    db.add_record(p)