# ============================================================================
# BI IMOBILIÁRIA - DASHBOARD ESTRATÉGICO
# Versão Produção com todas as funcionalidades avançadas
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from io import BytesIO

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

st.set_page_config(page_title="BI Imobiliário BH", layout="wide")

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

EXCEL_FILE = DATA_DIR / "dados_imoveis_exemplo.xlsx"
CSV_FILE = DATA_DIR / "imoveis_base.csv"

# ============================================================================
# FUNÇÕES DE CARREGAMENTO
# ============================================================================

@st.cache_data
def load_enhanced_data():
    """Gera dados simulados com lógica de BH"""
    np.random.seed(42)
    n_rows = 800
    
    bairros = ['Savassi', 'Funcionários', 'Castelo']
    tipos = ['Apartamento', 'Cobertura', 'Área Privativa']
    
    data = {
        'id_lead': range(1, n_rows + 1),
        'bairro': np.random.choice(bairros, n_rows, p=[0.25, 0.25, 0.5]), 
        'tipo': np.random.choice(tipos, n_rows, p=[0.7, 0.1, 0.2]),
        'metragem': np.random.randint(55, 280, n_rows),
        'dias_no_mercado': np.random.randint(1, 365, n_rows),
    }
    
    df = pd.DataFrame(data)
    
    # Precificação por bairro e tipo
    def get_market_values(row):
        base_m2 = 13500 if row['bairro'] in ['Savassi', 'Funcionários'] else 7200
        fator_tipo = 1.3 if row['tipo'] == 'Cobertura' else (1.1 if row['tipo'] == 'Área Privativa' else 1.0)
        preco_venda = row['metragem'] * base_m2 * fator_tipo
        sobrepreco = 1.0 + (row['dias_no_mercado'] / 1000) 
        preco_final = preco_venda * sobrepreco * np.random.uniform(0.95, 1.05)
        return preco_final

    df['preco_venda'] = df.apply(get_market_values, axis=1)
    df['preco_m2'] = df['preco_venda'] / df['metragem']

    # Funil de Vendas
    df['contato_efetivo'] = np.random.choice([0, 1], size=n_rows, p=[0.4, 0.6])
    
    def check_visit(row):
        if row['contato_efetivo'] == 0:
            return 0
        prob_visita = 0.20 if row['bairro'] in ['Savassi', 'Funcionários'] else 0.35
        return np.random.choice([0, 1], p=[1-prob_visita, prob_visita])

    df['visita_agendada'] = df.apply(check_visit, axis=1)

    # Comissões
    def get_commission(row):
        taxa = 0.03 if row['bairro'] in ['Savassi', 'Funcionários'] else 0.05
        return row['preco_venda'] * taxa

    df['receita_projetada'] = df.apply(get_commission, axis=1)
    
    # Score de Urgência
    def calc_urgencia_score(row):
        prob_conversao = row['contato_efetivo'] * 0.6 + (1 - min(row['dias_no_mercado'] / 365, 1)) * 0.4
        max_receita = df['receita_projetada'].max()
        receita_norm = row['receita_projetada'] / max_receita if max_receita > 0 else 0
        return prob_conversao * receita_norm * 100
    
    df['score_urgencia'] = df.apply(calc_urgencia_score, axis=1)
    df['dias_sem_contato'] = np.random.randint(0, 60, n_rows)
    
    return df

df_raw = load_enhanced_data()

# ============================================================================
# FUNÇÕES DE EXPORTAÇÃO
# ============================================================================

def export_para_excel(df_data):
    """Exporta para Excel com múltiplas abas e formatação"""
    output = BytesIO()
    pipeline_quente = df_data[df_data['visita_agendada'] == 1]
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Aba 1: Resumo
        resumo = pd.DataFrame({
            'Métrica': ['VGV Total', 'Receita Potencial', 'Ticket Médio', 'Total de Leads', 'Contact Rate', 'Conversion Rate'],
            'Valor': [
                f"R$ {df_data['preco_venda'].sum()/1e6:.2f}M",
                f"R$ {pipeline_quente['receita_projetada'].sum()/1e3:.0f}K",
                f"R$ {df_data['preco_venda'].mean()/1e3:.0f}K",
                len(df_data),
                f"{(df_data['contato_efetivo'].sum()/len(df_data)*100):.1f}%",
                f"{(df_data['visita_agendada'].sum()/df_data['contato_efetivo'].sum()*100 if df_data['contato_efetivo'].sum() > 0 else 0):.1f}%"
            ]
        })
        resumo.to_excel(writer, sheet_name='Resumo', index=False)
        
        # Aba 2: Imóveis (ordenado por score)
        df_export = df_data[['id_lead', 'bairro', 'tipo', 'metragem', 'preco_venda', 'preco_m2', 'dias_no_mercado', 'score_urgencia', 'dias_sem_contato']].copy()
        df_export = df_export.sort_values('score_urgencia', ascending=False)
        df_export.to_excel(writer, sheet_name='Imóveis', index=False)
        
        # Aba 3: Análise por Bairro
        analise_bairro = df_data.groupby('bairro').agg({
            'preco_venda': ['sum', 'mean'],
            'preco_m2': 'mean',
            'id_lead': 'count',
            'visita_agendada': 'sum',
            'receita_projetada': 'sum'
        }).round(2)
        analise_bairro.to_excel(writer, sheet_name='Análise Bairro')
    
    output.seek(0)
    return output

