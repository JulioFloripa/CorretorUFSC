import pandas as pd
import os

def decompor_somatorio(valor):
    afirmativas = {
        1: '01',
        2: '02',
        4: '04',
        8: '08',
        16: '16',
        32: '32',
        64: '64'
    }
    corretas = []
    for num in sorted(afirmativas.keys(), reverse=True):
        if valor >= num:
            corretas.append(afirmativas[num])
            valor -= num
    return corretas

def calcular_pontuacao(NP, NTPC, NPC, NPI):
    if NPC > NPI:
        P = (NP - (NTPC - (NPC - NPI))) / NP
    else:
        P = 0
    return round(P, 2)

def corrigir_simulado(arquivo_dia1, arquivo_dia2, gabarito_dia1, gabarito_dia2):
    # Lê os arquivos de respostas enviados
    respostas_dia1 = pd.read_excel(arquivo_dia1)
    respostas_dia2 = pd.read_excel(arquivo_dia2)

    # --- Separar os gabaritos do Dia 1
    gabarito_comum_dia1 = gabarito_dia1[gabarito_dia1['Disciplina'] == 'Comum']
    gabarito_ingles = gabarito_dia1[gabarito_dia1['Disciplina'] == 'Inglês']
    gabarito_espanhol = gabarito_dia1[gabarito_dia1['Disciplina'] == 'Espanhol']

    # --- Encontrar coluna da língua estrangeira
    coluna_lingua = next((col for col in respostas_dia1.columns if 'língua' in col.lower()), None)
    if coluna_lingua is None:
        raise ValueError("⚠️ Coluna de língua estrangeira não encontrada no Dia 1.")

    # --- Criar pasta de relatórios se ainda não existir
    if not os.path.exists('relatorios_individuais'):
        os.makedirs('relatorios_individuais')

    todos_emails = set(respostas_dia1['Email'].unique()).union(respostas_dia2['Email'].unique())
    resultado_final_com_disciplinas = []

    for email in todos_emails:
        aluno_dia1 = respostas_dia1[respostas_dia1['Email'] == email]
        aluno_dia2 = respostas_dia2[respostas_dia2['Email'] == email]

        nome = aluno_dia1['Name'].values[0] if not aluno_dia1.empty else aluno_dia2['Name'].values[0]
        lingua = aluno_dia1[coluna_lingua].values[0].strip().lower() if not aluno_dia1.empty else 'não informado'

        nota_portugues = 0
        nota_lingua = 0
        nota_matematica = 0
        nota_biologia = 0
        nota_humanas = 0
        nota_fisica = 0
        nota_quimica = 0

        # --- Corrigir Dia 1
        if not aluno_dia1.empty:
            aluno_dia1 = aluno_dia1.iloc[0]

            for _, questao in gabarito_comum_dia1.iterrows():
                numero_questao = int(questao['Questão'])
                questao_nome = f"Questões {numero_questao}"
                resposta_raw = aluno_dia1.get(questao_nome, 'Ausente')

                pontuacao = calcular_pontuacao_questao(resposta_raw, questao)

                if 1 <= numero_questao <= 12:
                    nota_portugues += pontuacao
                elif 13 <= numero_questao <= 20:
                    nota_lingua += pontuacao
                elif 21 <= numero_questao <= 30:
                    nota_matematica += pontuacao
                elif 31 <= numero_questao <= 40:
                    nota_biologia += pontuacao

            # Corrigir Língua Estrangeira
            gabarito_lingua = gabarito_ingles if lingua == 'inglês' else gabarito_espanhol if lingua == 'espanhol' else pd.DataFrame()
            for _, questao in gabarito_lingua.iterrows():
                numero_questao = int(questao['Questão'])
                questao_nome = f"Questões {numero_questao}"
                resposta_raw = aluno_dia1.get(questao_nome, 'Ausente')

                pontuacao = calcular_pontuacao_questao(resposta_raw, questao)
                nota_lingua += pontuacao

        # --- Corrigir Dia 2
        if not aluno_dia2.empty:
            aluno_dia2 = aluno_dia2.iloc[0]

            for _, questao in gabarito_dia2.iterrows():
                numero_questao = int(questao['Questão'])
                questao_nome = f"Questões {numero_questao}"
                resposta_raw = aluno_dia2.get(questao_nome, 'Ausente')

                pontuacao = calcular_pontuacao_questao(resposta_raw, questao)

                if 1 <= numero_questao <= 20:
                    nota_humanas += pontuacao
                elif 21 <= numero_questao <= 30:
                    nota_fisica += pontuacao
                elif 31 <= numero_questao <= 40:
                    nota_quimica += pontuacao

        # Resultado do aluno
        resultado_final_com_disciplinas.append({
            'Email': email,
            'Nome': nome,
            'Português/Lit': round(nota_portugues, 2),
            'Segunda Língua': round(nota_lingua, 2),
            'Matemática': round(nota_matematica, 2),
            'Biologia': round(nota_biologia, 2),
            'Ciências Humanas': round(nota_humanas, 2),
            'Física': round(nota_fisica, 2),
            'Química': round(nota_quimica, 2),
            'Nota Final': round(nota_portugues + nota_lingua + nota_matematica + nota_biologia + nota_humanas + nota_fisica + nota_quimica, 2)
        })

    # --- Gerar o relatório final em Excel ---
    resultado_final_df = pd.DataFrame(resultado_final_com_disciplinas)
    resultado_final_df.to_excel('resultado_final.xlsx', index=False)

    return resultado_final_com_disciplinas

def calcular_pontuacao_questao(resposta_raw, questao):
    if pd.isna(resposta_raw) or resposta_raw == 'Ausente':
        return 0
    try:
        resposta_num = int(resposta_raw)
        if resposta_num > 99:
            resposta_num = 99
        resposta_aluno = decompor_somatorio(resposta_num)
        corretas = decompor_somatorio(int(questao['Somatório Correto']))
        NP = int(questao['Total de Afirmativas'])
        NTPC = len(corretas)
        NPC = len([alt for alt in resposta_aluno if alt in corretas])
        NPI = len([alt for alt in resposta_aluno if alt not in corretas])
        return calcular_pontuacao(NP, NTPC, NPC, NPI)
    except:
        return 0
