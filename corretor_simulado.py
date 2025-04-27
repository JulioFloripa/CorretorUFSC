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

# --- Ler os arquivos de respostas
respostas_dia1 = pd.read_excel('respostas_dia1.xlsx')
respostas_dia2 = pd.read_excel('respostas_dia2.xlsx')

# --- Ler os gabaritos
gabarito_dia1 = pd.read_excel('gabarito_dia1.xlsx')
gabarito_dia2 = pd.read_excel('gabarito_dia2.xlsx')

# --- Separar os gabaritos
gabarito_comum_dia1 = gabarito_dia1[gabarito_dia1['Disciplina'] == 'Comum']
gabarito_ingles = gabarito_dia1[gabarito_dia1['Disciplina'] == 'Inglês']
gabarito_espanhol = gabarito_dia1[gabarito_dia1['Disciplina'] == 'Espanhol']

# --- Corrigir as provas
resultado_final = []

# Encontrar automaticamente a coluna da língua estrangeira
coluna_lingua = next((col for col in respostas_dia1.columns if 'língua' in col.lower()), None)
if coluna_lingua is None:
    raise ValueError("⚠️ Coluna de língua estrangeira não encontrada no arquivo de respostas do Dia 1.")

print("\nCorrigindo provas...")

# Criar pasta de relatórios se ainda não existir
if not os.path.exists('relatorios_individuais'):
    os.makedirs('relatorios_individuais')

# Pegar todos os emails únicos de Dia 1 e Dia 2
emails_dia1 = set(respostas_dia1['Email'].unique())
emails_dia2 = set(respostas_dia2['Email'].unique())
todos_emails = emails_dia1.union(emails_dia2)

