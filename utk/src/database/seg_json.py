import sqlite3
import json
import datetime
from collections import Counter


# ─────────────────────────────────────────────
#  UTILITÁRIOS
# ─────────────────────────────────────────────

def get_last_grammar(cursor):
    """Busca o último grammar_json salvo no banco para comparação."""
    cursor.execute('SELECT grammar_json FROM Operation ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    if row:
        try:
            return json.loads(row[0])
        except Exception:
            return None
    return None


def find_differences(old_data, new_data, path=""):
    """
    Compara dois dicionários JSON recursivamente.
    Retorna lista de strings descrevendo o que mudou.
    Ex: ["map.camera.position alterado", "knots.rio adicionado"]
    """
    differences = []

    if isinstance(new_data, dict) and isinstance(old_data, dict):
        all_keys = set(old_data.keys()) | set(new_data.keys())
        for key in all_keys:
            full_key = f"{path}.{key}" if path else key
            if key not in old_data:
                differences.append(f"'{full_key}' adicionado")
            elif key not in new_data:
                differences.append(f"'{full_key}' removido")
            else:
                differences += find_differences(old_data[key], new_data[key], full_key)
    elif isinstance(new_data, list) and isinstance(old_data, list):
        if new_data != old_data:
            differences.append(f"'{path}' alterado")
    else:
        if old_data != new_data:
            differences.append(f"'{path}' alterado: '{old_data}' → '{new_data}'")

    return differences


# ─────────────────────────────────────────────
#  INSERÇÃO NO BANCO
# ─────────────────────────────────────────────

def imputDataBase(json_file, user_ip=None):
    """
    Lê o grammar.json, detecta diferenças em relação ao último salvo
    e armazena tudo no banco utk.db.
    """
    currentDateTime = datetime.datetime.now()

    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"[ERRO] Arquivo não encontrado: {json_file}")
        return
    except json.JSONDecodeError as e:
        print(f"[ERRO] JSON inválido: {e}")
        return

    conn = sqlite3.connect('utk.db')
    cursor = conn.cursor()

    try:
        # Detectar criação ou atualização
        last_grammar = get_last_grammar(cursor)
        if last_grammar is None:
            operation_type = "creat"
            differences = []
        else:
            differences = find_differences(last_grammar, data)
            operation_type = "update" if differences else "no_change"

        if operation_type == "no_change":
            print("[INFO] Nenhuma alteração detectada. Nada foi salvo.")
            conn.close()
            return

        if differences:
            print(f"[INFO] {len(differences)} alteração(ões) detectada(s):")
            for d in differences:
                print(f"  - {d}")

        # Inserir Operation
        cursor.execute(
            'INSERT INTO Operation (time, type, grammar_json) VALUES (?, ?, ?)',
            (currentDateTime, operation_type, json.dumps(data, ensure_ascii=False))
        )
        id_operation = cursor.lastrowid
        print(f"[OK] Operação '{operation_type}' registrada com id={id_operation}")

        # Registrar usuário
        if user_ip:
            cursor.execute(
                'INSERT INTO User (ip, id_operation) VALUES (?, ?)',
                (user_ip, id_operation)
            )

        # Grid
        grid = data.get("grid", {})
        if grid:
            cursor.execute(
                'INSERT INTO Grid (width, height, id_operation) VALUES (?, ?, ?)',
                (grid.get("width"), grid.get("height"), id_operation)
            )

        # Grammar_Position
        gp = data.get("grammar_position", {})
        if gp:
            cursor.execute(
                'INSERT INTO Grammar_Position (width, height, id_operation) VALUES (?, ?, ?)',
                (str(gp.get("width")), str(gp.get("height")), id_operation)
            )

        # Components
        components = data.get("components", [])
        if components:
            component = components[0]

            position = component.get("position", {})
            if position:
                cursor.execute(
                    'INSERT INTO Position (width, height, id_operation) VALUES (?, ?, ?)',
                    (str(position.get("width")), str(position.get("height")), id_operation)
                )

            plots = component.get("plots", [])
            if plots:
                plot = plots[0]
                cursor.execute(
                    'INSERT INTO Plots (description, arg, arrangement, id_operation) VALUES (?, ?, ?, ?)',
                    (plot.get("description"), plot.get("arg"), plot.get("arrangement"), id_operation)
                )

            maps = component.get("map", {})
            if maps:
                camera = maps.get("camera", {})
                direction = camera.get("direction", {})
                cursor.execute(
                    'INSERT INTO Maps (position, direction_right, direction_lookAt, direction_up, id_operation) VALUES (?, ?, ?, ?, ?)',
                    (
                        str(camera.get("position")),
                        str(direction.get("right")),
                        str(direction.get("lookAt")),
                        str(direction.get("up")),
                        id_operation
                    )
                )
                id_map = cursor.lastrowid

                for knot in maps.get("knots", []):
                    cursor.execute('INSERT INTO Maps_Knots (knots, maps) VALUES (?, ?)', (knot, id_map))

                for interaction in maps.get("interactions", []):
                    cursor.execute('INSERT INTO Interactions (interaction, maps) VALUES (?, ?)', (interaction, id_map))

            for widget in component.get("widgets", []):
                cursor.execute('INSERT INTO Widgets (type, id_operation) VALUES (?, ?)', (widget.get("type"), id_operation))

            for knot in component.get("knots", []):
                cursor.execute(
                    'INSERT INTO Knots (name, integration_scheme, id_operation) VALUES (?, ?, ?)',
                    (knot.get("id"), json.dumps(knot.get("integration_scheme"), ensure_ascii=False), id_operation)
                )

        conn.commit()
        print("[OK] Dados salvos com sucesso.\n")

    except Exception as e:
        conn.rollback()
        print(f"[ERRO] Falha ao salvar no banco: {e}")
    finally:
        conn.close()


