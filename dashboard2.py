import pandas as pd
import streamlit as st
import plotly.express as px

# Leia o arquivo CSV
df = pd.read_csv('ACOs_selecionadas_parte5.csv', sep="|")
df['Data de julgamento'] = pd.to_datetime(df['Data de julgamento'])

# Criar a coluna 'Ano' na base de dados original
df['Ano'] = df['Data de julgamento'].dt.year

# Iniciando o dashboard
st.set_page_config(page_title='Análise das ACOs - STF', layout='wide')

st.title('Análise das Ações Originárias no STF sobre Dívidas entre União e Estados')
st.write('Este dashboard apresenta uma análise das Ações Civis Originárias (ACO) relacionadas a dívidas entre a União e os Estados brasileiros no período 2013-2023.')

# Listas para os filtros
estados = df['Parte Ativa'].unique()
relatores = df['Relator'].unique()
anos = sorted(df['Ano'].unique())

# Barra lateral para filtros
st.sidebar.header('Filtros')

# Filtro por Estado
estado_selecionado = st.sidebar.multiselect('Selecione o(s) Estado(s):', estados, default=estados)

# Filtro por Relator
relator_selecionado = st.sidebar.multiselect('Selecione o(s) Relator(es):', relatores, default=relatores)

# Filtro por Ano
ano_selecionado = st.sidebar.multiselect('Selecione o(s) Ano(s):', anos, default=anos)

# Filtro por Vencedor
vencedor_selecionado = st.sidebar.multiselect('Selecione o(s) Vencedor(es):', ['ESTADO', 'UNIÃO'], default=['ESTADO', 'UNIÃO'])

# Aplicar filtros
df_filtered = df[
    (df['Parte Ativa'].isin(estado_selecionado)) &
    (df['Relator'].isin(relator_selecionado)) &
    (df['Ano'].isin(ano_selecionado)) &
    (df['Vencedor'].isin(vencedor_selecionado))
]

# Seção 1: Estados que mais litigam contra a União
# Contagem de ações por Estado
acoes_por_estado = df_filtered['Parte Ativa'].value_counts().reset_index()
acoes_por_estado.columns = ['Estado', 'Número de Ações']

# Ordenar o DataFrame em ordem crescente de 'Número de Ações'
acoes_por_estado = acoes_por_estado.sort_values('Número de Ações', ascending=True)

# Gráfico de barras horizontal
fig1 = px.bar(acoes_por_estado, y='Estado', x='Número de Ações', orientation='h', title='Estados que mais litigam contra a União')

# Atualizar a ordem das categorias para refletir a ordem decrescente
fig1.update_layout(yaxis={'categoryorder':'total ascending'})

# Exibir o gráfico
st.plotly_chart(fig1, use_container_width=True)

# Destaques ou Insights Dinâmicos:
# Verifica se o DataFrame não está vazio
if not acoes_por_estado.empty:
    # Estado com mais ações (última linha devido à ordenação)
    estado_top = acoes_por_estado.iloc[-1]['Estado']
    num_acoes_top = acoes_por_estado.iloc[-1]['Número de Ações']

    st.markdown(f"**Insight:** Atualmente, o **{estado_top}** lidera com **{num_acoes_top}** ações contra a União no contexto selecionado.")
else:
    st.markdown("**Insight:** Não há dados para o contexto selecionado.")

# Seção 2: Proporção de decisões favoráveis aos Estados e à União
# Contagem de decisões por Vencedor
decisoes_vencedor = df_filtered['Vencedor'].value_counts().reset_index()
decisoes_vencedor.columns = ['Vencedor', 'Número de Decisões']

# Gráfico de pizza
fig2 = px.pie(decisoes_vencedor, values='Número de Decisões', names='Vencedor', title='Proporção de decisões favoráveis')

# Exibir o gráfico
st.plotly_chart(fig2, use_container_width=True)