def gerar_print_relatorio(df_data):
    """Gera relatório em texto formatado"""
    pipeline_quente = df_data[df_data['visita_agendada'] == 1]
    
    relatorio = f"""
╔════════════════════════════════════════════════════════════════╗
║       RELATÓRIO ESTRATÉGICO - BI IMOBILIÁRIO BH                ║
║                   {datetime.now().strftime('%d/%m/%Y %H:%M')}                        ║
╚════════════════════════════════════════════════════════════════╝

📊 RESUMO EXECUTIVO
{'─'*60}
VGV Total (Estoque):             R$ {df_data['preco_venda'].sum()/1e6:>12,.1f} M
Receita Projetada (Quente):      R$ {pipeline_quente['receita_projetada'].sum()/1e3:>12,.0f} K
Ticket Médio:                    R$ {df_data['preco_venda'].mean()/1e3:>12,.0f} K

📈 EFICIÊNCIA OPERACIONAL
{'─'*60}
Total de Leads:                  {len(df_data):>15}
Contact Rate (Eficiência):       {(df_data['contato_efetivo'].sum()/len(df_data)*100):>14.1f}%
Conversion Rate (Qualidade):     {(df_data['visita_agendada'].sum()/df_data['contato_efetivo'].sum()*100 if df_data['contato_efetivo'].sum() > 0 else 0):>14.1f}%
Visitas Agendadas:               {df_data['visita_agendada'].sum():>15}

🎯 TOP 5 IMÓVEIS PRIORITÁRIOS (Score de Urgência)
{'─'*60}
"""
    
    top5 = df_data.nlargest(5, 'score_urgencia')[['bairro', 'tipo', 'metragem', 'preco_venda', 'dias_no_mercado', 'score_urgencia']]
    for idx, (_, row) in enumerate(top5.iterrows(), 1):
        relatorio += f"\n{idx}. {row['bairro']:15} | {row['tipo']:15} | {row['metragem']:>3}m² | R${row['preco_venda']/1e3:>8,.0f}K | Score: {row['score_urgencia']:>6.1f}"
    
    leads_alert = df_data[df_data['dias_sem_contato'] > 30]
    relatorio += f"\n\n⚠️  ALERTAS DE CONTATO\n{'─'*60}"
    relatorio += f"\nLeads sem contato > 30 dias: {len(leads_alert)}"
    if len(leads_alert) > 0:
        for idx, (_, row) in enumerate(leads_alert.head(5).iterrows(), 1):
            relatorio += f"\n   {idx}. {row['bairro']} - {row['dias_sem_contato']} dias sem contato"
    
    relatorio += f"\n\n{'='*60}\nFim do Relatório\n{'='*60}\n"
    
    return relatorio

# ============================================================================
# SIDEBAR - FILTROS
# ============================================================================

with st.sidebar:
    st.header("🔍 Filtros Estratégicos")
    
    bairros_sel = st.multiselect(
        "Bairros", 
        df_raw['bairro'].unique(), 
        default=list(df_raw['bairro'].unique())
    )
    
    tipos_sel = st.multiselect(
        "Tipos", 
        df_raw['tipo'].unique(), 
        default=list(df_raw['tipo'].unique())
    )

df_filtered = df_raw[
    (df_raw['bairro'].isin(bairros_sel)) & 
    (df_raw['tipo'].isin(tipos_sel))
].copy()

if df_filtered.empty:
    st.error("Sem dados para os filtros selecionados.")
    st.stop()

# ============================================================================
# TÍTULO
# ============================================================================

st.title("🏢 BI IMOBILIÁRIO BH")
st.markdown("Dashboard Estratégico de Análise de Mercado Imobiliário")

# ============================================================================
# ABAS PRINCIPAIS
# ============================================================================