for email in todos_emails:
    aluno_dia1 = respostas_dia1[respostas_dia1['Email'] == email]
    aluno_dia2 = respostas_dia2[respostas_dia2['Email'] == email]
    
    nome = aluno_dia1['Name'].values[0] if not aluno_dia1.empty else aluno_dia2['Name'].values[0]
    lingua = aluno_dia1[coluna_lingua].values[0].strip().lower() if not aluno_dia1.empty else 'não informado'
    
    nota_dia1 = 0
    nota_dia2 = 0

    relatorio_dia1 = []
    relatorio_dia2 = []

    # --- Corrigir Dia 1
    if not aluno_dia1.empty:
        aluno_dia1 = aluno_dia1.iloc[0]

        for _, questao in gabarito_comum_dia1.iterrows():
            questao_nome = f"Questões {int(questao['Questão'])}"
            if questao_nome in aluno_dia1:
                resposta_raw = aluno_dia1[questao_nome]
                if pd.isna(resposta_raw):
                    resposta_tratada = 'Ausente'
                else:
                    try:
                        resposta_num = int(resposta_raw)
                        if resposta_num > 99:
                            resposta_num = 99
                        resposta_tratada = resposta_num
                    except:
                        resposta_tratada = 'Ausente'
            else:
                resposta_tratada = 'Ausente'

            gabarito_correto = questao['Somatório Correto']
            if resposta_tratada == 'Ausente':
                pontuacao = 0
            else:
                resposta_aluno = decompor_somatorio(resposta_tratada)
                corretas = decompor_somatorio(int(gabarito_correto))
                NP = int(questao['Total de Afirmativas'])
                NTPC = len(corretas)
                NPC = len([alt for alt in resposta_aluno if alt in corretas])
                NPI = len([alt for alt in resposta_aluno if alt not in corretas])
                pontuacao = calcular_pontuacao(NP, NTPC, NPC, NPI)

            relatorio_dia1.append({
                'Questão': int(questao['Questão']),
                'Resposta Aluno': resposta_tratada,
                'Resposta Correta': gabarito_correto,
                'Pontuação': pontuacao
            })
            nota_dia1 += pontuacao

        # Corrigir Língua Estrangeira
        if lingua == 'inglês':
            gabarito_lingua = gabarito_ingles
        elif lingua == 'espanhol':
            gabarito_lingua = gabarito_espanhol
        else:
            gabarito_lingua = pd.DataFrame()

        for _, questao in gabarito_lingua.iterrows():
            questao_nome = f"Questões {int(questao['Questão'])}"
            if questao_nome in aluno_dia1:
                resposta_raw = aluno_dia1[questao_nome]
                if pd.isna(resposta_raw):
                    resposta_tratada = 'Ausente'
                else:
                    try:
                        resposta_num = int(resposta_raw)
                        if resposta_num > 99:
                            resposta_num = 99
                        resposta_tratada = resposta_num
                    except:
                        resposta_tratada = 'Ausente'
            else:
                resposta_tratada = 'Ausente'

            gabarito_correto = questao['Somatório Correto']
            if resposta_tratada == 'Ausente':
                pontuacao = 0
            else:
                resposta_aluno = decompor_somatorio(resposta_tratada)
                corretas = decompor_somatorio(int(gabarito_correto))
                NP = int(questao['Total de Afirmativas'])
                NTPC = len(corretas)
                NPC = len([alt for alt in resposta_aluno if alt in corretas])
                NPI = len([alt for alt in resposta_aluno if alt not in corretas])
                pontuacao = calcular_pontuacao(NP, NTPC, NPC, NPI)

            relatorio_dia1.append({
                'Questão': int(questao['Questão']),
                'Resposta Aluno': resposta_tratada,
                'Resposta Correta': gabarito_correto,
                'Pontuação': pontuacao
            })
            nota_dia1 += pontuacao

    # --- Corrigir Dia 2
    if not aluno_dia2.empty:
        aluno_dia2 = aluno_dia2.iloc[0]

        for _, questao in gabarito_dia2.iterrows():
            questao_nome = f"Questões {int(questao['Questão'])}"
            if questao_nome in aluno_dia2:
                resposta_raw = aluno_dia2[questao_nome]
                if pd.isna(resposta_raw):
                    resposta_tratada = 'Ausente'
                else:
                    try:
                        resposta_num = int(resposta_raw)
                        if resposta_num > 99:
                            resposta_num = 99
                        resposta_tratada = resposta_num
                    except:
                        resposta_tratada = 'Ausente'
            else:
                resposta_tratada = 'Ausente'

            gabarito_correto = questao['Somatório Correto']
            if resposta_tratada == 'Ausente':
                pontuacao = 0
            else:
                resposta_aluno = decompor_somatorio(resposta_tratada)
                corretas = decompor_somatorio(int(gabarito_correto))
                NP = int(questao['Total de Afirmativas'])
                NTPC = len(corretas)
                NPC = len([alt for alt in resposta_aluno if alt in corretas])
                NPI = len([alt for alt in resposta_aluno if alt not in corretas])
                pontuacao = calcular_pontuacao(NP, NTPC, NPC, NPI)

            relatorio_dia2.append({
                'Questão': int(questao['Questão']),
                'Resposta Aluno': resposta_tratada,
                'Resposta Correta': gabarito_correto,
                'Pontuação': pontuacao
            })
            nota_dia2 += pontuacao

    # --- Gerar boletim individual ---
    relatorio_dia1_df = pd.DataFrame(relatorio_dia1)
    relatorio_dia2_df = pd.DataFrame(relatorio_dia2)

    info_aluno = pd.DataFrame({
        'Informação': ['Nome', 'Email', 'Língua Estrangeira'],
        'Valor': [nome, email, lingua]
    })

    with pd.ExcelWriter(f'relatorios_individuais/{email}.xlsx') as writer:
        info_aluno.to_excel(writer, index=False, sheet_name='Dados do Aluno')
        
        colunas_salvar_dia1 = [col for col in ['Questão', 'Resposta Aluno', 'Resposta Correta', 'Pontuação'] if col in relatorio_dia1_df.columns]
        relatorio_dia1_df[colunas_salvar_dia1].to_excel(writer, index=False, sheet_name='Respostas Dia 1')
        
        colunas_salvar_dia2 = [col for col in ['Questão', 'Resposta Aluno', 'Resposta Correta', 'Pontuação'] if col in relatorio_dia2_df.columns]
        relatorio_dia2_df[colunas_salvar_dia2].to_excel(writer, index=False, sheet_name='Respostas Dia 2')


    # Salvar resultado geral
    resultado_final.append({
        'Email': email,
        'Name': nome,
        'Nota Dia 1': round(nota_dia1, 2),
        'Nota Dia 2': round(nota_dia2, 2),
        'Nota Final': round(nota_dia1 + nota_dia2, 2)
    })