# ─────────────────────────────────────────────
#  ANÁLISE COMPORTAMENTAL
# ─────────────────────────────────────────────

def analisar_comportamento(user_ip, limites=[5, 10, 50]):
    """
    Analisa o comportamento de um usuário com base nos últimos N updates.
    Mostra quais campos foram mais alterados nos últimos 5, 10 e 50 saves.

    Parâmetros:
        user_ip (str): IP do usuário a analisar
        limites (list): janelas de análise (padrão: 5, 10 e 50 últimos updates)
    """
    conn = sqlite3.connect('utk.db')
    cursor = conn.cursor()

    # Buscar os grammar_json do usuário do mais recente para o mais antigo
    cursor.execute("""
        SELECT o.grammar_json, o.time
        FROM Operation o
        JOIN User u ON u.id_operation = o.id
        WHERE u.ip = ? AND o.type = 'update'
        ORDER BY o.id DESC
    """, (user_ip,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"[INFO] Nenhum update encontrado para o usuário {user_ip}.")
        return

    # Converter grammar_json de string para dict
    grammars = []
    for row in rows:
        try:
            grammars.append(json.loads(row[0]))
        except Exception:
            continue

    print(f"\n{'='*55}")
    print(f"  ANÁLISE COMPORTAMENTAL — Usuário: {user_ip}")
    print(f"  Total de updates registrados: {len(grammars)}")
    print(f"{'='*55}")

    for limite in limites:
        janela = grammars[:limite]  # os N mais recentes

        if len(janela) < 2:
            print(f"\n  [Últimos {limite}] Dados insuficientes (mínimo 2 registros).")
            continue

        # Contar diferenças entre cada par consecutivo
        contador = Counter()
        for i in range(len(janela) - 1):
            diffs = find_differences(janela[i + 1], janela[i])
            for d in diffs:
                campo = d.split("'")[1] if "'" in d else d
                contador[campo] += 1

        print(f"\n  📊 Últimos {limite} updates — campos mais alterados:")
        print(f"  {'-'*45}")

        if not contador:
            print("  Nenhuma diferença encontrada nessa janela.")
            continue

        total = sum(contador.values())
        for campo, qtd in contador.most_common(10):
            barra = "█" * qtd
            pct = (qtd / total) * 100
            print(f"  {campo:<35} {barra} {qtd}x ({pct:.0f}%)")

    print(f"\n{'='*55}\n")


def resumo_geral():
    """
    Mostra um resumo geral de todos os usuários e suas atividades.
    Útil para comparar comportamentos entre usuários diferentes.
    """
    conn = sqlite3.connect('utk.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.ip, COUNT(o.id) as total, MAX(o.time) as ultimo_acesso
        FROM User u
        JOIN Operation o ON o.id = u.id_operation
        GROUP BY u.ip
        ORDER BY total DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("[INFO] Nenhum usuário registrado ainda.")
        return

    print(f"\n{'='*55}")
    print(f"  RESUMO GERAL DE USUÁRIOS")
    print(f"{'='*55}")
    print(f"  {'IP':<20} {'Updates':>8}  {'Último acesso'}")
    print(f"  {'-'*50}")
    for ip, total, ultimo in rows:
        print(f"  {ip:<20} {total:>8}x  {ultimo}")
    print(f"{'='*55}\n")


# ─────────────────────────────────────────────
#  EXECUÇÃO
# ─────────────────────────────────────────────

if __name__ == "__main__":

    # 1 - Salvar novo estado do grammar.json
    imputDataBase(
        json_file='examples/downtown_manhattan/grammar.json',
        user_ip='192.168.0.1'
    )

    # 2 - Analisar comportamento do usuário nos últimos 5, 10 e 50 updates
    analisar_comportamento(user_ip='192.168.0.1', limites=[5, 10, 50])

    # 3 - Ver resumo geral de todos os usuários
    resumo_geral()