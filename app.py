from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'klaus_gerenciador_vendas_secreto'

# Filtro customizado para o Jinja2 (Moeda BRL)
@app.template_filter('currency')
def currency_format(value):
    try:
        return f"{float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return value

# Filtro customizado para o Jinja2 (Data PT-BR)
@app.template_filter('date_br')
def date_br_format(value):
    if not value or len(str(value)) < 10:
        return value
    # value expected: "YYYY-MM-DD"
    try:
        parts = str(value).split('-')
        return f"{parts[2]}/{parts[1]}/{parts[0]}"
    except IndexError:
        return value

def parse_monetary(value):
    if not value:
        raise ValueError("Valor vazio")
    val_str = str(value).strip()
    
    if ',' in val_str:
        val_str = val_str.replace('.', '')
        val_str = val_str.replace(',', '.')
    else:
        parts = val_str.split('.')
        if len(parts) > 1 and len(parts[-1]) == 3:
            val_str = val_str.replace('.', '')
            
    return float(val_str)


def init_db():
    conn = sqlite3.connect('database.db')
    
    # Tabela de Usuários
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL
        )
    ''')

    # Tabela de Vendas
    conn.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            data_venda TEXT NOT NULL,
            vendedor TEXT NOT NULL,
            forma_pagamento TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES usuarios (id)
        )
    ''')
    
    # Migração simples para adicionar user_id em uma base já existente
    try:
        conn.execute('ALTER TABLE vendas ADD COLUMN user_id INTEGER REFERENCES usuarios(id)')
    except sqlite3.OperationalError:
        pass # Coluna já existe
        
    conn.commit()
    conn.close()

# Inicializa o banco ao rodar o app
init_db()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Decorator de login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Por favor, faça login para acessar esta página.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro-usuario", methods=["GET", "POST"])
def cadastro_usuario():
    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        senha_hash = generate_password_hash(senha)
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)', (nome, email, senha_hash))
            conn.commit()
            flash("Usuário cadastrado com sucesso! Faça login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Este email já está cadastrado.", "error")
        finally:
            conn.close()
            
    return render_template("cadastro_usuario.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        senha = request.form['senha']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['senha_hash'], senha):
            session['user_id'] = user['id']
            session['user_nome'] = user['nome']
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Email ou senha incorretos.", "error")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso.", "success")
    return redirect(url_for('index'))