# Gráfico de Barras Horizontal com Proporção por Estado:
# Calcula a proporção de vitórias por Estado
vit_por_estado = df_filtered.groupby('Parte Ativa')['Vencedor'].value_counts(normalize=True).mul(100).rename('Proporção').reset_index()

# Filtra apenas as vitórias do Estado
vit_estados = vit_por_estado[vit_por_estado['Vencedor'] == 'ESTADO']

# Ordenar o DataFrame em ordem crescente de 'Proporção'
vit_estados = vit_estados.sort_values('Proporção', ascending=True)

# Gráfico de barras horizontal
fig3 = px.bar(vit_estados, y='Parte Ativa', x='Proporção', orientation='h', title='Proporção de vitórias dos Estados')

# Exibir o gráfico
st.plotly_chart(fig3, use_container_width=True)

# Seção 3: Variação das decisões ao longo do tempo
# Contagem de decisões por Ano e Vencedor
decisoes_ano = df_filtered.groupby(['Ano', 'Vencedor']).size().reset_index(name='Número de Decisões')

# Gráfico de barras empilhadas
fig4 = px.bar(decisoes_ano, x='Ano', y='Número de Decisões', color='Vencedor', title='Decisões ao longo do tempo')

# Atualizar o layout para mostrar todos os anos
fig4.update_layout(xaxis=dict(dtick=1))

# Exibir o gráfico
st.plotly_chart(fig4, use_container_width=True)

# Anotações Dinâmicas:
# Verifica se o DataFrame não está vazio
if not decisoes_ano.empty:
    # Identificar o ano com mais decisões
    ano_top = decisoes_ano.groupby('Ano')['Número de Decisões'].sum().idxmax()
    num_decisoes_top = decisoes_ano.groupby('Ano')['Número de Decisões'].sum().max()

    st.markdown(f"**Insight:** No ano de **{ano_top}**, houve o maior número de decisões, totalizando **{num_decisoes_top}** decisões no contexto selecionado.")
else:
    st.markdown("**Insight:** Não há dados para o contexto selecionado.")

# Seção 4: Como as decisões variam entre Ministros
# Contagem de decisões por Relator
decisoes_relator = df_filtered['Relator'].value_counts().reset_index()
decisoes_relator.columns = ['Relator', 'Número de Decisões']

# Ordenar o DataFrame em ordem crescente de 'Número de Decisões'
decisoes_relator = decisoes_relator.sort_values('Número de Decisões', ascending=True)

# Gráfico de barras horizontal
fig5 = px.bar(decisoes_relator, y='Relator', x='Número de Decisões', orientation='h', title='Decisões por Ministro Relator')

# Atualizar a ordem das categorias para refletir a ordem decrescente
fig5.update_layout(yaxis={'categoryorder':'total ascending'})

# Exibir o gráfico
st.plotly_chart(fig5, use_container_width=True)

# Heatmap (Mapa de Calor) de Decisões por Relator e Ano:
# Contagem de decisões por Relator e Ano
decisoes_relator_ano = df_filtered.groupby(['Relator', 'Ano']).size().reset_index(name='Número de Decisões')

# Pivot para formato adequado ao heatmap
heatmap_data = decisoes_relator_ano.pivot(index='Relator', columns='Ano', values='Número de Decisões').fillna(0)

# Gráfico de heatmap
fig6 = px.imshow(heatmap_data, aspect='auto', color_continuous_scale='Viridis', title='Mapa de Calor das Decisões por Ministro e Ano')

# Exibir o gráfico
st.plotly_chart(fig6, use_container_width=True)

# Seção 5: Tabela Detalhada
# Selecionar colunas relevantes
colunas = ['Numero_ACO', 'Data de julgamento', 'URL', 'Resumo']
tabela = df_filtered[colunas]

# Exibir a tabela
st.subheader('Detalhamento das Decisões')
st.dataframe(tabela)

# Botão para download dos dados filtrados
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(tabela)

st.download_button(
    label="Baixar dados filtrados em CSV",
    data=csv,
    file_name='dados_filtrados.csv',
    mime='text/csv',
)