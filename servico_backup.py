import subprocess
import datetime
import os
datetime.datetime.now()  # ✅ CORRETO
def realizar_backup_automatico():
    # Configurações
    db_user = "intramell"
    db_password = "IntraMell!@#789"
    db_host = "10.200.10.62"
    db_name = "plataforma_mell"
    
    # Cria pasta de backups se não existir
    pasta_backup = "backups_automaticos"
    if not os.path.exists(pasta_backup):
        os.makedirs(pasta_backup)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    nome_arquivo = f"AUTOBACKUP_{db_name}_{timestamp}.sql"
    caminho_completo = os.path.join(pasta_backup, nome_arquivo)
    
    # Caminho do MariaDB
    mysqldump_exe = r'"C:\Program Files\MariaDB 12.2\bin\mysqldump.exe"'
    
    comando = f'{mysqldump_exe} -h {db_host} -u {db_user} -p"{db_password}" --ssl=0 {db_name} > "{caminho_completo}"'
    
    print(f"[{datetime.datetime.now()}] Iniciando backup...")
    subprocess.run(comando, shell=True)
    print(f"[{datetime.datetime.now()}] Backup concluído: {nome_arquivo}")
    print(f"📍 Local: {caminho_completo}")

if __name__ == "__main__":
    realizar_backup_automatico()