tab1, tab2, tab3 = st.tabs([
    "💰 Performance Financeira", 
    "🧠 Inteligência de Mercado", 
    "⚡ Ferramentas Avançadas"
])

# ============================================================================
# TAB 1: PERFORMANCE FINANCEIRA
# ============================================================================

with tab1:
    st.markdown("### Visão de Receita e Pipeline")
    
    vgv_total = df_filtered['preco_venda'].sum()
    pipeline_quente = df_filtered[df_filtered['visita_agendada'] == 1]
    receita_potencial = pipeline_quente['receita_projetada'].sum()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("VGV Total (Estoque)", f"R$ {vgv_total/1e6:,.1f} M")
    c2.metric("Receita Projetada (Pipeline Quente)", f"R$ {receita_potencial/1e3:,.0f} K")
    c3.metric("Ticket Médio", f"R$ {df_filtered['preco_venda'].mean()/1e3:,.0f} K")
    
    st.divider()
    
    receita_bairro = pipeline_quente.groupby('bairro')['receita_projetada'].sum().reset_index()
    fig_rev = px.bar(
        receita_bairro, 
        x='bairro', 
        y='receita_projetada',
        title="Onde está o dinheiro? (Receita Projetada por Bairro)",
        text_auto='.2s',
        color='bairro',
        color_discrete_map={'Savassi': '#EF553B', 'Funcionários': '#636EFA', 'Castelo': '#00CC96'}
    )
    st.plotly_chart(fig_rev, width='stretch')

# ============================================================================
# TAB 2: INTELIGÊNCIA DE MERCADO
# ============================================================================

with tab2:
    st.markdown("### Eficiência Operacional & Análise de Preço")
    
    total_leads = len(df_filtered)
    total_contatos = int(df_filtered['contato_efetivo'].sum())
    total_visitas = int(df_filtered['visita_agendada'].sum())
    
    contact_rate = (total_contatos / total_leads) * 100 if total_leads > 0 else 0
    conversion_rate = (total_visitas / total_contatos) * 100 if total_contatos > 0 else 0
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Leads Totais", total_leads)
    k2.metric("Contact Rate", f"{contact_rate:.1f}%")
    k3.metric("Conversion Rate", f"{conversion_rate:.1f}%")
    k4.metric("Visitas Agendadas", total_visitas)
    
    st.divider()
    
    st.subheader("Análise de Liquidez: Preço m² vs. Dias de Estoque")
    st.caption("Pontos no canto superior direito indicam imóveis caros e encalhados.")
    
    fig_scatter = px.scatter(
        df_filtered,
        x='dias_no_mercado',
        y='preco_m2',
        color='bairro',
        size='metragem',
        hover_data=['tipo', 'preco_venda'],
        trendline="ols",
        title="Correlação: Imóveis mais caros ficam mais tempo parados?",
        color_discrete_map={'Savassi': '#EF553B', 'Funcionários': '#636EFA', 'Castelo': '#00CC96'}
    )
    
    media_m2 = df_filtered['preco_m2'].mean()
    fig_scatter.add_hline(y=media_m2, line_dash="dot", annotation_text="Média Preço/m²")
    fig_scatter.add_vline(x=180, line_dash="dot", annotation_text="Zona de Risco (>6 meses)")
    
    st.plotly_chart(fig_scatter, width='stretch')

# ============================================================================
# TAB 3: FERRAMENTAS AVANÇADAS
# ============================================================================

