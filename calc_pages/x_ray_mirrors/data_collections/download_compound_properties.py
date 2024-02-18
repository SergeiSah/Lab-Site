"""
PubChem
CAS Common Chemistry*
Springer Materials
Materials Project*
"""
import re
import requests
from bs4 import BeautifulSoup
from typing import Final
from statistics import mode, mean
from chemparse import parse_formula
from element_properties import ElementsManager
import pandas as pd
import os
import time


class PubChemManager:
    URL_SEARCH_BY_FORMULA: Final = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastformula/'
    URL_GET_FROM_WEBPAGE: Final = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/'

    def __init__(self):
        self._soup = None
        self._current_cid = None

    def search_cids(self, chemical_formula):
        response = requests.get(self.URL_SEARCH_BY_FORMULA + chemical_formula + '/cids/JSON')
        if response.status_code == 200:
            return response.json()['IdentifierList']['CID']
        return []

    def get_properties(self, cid):
        self._get_xml_page(cid)

        return {
            'formula': self._get_molecular_formula(),
            'name': self._get_chem_name(),
            'density': self._get_density(),
            'mol_weight': self._get_mol_weight(),
            'id': self._current_cid,
            'source': 'PubChem'
        }

    def _get_xml_page(self, cid):
        response = requests.get(self.URL_GET_FROM_WEBPAGE + str(cid) + '/XML')
        if response.status_code == 200:
            self._soup = BeautifulSoup(response.content, features='xml')
            self._current_cid = cid

    def _get_density(self, few_val_process='mode'):
        str_densities = self._find_strings("Density")
        if str_densities is None:
            return None

        # Process '<String>...</String>' and values like '18.7-19.3'
        densities = []
        for s in str_densities:
            d = (re.findall(r'[\d.]+[\d.\-]*', s.find(string=True)))
            # TODO: работает некорректно, пример CID 5461123
            dens = list(filter(lambda x: float(x.split('-')[0]) // 100 == 0, d))[0]
            if '-' in dens:
                dens = mean(map(float, dens.split('-')))
            densities.append(float(dens))

        print(f'Densities for the compound {self._current_cid}: {densities}')

        if few_val_process == 'mode':
            return mode(densities)
        elif few_val_process == 'mean':
            return mean(densities)
        else:
            return densities[0]

    def _get_mol_weight(self):
        str_mol_weight = self._find_strings("Molecular Weight")[0]
        return float(str_mol_weight.find(string=True))

    def _get_molecular_formula(self):
        return self._find_strings("Molecular Formula")[0].find(string=True)

    def _get_chem_name(self):
        return self._soup.find('RecordTitle').find(string=True)

    def _find_strings(self, property_name: str):
        # Find <String>...</String> with needed property value
        try:
            strings = self._soup.find('TOCHeading', string=re.compile(property_name)).parent.find_all('String')
        except AttributeError:
            return None
        return strings


class SpringerMaterialsManager:
    SM_URL = 'https://materials.springer.com/'
    ISP_URL = 'isp/crystallographic/docs/'  # URL for 'Inorganic Solid Phases' data collection
    package_directory = os.path.dirname(os.path.abspath(__file__))
    PATH_TO_ELEMENT_PROPERTIES = os.path.join(package_directory, '../../substance_properties')
    params = {
        'searchTerm': '',            # Chem formula to be found
        'datasourceFacet': 'sm_isp'  # Filter for searching in only 'Inorganic Solid Phases' data collection
    }

    def __init__(self):
        self._soup = None
        self._current_sd = None

    def search_sds(self, chemical_formula):
        self.params['searchTerm'] = chemical_formula
        response = requests.get(self.SM_URL + 'search', params=self.params)
        if response.status_code == 200:
            bs = BeautifulSoup(response.content, 'html.parser')
            return [a.get('href').split('/')[-1] for a in bs.find_all('a', {'class': 'search_result'})]

    def get_properties(self, sd):
        """
        :param sd: Dataset ID in data collection
        :return: dict
        """
        response = requests.get(self.SM_URL + self.ISP_URL + sd)
        if response.status_code == 200:
            bs = BeautifulSoup(response.content, 'html.parser')
            props = bs.find('div', {'id': 'substance-summary'}).find_all('li')
            dens = props[-1].find('span').text.split(' ')[2]
            st_formula = props[0].find('span').text.strip()
            return {
                'formula': st_formula,
                'name': '',
                'density': dens,
                'mol_weight': self._calc_mol_weight(st_formula),
                'id': sd,
                'source': 'Springer Materials'
            }

    @staticmethod
    def _calc_mol_weight(chem_formula):
        parsed_f = parse_formula(chem_formula)
        sum_mol_weight = 0

        for elem in parsed_f.keys():
            sum_mol_weight += ElementsManager(elem).at_weight * parsed_f[elem]

        return sum_mol_weight


if __name__ == '__main__':
    # x = PubChemManager()
    # cids = x.search_cids('Cr2Ti')
    # print(cids)
    # for cid in cids[:2]:
    #     print(x.get_properties(cid))
    #     time.sleep(1)

    x = SpringerMaterialsManager()
    print(x.get_properties('sd_0450079'))