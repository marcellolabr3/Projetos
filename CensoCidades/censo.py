import requests

def get_population(city_codes):
    url = f'https://servicodados.ibge.gov.br/api/v1/populacao/{city_codes}/periodos/2023'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Lista de códigos IBGE dos municípios brasileiros fornecidos pelo link
city_codes = "1100015|1100023|1100031|1100049|1100056|1100064|1100072|1100080|1100098|1100106|1100114|1100122|1100130|1100148|1100155|1100189|1100205|1100254|1100262|1100288|1100296|1100304|1100320|1100338|1100346|1100379|1100403|1100452|1100502|1100601|1100700|1100809|1100908|1100924|1100940|1101005|1101104|1101203|1101302|1101401|1101435|1101450|1101468|1101476|1101484|1101492|1101500|1101559|5221452|5221502|5221551|5221577|5221601|5221700|5221809|5221858|5221908|5222005|5222054|5222203|5222302|5300108"

# Obtendo os dados da população dos municípios
population_data = get_population(city_codes)

# Exibindo os dados obtidos
if population_data:
    for city_data in population_data:
        city_name = city_data['nome']
        city_population = city_data['series'][0]['serie']
        print(f"Cidade: {city_name} | População: {city_population}")
else:
    print("Falha ao obter os dados da API")