# --- Calcular Notas por Disciplina no resultado final ---

# --- Calcular Notas por Disciplina com pontuação correta ---

resultado_final_com_disciplinas = []

for email in todos_emails:
    aluno_dia1 = respostas_dia1[respostas_dia1['Email'] == email]
    aluno_dia2 = respostas_dia2[respostas_dia2['Email'] == email]
    
    nome = aluno_dia1['Name'].values[0] if not aluno_dia1.empty else aluno_dia2['Name'].values[0]

    # Inicializar notas
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

            if pd.isna(resposta_raw) or resposta_raw == 'Ausente':
                resposta_tratada = 'Ausente'
                pontuacao = 0
            else:
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
                    pontuacao = calcular_pontuacao(NP, NTPC, NPC, NPI)
                except:
                    pontuacao = 0

            if 1 <= numero_questao <= 12:
                nota_portugues += pontuacao
            elif 13 <= numero_questao <= 20:
                nota_lingua += pontuacao
            elif 21 <= numero_questao <= 30:
                nota_matematica += pontuacao
            elif 31 <= numero_questao <= 40:
                nota_biologia += pontuacao

        # Corrigir língua estrangeira
        if lingua == 'inglês':
            gabarito_lingua = gabarito_ingles
        elif lingua == 'espanhol':
            gabarito_lingua = gabarito_espanhol
        else:
            gabarito_lingua = pd.DataFrame()

        for _, questao in gabarito_lingua.iterrows():
            numero_questao = int(questao['Questão'])
            questao_nome = f"Questões {numero_questao}"
            resposta_raw = aluno_dia1.get(questao_nome, 'Ausente')

            if pd.isna(resposta_raw) or resposta_raw == 'Ausente':
                resposta_tratada = 'Ausente'
                pontuacao = 0
            else:
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
                    pontuacao = calcular_pontuacao(NP, NTPC, NPC, NPI)
                except:
                    pontuacao = 0

            nota_lingua += pontuacao

    # --- Corrigir Dia 2
    if not aluno_dia2.empty:
        aluno_dia2 = aluno_dia2.iloc[0]

        for _, questao in gabarito_dia2.iterrows():
            numero_questao = int(questao['Questão'])
            questao_nome = f"Questões {numero_questao}"
            resposta_raw = aluno_dia2.get(questao_nome, 'Ausente')

            if pd.isna(resposta_raw) or resposta_raw == 'Ausente':
                resposta_tratada = 'Ausente'
                pontuacao = 0
            else:
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
                    pontuacao = calcular_pontuacao(NP, NTPC, NPC, NPI)
                except:
                    pontuacao = 0

            if 1 <= numero_questao <= 20:
                nota_humanas += pontuacao
            elif 21 <= numero_questao <= 30:
                nota_fisica += pontuacao
            elif 31 <= numero_questao <= 40:
                nota_quimica += pontuacao

    resultado_final_com_disciplinas.append({
        'Email': email,
        'Name': nome,
        'Português/Lit': round(nota_portugues, 2),
        'Segunda Língua': round(nota_lingua, 2),
        'Matemática': round(nota_matematica, 2),
        'Biologia': round(nota_biologia, 2),
        'Ciências Humanas': round(nota_humanas, 2),
        'Física': round(nota_fisica, 2),
        'Química': round(nota_quimica, 2),
        'Nota Final': round(nota_portugues + nota_lingua + nota_matematica + nota_biologia + nota_humanas + nota_fisica + nota_quimica, 2)
    })

# --- Salvar o novo resultado final atualizado
resultado_final_df = pd.DataFrame(resultado_final_com_disciplinas)
resultado_final_df.to_excel('resultado_final.xlsx', index=False)

print("\n✅ Novo relatório com pontuação REAL por disciplinas gerado com sucesso!")


# --- Salvar o novo resultado final atualizado
resultado_final_df = pd.DataFrame(resultado_final_com_disciplinas)
resultado_final_df.to_excel('resultado_final.xlsx', index=False)

print("\n✅ Arquivo 'resultado_final.xlsx' e boletins individuais gerados com sucesso!")

