import { useState } from "react";
import { useNavigate } from "react-router-dom";

function CadastroGabarito() {
  const navigate = useNavigate();

  const disciplinasDia1 = [
    { nome: "Língua Portuguesa e Literatura Brasileira", questoes: 12 },
    { nome: "Segunda Língua (Inglês)", questoes: 8, segundaLingua: true },
    { nome: "Segunda Língua (Espanhol)", questoes: 8, segundaLingua: true },
    { nome: "Matemática", questoes: 10 },
    { nome: "Biologia", questoes: 10 },
  ];

  const disciplinasDia2 = [
    { nome: "Física", questoes: 10 },
    { nome: "Química", questoes: 10 },
    { nome: "Ciências Humanas e Sociais", questoes: 20 },
  ];

  const [gabaritos, setGabaritos] = useState([]);
  const [nomeGabarito, setNomeGabarito] = useState("");

  const handleChange = (index, field, value) => {
    const novosGabaritos = [...gabaritos];
    novosGabaritos[index][field] = value;
    setGabaritos(novosGabaritos);
  };

  const gerarQuestoes = () => {
    let lista = [];
    let numeroQuestao = 1;
    let numeroQuestaoSegundaLingua = 13;


    // Dia 1
    disciplinasDia1.forEach((disciplina) => {
      if (disciplina.segundaLingua) {
        for (let i = 1; i <= disciplina.questoes; i++) {
          lista.push({
            dia: 1,
            disciplina: disciplina.nome,
            numeroQuestao: numeroQuestaoSegundaLingua + (i - 1),
            somatorioCorreto: "",
            totalAfirmativas: "",
            tipoQuestao: "Somatório",
          });
        }
      } else {
        for (let i = 1; i <= disciplina.questoes; i++) {
          lista.push({
            dia: 1,
            disciplina: disciplina.nome,
            numeroQuestao: numeroQuestao,
            somatorioCorreto: "",
            totalAfirmativas: "",
            tipoQuestao: "Somatório",
          });
          numeroQuestao++;
        }
      }
    });

    // Dia 2 (reinicia contagem)
numeroQuestao = 1;

// ATENÇÃO: ordem manual para o Dia 2
[
  { nome: "Ciências Humanas e Sociais", questoes: 20 },
  { nome: "Física", questoes: 10 },
  { nome: "Química", questoes: 10 }
].forEach((disciplina) => {
  for (let i = 1; i <= disciplina.questoes; i++) {
    lista.push({
      dia: 2,
      disciplina: disciplina.nome,
      numeroQuestao: numeroQuestao,
      somatorioCorreto: "",
      totalAfirmativas: "",
      tipoQuestao: "Somatório",
    });
    numeroQuestao++;
  }
});


    setGabaritos(lista);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!nomeGabarito.trim()) {
      alert("⚠️ Por favor, preencha o Nome do Gabarito!");
      return;
    }

    const dadosParaSalvar = {
      nomeGabarito,
      questoes: gabaritos,
    };

    console.log("Gabarito enviado:", dadosParaSalvar);
    alert(`✅ Gabarito "${nomeGabarito}" montado! (Veja no console)`);
    navigate("/"); // Redireciona para a lista de gabaritos
  };

  if (gabaritos.length === 0) {
    gerarQuestoes();
  }

  return (
    <div className="bg-green-50 min-h-screen p-6">
      <h1 className="text-3xl font-bold text-green-700 mb-6">Cadastro de Gabarito - Corretor UFSC</h1>
<button
  type="button"
  onClick={() => navigate("/")}
  className="mb-6 bg-green-300 hover:bg-green-400 text-green-900 font-bold py-2 px-4 rounded-lg"
>
  ← Voltar
</button>

      <form onSubmit={handleSubmit}>
        <div className="mb-8">
          <label className="block text-green-700 font-semibold mb-2 text-xl">
            Nome do Gabarito:
          </label>
          <input
            type="text"
            value={nomeGabarito}
            onChange={(e) => setNomeGabarito(e.target.value)}
            placeholder="Exemplo: Simulado UFSC Inverno"
            className="w-full max-w-md border border-green-300 rounded p-2 shadow-sm"
            required
          />
        </div>

        {[1, 2].map((dia) => (
          <div key={dia} className="mb-10">
            <h2 className="text-2xl font-semibold text-green-700 mb-4">
              Dia {dia}
            </h2>

            <div className="overflow-x-auto shadow rounded-lg">
              <table className="min-w-full bg-white rounded-lg">
                <thead className="bg-green-600 text-white">
                  <tr>
                    <th className="py-2 px-4 text-left">Disciplina</th>
                    <th className="py-2 px-4 text-left">Questão</th>
                    <th className="py-2 px-4 text-left">Somatório Correto</th>
                    <th className="py-2 px-4 text-left">Total de Afirmativas</th>
                    <th className="py-2 px-4 text-left">Tipo de Questão</th>
                  </tr>
                </thead>
                <tbody>
                  {gabaritos
                    .filter((q) => q.dia === dia)
                    .map((q, index) => (
                      <tr key={index} className="hover:bg-green-100">
                        <td className="border px-4 py-2">{q.disciplina}</td>
                        <td className="border px-4 py-2">{q.numeroQuestao}</td>
                        <td className="border px-4 py-2">
                          <input
                            type="text"
                            inputMode="numeric"
                            pattern="[0-9]*"
                            value={q.somatorioCorreto}
                            onChange={(e) => {
                              const valor = e.target.value;
                              if (/^\d*$/.test(valor)) {  // Permite apenas números
                                handleChange(index, "somatorioCorreto", valor);
                              }
                            }}
                          />
                        </td>
                        <td className="border px-4 py-2">
                          <input
                            type="number"
                            min="0"
                            max="7"
                            value={q.totalAfirmativas !== "" ? Number(q.totalAfirmativas) : ""}
                            onChange={(e) => handleChange(index, "totalAfirmativas", e.target.value)}
                            className="w-20 p-1 border border-green-300 rounded"
                            required
                          />
                        </td>
                        <td className="border px-4 py-2">
                          <select
                            value={q.tipoQuestao}
                            onChange={(e) => handleChange(index, "tipoQuestao", e.target.value)}
                            className="p-1 border border-green-300 rounded"
                          >
                            <option value="Somatório">Somatório</option>
                            <option value="Aberta">Aberta</option>
                          </select>
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}

        <button
          type="submit"
          className="mt-6 bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-lg"
        >
          Salvar Gabarito
        </button>
      </form>
    </div>
  );
}

export default CadastroGabarito;
