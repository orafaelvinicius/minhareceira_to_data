import json
import requests
import pandas as pd
import numpy as np

# Faça a requisição dos dados
def Request(cnpj):
    response = requests.get(f'https://minhareceita.org/{cnpj}')
    
    json_data = json.loads(response.text)

    return json_data

def structure_and_treatment(json_data):
    data_formated = []

    cnpj =                   json_data['cnpj']
    nome_fantasia =          json_data['nome_fantasia']
    estado =                 json_data['uf']
    cep =                    json_data['cep']
    atividade_principal =    json_data['cnae_fiscal_descricao']
    socios =                 json_data['qsa']
    atividades_secundarias = json_data['cnaes_secundarios']
    
    data_formated.append({'cnpj':cnpj})
    data_formated.append({'nome_fantasia':nome_fantasia})
    data_formated.append({'estado':estado})
    data_formated.append({'cep':cep})
    data_formated.append({'atividade_principal':atividade_principal})
    
    for item in socios:
        nome_socio = item['nome_socio']
        data_formated.append({'socios':nome_socio})

    for atividade in atividades_secundarias:
        atividades_secundarias = atividade['descricao']
        data_formated.append({'atividade_secundaria':atividades_secundarias})
    
    return data_formated

def create_dataframe(data):
    print('CRIANDO O DATAFRAME')
    # data_json = pd.read_json(data)

    df = pd.DataFrame(data)

    return df

def create_excel(df, filename):
    df.to_excel(filename, index=False)


cnpj = '30231143000175'

print('Fazendo a requisição na api')
json_data = Request(cnpj)

print('Estruturando e tratando dados')
data = structure_and_treatment(json_data)

print('Criando tabela')
df = create_dataframe(data)

print('Criando planilha no excel')
create_excel(df, 'info_cnpj.xlsx')