with tab3:
    st.markdown("### 🎯 Score de Urgência")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("**Score de Urgência** = Probabilidade de Conversão × Impacto Financeiro")
    
    with col2:
        num_top = st.number_input("Mostrar Top N", min_value=5, max_value=50, value=10)
    
    df_urgencia = df_filtered.nlargest(num_top, 'score_urgencia')[
        ['id_lead', 'bairro', 'tipo', 'metragem', 'preco_venda', 'dias_no_mercado', 'dias_sem_contato', 'score_urgencia']
    ].copy()
    df_urgencia['preco_venda'] = df_urgencia['preco_venda'].apply(lambda x: f"R$ {x/1e3:.0f}K")
    df_urgencia['score_urgencia'] = df_urgencia['score_urgencia'].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(df_urgencia, width='stretch', hide_index=True)
    
    fig_score = px.box(
        df_filtered,
        x='bairro',
        y='score_urgencia',
        color='bairro',
        title="Distribuição de Score por Bairro",
        color_discrete_map={'Savassi': '#EF553B', 'Funcionários': '#636EFA', 'Castelo': '#00CC96'}
    )
    st.plotly_chart(fig_score, width='stretch')
    
    st.divider()
    st.markdown("### ⚠️ Sistema de Alerta")
    
    col_alert1, col_alert2, col_alert3 = st.columns(3)
    
    dias_limite = col_alert1.slider("Limite de dias sem contato", 10, 60, 30)
    
    leads_alerta = df_filtered[df_filtered['dias_sem_contato'] > dias_limite]
    receita_em_risco = leads_alerta['receita_projetada'].sum()
    
    col_alert1.metric("Leads em Alerta", len(leads_alerta))
    col_alert2.metric("Receita em Risco", f"R$ {receita_em_risco/1e3:.0f}K")
    col_alert3.metric("% do Total", f"{(len(leads_alerta)/len(df_filtered)*100):.1f}%" if len(df_filtered) > 0 else "0%")
    
    if len(leads_alerta) > 0:
        st.warning(f"⚠️ {len(leads_alerta)} leads precisam de contato urgente!")
        
        df_alerta_display = leads_alerta[[
            'id_lead', 'bairro', 'tipo', 'metragem', 'preco_venda', 'dias_sem_contato', 'receita_projetada'
        ]].sort_values('dias_sem_contato', ascending=False).head(15).copy()
        
        df_alerta_display['preco_venda'] = df_alerta_display['preco_venda'].apply(lambda x: f"R$ {x/1e3:.0f}K")
        df_alerta_display['receita_projetada'] = df_alerta_display['receita_projetada'].apply(lambda x: f"R$ {x/1e3:.0f}K")
        
        st.dataframe(df_alerta_display, width='stretch', hide_index=True)
    
    st.divider()
    st.markdown("### 💰 Simulador de Desconto")
    
    col_sim1, col_sim2 = st.columns(2)
    
    with col_sim1:
        desconto_pct = st.slider("Percentual de desconto", 0, 20, 5) / 100
        st.info(f"**Desconto aplicado: {desconto_pct*100:.0f}%**")
    
    df_sim = df_filtered.copy()
    df_sim['preco_novo'] = df_sim['preco_venda'] * (1 - desconto_pct)
    df_sim['dias_economizados'] = (desconto_pct * 100) * 5
    df_sim['dias_novo'] = (df_sim['dias_no_mercado'] - df_sim['dias_economizados']).clip(lower=1)
    
    with col_sim2:
        st.metric("Redução média de estoque", f"{df_sim['dias_economizados'].mean():.1f} dias")
    
    vgv_original = df_filtered['preco_venda'].sum()
    vgv_desconto = df_sim['preco_novo'].sum()
    diferenca = vgv_original - vgv_desconto
    
    comparativo = pd.DataFrame({
        'Métrica': ['VGV Total', 'Preço Médio', 'Dias Médio', 'Perda em Receita'],
        'Cenário Atual': [
            f"R$ {vgv_original/1e6:.2f}M",
            f"R$ {df_filtered['preco_venda'].mean()/1e3:.0f}K",
            f"{df_filtered['dias_no_mercado'].mean():.0f} dias",
            "-"
        ],
        'Com Desconto': [
            f"R$ {vgv_desconto/1e6:.2f}M",
            f"R$ {df_sim['preco_novo'].mean()/1e3:.0f}K",
            f"{df_sim['dias_novo'].mean():.0f} dias",
            f"R$ {diferenca/1e3:.0f}K"
        ]
    })
    
    st.dataframe(comparativo, width='stretch', hide_index=True)
    
    fig_sim = go.Figure(data=[
        go.Bar(name='Cenário Atual', x=['VGV Total'], y=[vgv_original/1e6]),
        go.Bar(name=f'Com Desconto ({desconto_pct*100:.0f}%)', x=['VGV Total'], y=[vgv_desconto/1e6])
    ])
    fig_sim.update_layout(title="Impacto Financeiro", yaxis_title="VGV (Milhões)", barmode='group')
    st.plotly_chart(fig_sim, width='stretch')
    
    st.divider()
    st.markdown("### 📥 Exportar Relatório")
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        if st.button("📄 Gerar Relatório", use_container_width=True):
            relatorio_texto = gerar_print_relatorio(df_filtered)
            st.code(relatorio_texto, language="text")
            st.download_button(
                label="⬇️ Baixar TXT",
                data=relatorio_texto,
                file_name=f"relatorio_bh_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    with col_exp2:
        excel_buffer = export_para_excel(df_filtered)
        st.download_button(
            label="📊 Baixar Excel",
            data=excel_buffer,
            file_name=f"relatorio_bh_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

st.markdown("---")
st.caption("Dashboard Estratégico - Dados fictícios baseados na dinâmica de mercado de BH.")
