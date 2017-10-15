import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

arquivo = 'imd_notas.xlsx'
excel = pd.ExcelFile(arquivo)
dados = excel.parse(0)

blue = (0 / 255, 105 / 255, 164 / 255)
orange = (200 / 255, 82 / 255, 0 / 255)

disciplinas = dados['disciplina_ID'].unique()

dados_disciplinas = []
media = []
# Foram encontrados casos em que o aluno tem
# uma aprovacao antes de reprovacao ou
# tem mais de uma aprovacao na disciplina.
# Para o segundo caso, elimino a repeticao,
# para o primeiro, ainda sem solucao.
for i in disciplinas:
    dados_disciplinas.append(dados[dados['disciplina_ID'] == i])
    id_aprovados = pd.Series(
        dados_disciplinas[i]['a_ID'][
            dados_disciplinas[i]['status.disciplina'] == 'Aprovado'].unique())
    reprovacoes = dados_disciplinas[i]['a_ID'][
        dados_disciplinas[i]['a_ID'].isin(id_aprovados)][
        dados_disciplinas[i]['status.disciplina'] == 'Reprovado']
    media.append(reprovacoes.append(id_aprovados).value_counts().mean())

print(media)

print(np.mean(media))




cep_alunos_aprovados = dados['CEP'][dados['status.disciplina'] == 'Aprovado']
labels = ['0',
          'Av. Abel Cabral - Parnamirim',
          'Av. Maria Lacerda Montenegro - Parnamirim',
          'Macaíba - RN',
          'São Gonçalo do Amarante - RN',
          'Ouro Branco - RN',
          'João Câmara - RN',
          'Ceará-Mirim - RN',
          'Açu - RN',
          'Apodi - RN']

ax = sns.countplot(cep_alunos_aprovados,
                   color=blue,
                   order=cep_alunos_aprovados.value_counts()[:10].index)
ax.set_xticklabels(labels, rotation=90)

plt.title('Regiões com maiores indíces de aprovação')

plt.show()




for i, disciplina in zip(disciplinas, dados_disciplinas):
    sns.boxplot(data=disciplina,
                x='ano_disciplina',
                y='nota',
                hue='periodo_disciplina')
    plt.title('Estatística de notas da disciplina ' + str(i) + ' por período')
    plt.show()

    sns.boxplot(data=disciplina, x='ano_disciplina', y='nota')
    plt.title('Estatística de notas da disciplina ' + str(i) + ' por ano')
    plt.show()




sns.boxplot(data=dados, x='disciplina_ID', y='nota', orient='v')
plt.title('Estatística de notas por disciplina')
plt.show()




for i in range(disciplinas.size-1):
    d1 = dados_disciplinas[i]
    for j in range(i+1, disciplinas.size):
        d2 = dados_disciplinas[j]
        d1 = d1[
            d1['a_ID'].isin(d2['a_ID'])].drop_duplicates(
            'a_ID', keep='last').sort_values(by='a_ID')
        d2 = d2[
            d2['a_ID'].isin(d1['a_ID'])].drop_duplicates(
            'a_ID', keep='last').sort_values(by='a_ID')
        df = pd.DataFrame({
            str(i): d1['nota'].values, str(j): d2['nota'].values})

        ax = sns.regplot(data=df, x=str(i), y=str(j), fit_reg=False)
        plt.title('Relação entre as notas das  disciplinas '
                  + str(i) + ' e ' + str(j))
        plt.show()




alunos_enem = dados.drop_duplicates('a_ID').dropna()
status_grupo1 = alunos_enem['enen-nota'][alunos_enem['status'].isin([
    'ATIVO', 'CONCLUIDO', 'FORMANDO', 'FORMADO'])]
status_grupo2 = alunos_enem['enen-nota'][alunos_enem['status'].isin([
    'CANCELADO', 'TRANCADO'])]
sns.distplot(
    status_grupo1,
    kde=False,
    color=blue,
    hist_kws={'alpha': 1},
    label='Ativos/Formados')
sns.distplot(
    status_grupo2,
    kde=False,
    color=orange,
    hist_kws={'alpha': 0.7},
    label='Cancelados/Trancados',
    axlabel='Nota do ENEM')
plt.legend()
plt.show()




alunos_enem = dados.dropna()
for i in disciplinas:
    disciplina = alunos_enem[
        alunos_enem['disciplina_ID'] == i].drop_duplicates('a_ID', keep='last')
    ax = sns.regplot(x='nota', y='enen-nota', data=disciplina, fit_reg=False)
    plt.title('Relação entre notas do ENEM e notas dos alunos para '
              + 'a disciplina ' + str(i))
    plt.show()


# Existe uma relacao entre o numero medio de
# disciplinas cursadas por aluno
# e o seu desempenho?
media_alunos = pd.DataFrame()
anos = np.sort(dados['ano_disciplina'].unique())
for i in anos:
    periodos = np.sort(dados['periodo_disciplina'][
        dados['ano_disciplina'] == i].unique())
    for j in periodos:
        df = dados[['a_ID', 'status.disciplina']][
            (dados['ano_disciplina'] == i)
            & (dados['periodo_disciplina'] == j)]
        print(df.size)
