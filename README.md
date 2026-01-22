# 🏢 BI Imobiliário Estratégico - Belo Horizonte

Dashboard interativo para análise de vendas imobiliárias desenvolvido com **Streamlit**.

![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Visão Geral

Sistema de Business Intelligence (BI) especializado em análise de portfólio imobiliário, com foco em:

- **💰 Análise Financeira** - VGV, Receita Projetada e Ticket Médio
- **📈 Dinâmica de Mercado** - Preço m² vs Dias de Estoque, Taxa de Contato e Conversão
- **⚡ Oportunidades** - Score de Urgência, Sistema de Alerta e Simulador de Desconto

---

## 🚀 Recursos Principais

### ✨ Funcionalidades

- **3 Abas Analíticas**
  - 💰 Visão Executiva: Onde está o Dinheiro?
  - 📈 Dinâmica de Mercado & Precificação
  - ⚡ Radar de Oportunidades & Retenção

- **Visualizações Interativas**
  - Gráficos de barras, pizza e scatter plots
  - Análise de tendências com regressão (OLS)
  - Tabelas dinâmicas com dados formatados

- **Análises Automáticas**
  - Resumos inteligentes de cada métrica
  - Identificação de imóveis em zona de risco
  - Ranking de leads por urgência

- **Simuladores**
  - Simulador de desconto com impacto por bairro
  - Sistema de alerta para leads sem contato
  - Projeção de receita por bairro

- **Exportação de Dados**
  - Baixar relatórios em Excel
  - Exportar dados em CSV

---

## 📁 Estrutura do Projeto

```
IMOBILIARIA/
├── main.py                          # 🎯 Ponto de entrada (Streamlit)
├── requirements.txt                 # 📦 Dependências do projeto
├── README.md                        # 📖 Este arquivo
├── .gitignore                       # 🔐 Arquivos a ignorar no Git
└── data/
    ├── imoveis_base.csv             # 📊 Dados em CSV (800 registros)
    ├── dados_imoveis_exemplo.xlsx   # 📊 Dados em Excel (com resumo)
    └── bases_conectadas.txt         # 📝 Log de conexões (gerado automaticamente)
```

---

## 🔧 Instalação Local

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone ou baixe o repositório**
   ```bash
   cd IMOBILIARIA
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute a aplicação**
   ```bash
   streamlit run main.py
   ```

6. **Acesse no navegador**
   ```
   http://localhost:8501
   ```

---

## 🌐 Deploy no Streamlit Cloud

### Preparação para Cloud

1. **Verifique se tudo está organizado**
   - ✅ `main.py` como ponto de entrada
   - ✅ `requirements.txt` com todas as dependências
   - ✅ Pasta `data/` com arquivos de dados
   - ✅ `README.md` com documentação

2. **Push para GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: BI Imobiliário"
   git push origin main
   ```

### Deploy na Nuvem

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em "Deploy an app"
3. Selecione seu repositório GitHub
4. Configure:
   - **Repository:** seu-usuario/IMOBILIARIA
   - **Branch:** main
   - **Main file path:** main.py
5. Clique em "Deploy!"

---

## 📊 Fontes de Dados

O sistema suporta múltiplas fontes:

### 1. **Excel** (Prioritário)
   - Arquivo: `dados_imoveis_exemplo.xlsx`
   - Sheets: "Dados Imóveis" + "Resumo"
   - Registros: 800

### 2. **CSV** (Fallback)
   - Arquivo: `imoveis_base.csv`
   - Registros: 800

### 3. **Simulados** (Fallback Final)
   - Gerado dinamicamente se nenhum arquivo existir
   - Garante funcionamento mesmo sem dados

---

## 🎯 Como Usar

### Navegação

1. **Sidebar (Esquerda)**
   - 📁 Gerenciador de Bases: conecte Excel ou SQL
   - 📊 Fonte Ativa: veja qual base está sendo usada
   - 🔍 Filtros: selecione bairros e tipos de imóvel

2. **Abas (Topo)**
   - **Aba 1:** Análise financeira e receita
   - **Aba 2:** Dinâmica de mercado e preços
   - **Aba 3:** Oportunidades e simulações

### Filtros

- **Bairros:** Savassi, Funcionários, Castelo
- **Tipos:** Apartamento, Cobertura, Área Privativa

### Exportação

- Baixe relatórios completos em Excel
- Exporte dados filtrados em CSV

---

## 📈 Métricas Principais

### Financeiro
- **VGV Total:** Valor Geral de Vendas do estoque
- **Receita Projetada:** Comissões esperadas do pipeline quente
- **Ticket Médio:** Preço médio por imóvel

### Operacional
- **Contact Rate:** % de leads que receberam contato
- **Conversion Rate:** % de contatos que agendaram visita
- **Zona de Risco:** Imóveis caros que ficaram muito tempo no mercado

### Oportunidades
- **Score de Urgência:** Ranking de prioridade (0-100)
- **Sistema de Alerta:** Identifica leads sem follow-up
- **Simulador de Desconto:** Projeto de impacto de reduções

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| Streamlit | 1.28.1 | Framework web |
| Pandas | 2.1.0 | Processamento de dados |
| NumPy | 1.24.3 | Cálculos numéricos |
| Plotly | 5.17.0 | Visualizações interativas |
| OpenPyXL | 3.1.2 | Leitura/escrita Excel |
| Statsmodels | 0.14.0 | Análise estatística (regressão) |

---

## 📝 Estrutura de Dados

### Colunas do Dataset

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id_lead | int | ID único do imóvel |
| bairro | str | Região (Savassi, Funcionários, Castelo) |
| tipo | str | Tipo (Apartamento, Cobertura, Área Privativa) |
| metragem | int | Área em m² |
| dias_no_mercado | int | Dias desde inserção no portfólio |
| preco_venda | float | Preço total de venda |
| preco_m2 | float | Preço por m² |
| contato_efetivo | bool | Se recebeu contato (0/1) |
| visita_agendada | bool | Se agendou visita (0/1) |
| receita_projetada | float | Comissão esperada |
| score_urgencia | float | Prioridade de ação (0-100) |
| dias_sem_contato | int | Dias desde último contato |

---

## 🔐 Segurança e Privacidade

- ✅ Dados simulados (não reais)
- ✅ Sem credenciais sensíveis no código
- ✅ `.gitignore` configurado
- ✅ Pronto para LGPD/GDPR

---

## 📞 Suporte

Para dúvidas ou sugestões:
- 📧 Email: gabriel.eduardo@example.com
- 💬 GitHub Issues: [Abrir issue](https://github.com/seu-usuario/IMOBILIARIA/issues)

---

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

---

## 🙏 Agradecimentos

- Streamlit pela excelente framework
- Plotly pelos gráficos interativos
- Comunidade Python

---

**Versão:** 1.0.0  
**Última atualização:** 22 de Janeiro de 2026  
**Status:** ✅ Pronto para Deploy
