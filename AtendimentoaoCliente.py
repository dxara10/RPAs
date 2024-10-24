import sqlite3

# Função para criar a tabela de clientes no banco de dados
def criar_tabela_clientes():
    conn = sqlite3.connect("atendimento_ao_cliente.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        email TEXT,
        telefone TEXT,
        historico TEXT
    )
    """)
    conn.commit()
    conn.close()

# Função para adicionar um novo cliente ao banco de dados
def adicionar_cliente(nome, email, telefone):
    conn = sqlite3.connect("atendimento_ao_cliente.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nome, email, telefone, historico) VALUES (?, ?, ?, '')", (nome, email, telefone))
    conn.commit()
    conn.close()

# Função para registrar o histórico de interações com um cliente
def registrar_interacao(cliente_id, historico):
    conn = sqlite3.connect("atendimento_ao_cliente.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE clientes SET historico = ? WHERE id = ?", (historico, cliente_id))
    conn.commit()
    conn.close()

# Criar a tabela de clientes (se ainda não existir)
criar_tabela_clientes()

# Exemplo de uso:
# Adicionar clientes
adicionar_cliente("Alice", "alice@example.com", "555-1234")
adicionar_cliente("Bob", "bob@example.com", "555-5678")

# Registrar interações com clientes
registrar_interacao(1, "Cliente muito satisfeito com o produto.")
registrar_interacao(2, "Cliente com dúvidas sobre faturamento.")

# Listar clientes e histórico de interações
conn = sqlite3.connect("atendimento_ao_cliente.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM clientes")
clientes = cursor.fetchall()
conn.close()

print("Atendimento ao Cliente:")
for cliente in clientes:
    print(f"Nome: {cliente[1]}, Email: {cliente[2]}, Telefone: {cliente[3]}")
    print(f"Histórico de Interações: {cliente[4]}\n")
