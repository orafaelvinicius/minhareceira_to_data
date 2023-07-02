import json
from pprint import pprint
import requests
import pandas as pd

class CNPJ:
    def __init__(self, cnpj='30231143000175'):
        self.cnpj = cnpj
        self.json_data = {}
        self.data_formated = []
        self.df = pd.DataFrame()

    def make_request(self):
        response = requests.get(f'https://minhareceita.org/{self.cnpj}')
        
        json_data = json.loads(response.text)
        pprint(json_data)
        self.json_data.update(json_data)

    def structure_and_treatment(self):
        print('ESTRUTURANDO DADOS')
        print(self.json_data)
        cnpj =                   self.json_data['cnpj']
        nome_fantasia =          self.json_data['nome_fantasia']
        estado =                 self.json_data['uf']
        cep =                    self.json_data['cep']
        atividade_principal =    self.json_data['cnae_fiscal_descricao']
        socios =                 self.json_data['qsa']
        atividades_secundarias = self.json_data['cnaes_secundarios']

        self.data_formated.append({'cnpj':cnpj})
        self.data_formated.append({'nome_fantasia':nome_fantasia})
        self.data_formated.append({'estado':estado})
        self.data_formated.append({'cep':cep})
        self.data_formated.append({'atividade_principal':atividade_principal})
        
        for item in socios:
            nome_socio = item['nome_socio']
            self.data_formated.append({'socios':nome_socio})

        for atividade in atividades_secundarias:
            atividades_secundarias = atividade['descricao']
            self.data_formated.append({'atividade_secundaria':atividades_secundarias})
        
        # return self.data_formated

    def create_dataframe(self):
        df = pd.DataFrame(self.data_formated)
        print(df)
        return df

    def create_excel(self, filename):
        print('Criando arquivo excel')
        self.df.to_excel(filename, index=False)

    def run(self):
        self.make_request()
        self.structure_and_treatment()
        self.create_dataframe()
        self.create_excel('info_cnpj.xlsx')
        print('__FINISH__')


if __name__ == '__main__':
    req = CNPJ()
    req.run()