@app.route("/cadastro", methods=["GET", "POST"])
@login_required
def cadastro():
    if request.method == "POST":
        produto = request.form['produto']
        categoria = request.form['categoria']
        quantidade = request.form['quantidade']
        preco_unitario_str = request.form['preco']
        data_venda = request.form['data']
        vendedor = request.form['vendedor']
        forma_pagamento = request.form['pagamento']
        user_id = session['user_id']
        
        try:
            preco_unitario = parse_monetary(preco_unitario_str)
        except ValueError:
            flash("Valor de preço inválido. Use formatos como 1000, 1.000,50 ou 1000,50.", "error")
            return render_template("cadastro.html")

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO vendas (produto, categoria, quantidade, preco_unitario, data_venda, vendedor, forma_pagamento, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (produto, categoria, quantidade, preco_unitario, data_venda, vendedor, forma_pagamento, user_id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('vendas'))
        
    return render_template("cadastro.html")

@app.route("/vendas")
@login_required
def vendas():
    conn = get_db_connection()
    vendas_lista = conn.execute('SELECT * FROM vendas WHERE user_id = ? ORDER BY data_venda DESC, id DESC', (session['user_id'],)).fetchall()
    conn.close()
    return render_template("vendas.html", vendas=vendas_lista)

@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    conn = get_db_connection()
    venda = conn.execute('SELECT * FROM vendas WHERE id = ? AND user_id = ?', (id, session['user_id'])).fetchone()

    if venda is None:
        conn.close()
        flash("Venda não encontrada ou você não tem permissão para editá-la.", "error")
        return redirect(url_for('vendas'))

    if request.method == "POST":
        produto = request.form['produto']
        categoria = request.form['categoria']
        quantidade = request.form['quantidade']
        preco_unitario_str = request.form['preco']
        data_venda = request.form['data']
        vendedor = request.form['vendedor']
        forma_pagamento = request.form['pagamento']
        
        try:
            preco_unitario = parse_monetary(preco_unitario_str)
        except ValueError:
            flash("Valor de preço inválido. Use formatos como 1000, 1.000,50 ou 1000,50.", "error")
            return render_template("cadastro.html", venda=venda)

        conn.execute('''
            UPDATE vendas SET produto = ?, categoria = ?, quantidade = ?, preco_unitario = ?, data_venda = ?, vendedor = ?, forma_pagamento = ?
            WHERE id = ? AND user_id = ?
        ''', (produto, categoria, quantidade, preco_unitario, data_venda, vendedor, forma_pagamento, id, session['user_id']))
        conn.commit()
        conn.close()
        
        flash("Venda atualizada com sucesso!", "success")
        return redirect(url_for('vendas'))
        
    conn.close()
    return render_template("cadastro.html", venda=venda)

@app.route("/excluir/<int:id>", methods=["POST"])
@login_required
def excluir(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM vendas WHERE id = ? AND user_id = ?', (id, session['user_id']))
    conn.commit()
    conn.close()
    flash("Venda excluída com sucesso!", "success")
    return redirect(url_for('vendas'))

@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db_connection()
    todas_vendas = conn.execute('SELECT * FROM vendas WHERE user_id = ?', (session['user_id'],)).fetchall()
    
    # Cálculos das métricas com Python
    faturamento_total = sum(v['quantidade'] * v['preco_unitario'] for v in todas_vendas)
    quantidade_total_vendas = len(todas_vendas)
    total_itens = sum(v['quantidade'] for v in todas_vendas)
    ticket_medio = faturamento_total / quantidade_total_vendas if quantidade_total_vendas > 0 else 0
    
    # Agrupamentos
    produtos = {}
    categorias = {}
    categorias_qtd = {}
    pagamentos = {}
    
    produtos_grafico = {}
    datas_faturamento = {}

    for v in todas_vendas:
        # Produto mais vendido (por qtd de itens)
        produtos[v['produto']] = produtos.get(v['produto'], 0) + v['quantidade']
        # Usaremos faturamento por produto para o gráfico de barras
        produtos_grafico[v['produto']] = produtos_grafico.get(v['produto'], 0) + (v['quantidade'] * v['preco_unitario'])
        
        # Categoria (por faturamento) -> Dona de Doughnut
        categorias[v['categoria']] = categorias.get(v['categoria'], 0) + (v['quantidade'] * v['preco_unitario'])
        # Nova Inteligência: Categoria (por Volume de Itens Absoluto)
        categorias_qtd[v['categoria']] = categorias_qtd.get(v['categoria'], 0) + v['quantidade']
        
        # Pagamento mais usado (qtd de vendas)
        pagamentos[v['forma_pagamento']] = pagamentos.get(v['forma_pagamento'], 0) + 1
        
        # Faturamento no tempo (Convertendo formato para BR antes de colocar no gráfico pra ficar user-friendly)
        data_exibicao = date_br_format(v['data_venda'])
        datas_faturamento[data_exibicao] = datas_faturamento.get(data_exibicao, 0) + (v['quantidade'] * v['preco_unitario'])
        
    produto_mais_vendido = max(produtos, key=produtos.get) if produtos else "N/A"
    categoria_faturamento = max(categorias, key=categorias.get) if categorias else "N/A"
    pagamento_usado = max(pagamentos, key=pagamentos.get) if pagamentos else "N/A"
    
    metrics = {
        'faturamento': faturamento_total,
        'vendas': quantidade_total_vendas,
        'itens': total_itens,
        'ticket': ticket_medio,
        'produto_top': produto_mais_vendido,
        'categoria_top': categoria_faturamento.capitalize() if categoria_faturamento != "N/A" else "N/A",
        'pagamento_top': pagamento_usado.replace('_', ' ').capitalize() if pagamento_usado != "N/A" else "N/A"
    }
    
    vendas_recentes = conn.execute('SELECT * FROM vendas WHERE user_id = ? ORDER BY data_venda DESC, id DESC LIMIT 5', (session['user_id'],)).fetchall()
    conn.close()
    
    # Ordenar time-series (Datas crescentes)
    datas_faturamento = dict(sorted(datas_faturamento.items()))

    chart_data = {
        'produtos': list(produtos_grafico.keys()),
        'faturamento_produtos': list(produtos_grafico.values()),
        'categorias': list(categorias.keys()),
        'faturamento_categorias': list(categorias.values()),
        'categorias_qtd_labels': list(categorias_qtd.keys()),
        'categorias_qtd_valores': list(categorias_qtd.values()),
        'pagamentos': [p.replace('_', ' ').capitalize() for p in pagamentos.keys()],
        'qtd_pagamentos': list(pagamentos.values()),
        'datas': list(datas_faturamento.keys()),
        'faturamento_linha': list(datas_faturamento.values())
    }
    
    return render_template("dashboard.html", metrics=metrics, recentes=vendas_recentes, chart_data=chart_data)

if __name__ == "__main__":
    app.run(debug=True)