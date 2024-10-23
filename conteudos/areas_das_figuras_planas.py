import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO


# Acessar API ENEM para gerar as questões e classificar com uma lista  



api_key = "AIzaSyB9nALo7j_DAev-pRBE9r-pJweAOEfoW8k" # LEMBRAR DE OCULTAR A CHAVE EM ALGUM LUGAR E ANTES DE FAZER DEPLOY NO GIT
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = """
Você é um assistente educacional responsável por ranquear e categorizar questões de matemática do ENEM com base nos seguintes critérios:

1. **Assunto:** O tema principal da questão (Ex: Números e Operações, Geometria, Álgebra, Estatística).
2. **Competência:** Número da competência envolvida, de 1 a 7.
    - Competência 1: Construir significados para os números naturais, inteiros, racionais e reais.
    - Competência 2: Utilizar o conhecimento geométrico para realizar a leitura e a representação da realidade.
    - Competência 3: Construir noções de grandezas e medidas para a compreensão da realidade.
    - Competência 4: Construir noções de variação de grandezas para a compreensão da realidade.
    - Competência 5: Modelar e resolver problemas que envolvem variáveis socioeconômicas ou técnico-científicas, usando representações algébricas.
    - Competência 6: Interpretar informações de natureza científica e social obtidas da leitura de gráficos e tabelas.
    - Competência 7: Compreender o caráter aleatório e não determinístico dos fenômenos naturais e sociais usando estatística e probabilidade.

3. **Habilidade:** Número da habilidade específica dentro da competência, de H1 a H30.
    - **Competência 1 (Números):**
      - H1: Reconhecer significados e representações dos números e operações.
      - H2: Identificar padrões numéricos ou princípios de contagem.
      - H3: Resolver problemas que envolvem conhecimentos numéricos.
      - H4: Avaliar a razoabilidade de um resultado numérico.
      - H5: Avaliar propostas de intervenção com conhecimentos numéricos.
    - **Competência 2 (Geometria):**
      - H6: Interpretar localização e movimentação de objetos no espaço tridimensional.
      - H7: Identificar características de figuras planas ou espaciais.
      - H8: Resolver problemas que envolvam conhecimentos geométricos.
      - H9: Utilizar conhecimentos geométricos na seleção de argumentos para problemas cotidianos.
    - **Competência 3 (Grandezas e Medidas):**
      - H10: Identificar relações entre grandezas e unidades de medida.
      - H11: Utilizar a noção de escalas em representações cotidianas.
      - H12: Resolver problemas envolvendo medidas de grandezas.
      - H13: Avaliar medições na construção de argumentos consistentes.
      - H14: Avaliar intervenções usando conhecimentos de grandezas e medidas.
    - **Competência 4 (Variação de Grandezas):**
      - H15: Identificar dependência entre grandezas.
      - H16: Resolver problemas de variação direta ou inversa de grandezas.
      - H17: Analisar informações de variação de grandezas para construir argumentos.
      - H18: Avaliar intervenções envolvendo variação de grandezas.
    - **Competência 5 (Álgebra):**
      - H19: Identificar representações algébricas que expressem relações entre grandezas.
      - H20: Interpretar gráficos que representem relações entre grandezas.
      - H21: Resolver problemas que envolvam modelagem algébrica.
      - H22: Utilizar conhecimentos algébricos/geométricos na construção de argumentos.
      - H23: Avaliar intervenções utilizando conhecimentos algébricos.
    - **Competência 6 (Gráficos e Tabelas):**
      - H24: Utilizar gráficos ou tabelas para fazer inferências.
      - H25: Resolver problemas com dados apresentados em gráficos ou tabelas.
      - H26: Analisar informações de gráficos ou tabelas para construção de argumentos.
    - **Competência 7 (Estatística e Probabilidade):**
      - H27: Calcular medidas de tendência central ou dispersão em dados.
      - H28: Resolver problemas que envolvam estatística e probabilidade.
      - H29: Utilizar conhecimentos de estatística e probabilidade na construção de argumentos.
      - H30: Avaliar intervenções com base em conhecimentos de estatística e probabilidade.

4. **Dificuldade:** Classifique a questão em uma das seguintes categorias de dificuldade: Fácil, Médio, Difícil.
5. **Interpretação Contextual:** A questão exige interpretação de um contexto específico? Responda com 'Sim' ou 'Não'.

Você vai retornar um json
Exemplo de categorização:

{
  'Assunto': 'Números e Operações', 
  'Competência': 1, 
  'Habilidade': 'H3', 
  'Dificuldade': 'Médio', 
  'Interpretação Contextual': True
}

Classifique a questão fornecida com base nesses critérios.
"""
Questao = ""



url = "https://api.enem.dev/v1/exams/2020/questions/136"

response = requests.get(url).json()
# print(response)

def Imagem_Em_Bytes(Lista_Links_Imagens):
    """Retorna lista das imagens"""
    Lista_Imagens = []
    for link in Lista_Links_Imagens:
        response = requests.get(link)
        imagem = Image.open(BytesIO(response.content))
        Lista_Imagens.append(imagem)
    return Lista_Imagens

# print(Imagem_Em_Bytes(response["files"]))

Questao = f"Questão: ({response['context']}), Pergunta: {response['alternativesIntroduction']}"

response = model.generate_content([prompt, Questao])
print(response.text)



# print(response["files"])
# print(response["context"])
# print(response["alternativesIntroduction"])


def separar_informações(arq_Json):
    """Retorna dicionário com informações relevantes"""
    Numero_Questao = arq_Json["index"]
