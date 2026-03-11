<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
</div>

<br />

# 📊 Sistema "Relatório de Vendas"

Uma solução Web Full-Stack desenvolvida para o gerenciamento de inventário, registro de vendas e acompanhamento financeiro através de relatórios. O sistema combina um back-end robusto construído com **Python/Flask** e um front-end moderno inspirado em um design **Sci-Fi / Futurista / Cyberpunk**, com elementos refinados como *Glassmorphism* (vidro fumê/neon) e animações dinâmicas de fundo.

---

## 🚀 Principais Funcionalidades

### 🛒 Controle de Produtos
- **Cadastro completo:** Inserção de nome, categoria e preço dos produtos.
- **Gerenciamento visual:** Tabela dinâmica listando o inventário atual (com paginação e edição).
- **Categorização:** Organização de itens por departamentos (ex: Roupas, Eletrônicos).

### 💰 Registro e Gestão de Vendas
- **Lançamento de vendas:** Associação rápida entre clientes, produtos vendidos e a quantidade desejada.
- **Geração de histórico detalhada:** Cada venda processada gera um painel exibindo o resumo financeiro da transação.
- **Cálculo automático de receitas:** Sistema inteligente que multiplica valores e formata no padrão da moeda BRL.

### 📈 Dashboards e Análise de Dados
- **Visão Geral Financeira:** Cards animados e interativos mostrando o "Faturamento Total", "Total de Vendas Realizadas" e principais métricas de desempenho.
- **Gráficos Dinâmicos:** Integração com a biblioteca *Chart.js* para geração de gráficos em Pizza, em Barra ou em Linhas (ex: Vendas por Categoria).
- **Formatadores Personalizados:** Conversão de datas (padrão Internacional -> PT-BR `DD/MM/YYYY`) de forma transparente nas tabelas.

### 🔒 Autenticação e Segurança
- **Sistema de Login Seguro:** Banco de Dados configurado para criptografar senhas (hashes seguros) com a biblioteca `Werkzeug.security`.
- **Controle de Acesso de Rotas:** O sistema só permite visualização de dados ou lançamento de vendas quando a sessão (Session/Cookies) do usuário está ativa. O famoso `@login_required`.
- **Proteção contra SQL-Injection:** Parâmetros formatados nos Data Transfer Objects no padrão SQLite3.

---

## 🛠️ Tecnologias Utilizadas

### Back-End / Lógica
- **Linguagem Principal:** Python 3.x
- **Micro-Framework:** Flask
- **Banco de Dados Relacional:** SQLite 3 (Armazenamento leve e embutido)

### Front-End / Interface Visual
- **Páginas:** HTML5 com integração da engine de templates dinâmicos **Jinja2** (do próprio Flask).
- **Estilização e Tema:** CSS Vanilla, estruturada em blocos modulares (`styles.css` e `auth.css`), focado em UI Futurista, sombreamentos *(box-shadow)* coloridos (Neon Blue/Purple) e layout responsivo.
- **Interatividade:** JavaScript Vanilla para alertas, interações em modais e renderização avançada com *Chart.js*.
- **Iconografia:** Font Awesome

---

## 🎨 Arquitetura de Design (UI/UX)
O grande diferencial da interface é o seu tema visual apelidado de **Tons Obscuros**:
*   Fundo animado gerado matematicamente com JS (Efeito Estelar/Grid Matrix).
*   Glow Effect e animação constante durante "hovers" em cartões de apresentação.
*   Centralização do conteúdo (Cards), transmitindo organização e foco nos números mais importantes do relatório.
