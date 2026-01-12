import subprocess
import sys

# DB Config
DB_USER = "ragnarok"
DB_PASS = "BatataRagnavenaServerRoque"
DB_NAME = "ragnavena"

def get_char_data():
    query = (
        "SELECT L.userid, C.name, C.class, C.base_level, C.job_level, "
        "IFNULL(C.last_login, 'Never') as last_login, "
        "C.char_id as char_created_id, "
        "L.account_id as acc_created_id "
        "FROM login L "
        "JOIN `char` C ON L.account_id = C.account_id "
        "ORDER BY C.last_login DESC, C.char_id ASC, L.account_id ASC;"
    )
    
    cmd = [
        "mysql",
        f"-u{DB_USER}",
        f"-p{DB_PASS}",
        "-D", DB_NAME,
        "-e", query,
        "-B" # Batch mode (tab separated)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing database query: {e.stderr}")
        return None

def print_table(data):
    if not data:
        return

    lines = data.strip().split('\n')
    if not lines:
        print("No characters found.")
        return

    headers = lines[0].split('\t')
    rows = [line.split('\t') for line in lines[1:]]

    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(val))

    # Format string
    fmt = " | ".join([f"{{:<{w}}}" for w in widths])
    separator = "-+-".join(["-" * w for w in widths])

    print(fmt.format(*headers))
    print(separator)
    for row in rows:
        print(fmt.format(*row))

if __name__ == "__main__":
    output = get_char_data()
    if output:
        print_table(output)
