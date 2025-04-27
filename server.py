from flask import Flask, request, jsonify
import pandas as pd
from corretor_simulado import corrigir_simulado

app = Flask(__name__)

@app.route('/corrigir', methods=['POST'])
def corrigir():
    try:
        # Pega os arquivos e o ID enviados pelo frontend
        arquivo_dia1 = request.files['arquivoDia1']
        arquivo_dia2 = request.files['arquivoDia2']
        gabarito_id = request.form['gabaritoId']

        # Carregar os gabaritos correspondentes
        # (por enquanto fixo, futuramente podemos usar o ID para buscar o certo)
        gabarito_dia1 = pd.read_excel('backend/gabarito_dia1.xlsx')
        gabarito_dia2 = pd.read_excel('backend/gabarito_dia2.xlsx')

        # Chamar a função de correção
        resultados = corrigir_simulado(arquivo_dia1, arquivo_dia2, gabarito_dia1, gabarito_dia2)

        # Devolver o resumo corrigido como resposta
        return jsonify(resultados)

    except Exception as e:
        print(f"Erro ao corrigir: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
