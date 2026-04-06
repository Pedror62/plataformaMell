# backup_automatico.py
import subprocess
import datetime
import os
import sys
import traceback

def realizar_backup_automatico():
    """
    Função de backup automático - apenas o necessário
    """
    try:
        # Configurações do banco
        db_user = "intramell"
        db_password = "IntraMell!@#789"
        db_host = "10.200.10.62"
        db_name = "plataforma_mell"
        
        # Cria pasta de backups se não existir
        pasta_backup = "backups_automaticos"
        if not os.path.exists(pasta_backup):
            os.makedirs(pasta_backup)
        
        # Nome do arquivo com timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        nome_arquivo = f"AUTOBACKUP_{db_name}_{timestamp}.sql"
        caminho_completo = os.path.join(pasta_backup, nome_arquivo)
        
        # Caminho do mysqldump
        mysqldump_exe = r'"C:\Program Files\MariaDB 12.2\bin\mysqldump.exe"'
        
        # Comando de backup
        comando = f'{mysqldump_exe} -h {db_host} -u {db_user} -p"{db_password}" --ssl=0 {db_name} > "{caminho_completo}"'
        
        print(f"[{datetime.datetime.now()}] Iniciando backup...")
        
        # Executa o backup
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode == 0 and os.path.exists(caminho_completo):
            tamanho = os.path.getsize(caminho_completo) / (1024*1024)
            print(f"[{datetime.datetime.now()}] ✅ Backup OK: {nome_arquivo} ({tamanho:.2f} MB)")
            
            # Limpa backups antigos (mantém últimos 30)
            limpar_backups_antigos(pasta_backup, 30)
            
            return True, caminho_completo
        else:
            print(f"[{datetime.datetime.now()}] ❌ Erro: {resultado.stderr}")
            return False, resultado.stderr
            
    except Exception as e:
        print(f"[{datetime.datetime.now()}] ❌ Exceção: {e}")
        traceback.print_exc()
        return False, str(e)

def limpar_backups_antigos(pasta, manter=30):
    """Remove backups mais antigos que a quantidade especificada"""
    try:
        arquivos = []
        for arquivo in os.listdir(pasta):
            if arquivo.startswith('AUTOBACKUP_') and arquivo.endswith('.sql'):
                caminho = os.path.join(pasta, arquivo)
                arquivos.append((caminho, os.path.getmtime(caminho)))
        
        # Mantém os mais recentes
        arquivos.sort(key=lambda x: x[1], reverse=True)
        for caminho, _ in arquivos[manter:]:
            os.remove(caminho)
            print(f"[{datetime.datetime.now()}] Removido antigo: {os.path.basename(caminho)}")
    except Exception as e:
        print(f"Erro ao limpar: {e}")

def verificar_e_executar():
    """Verifica se já tem backup hoje antes de executar"""
    pasta_backup = "backups_automaticos"
    if not os.path.exists(pasta_backup):
        os.makedirs(pasta_backup)
    
    hoje = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Verifica se já existe backup de hoje
    for arquivo in os.listdir(pasta_backup):
        if arquivo.startswith('AUTOBACKUP_') and hoje in arquivo:
            print(f"[{datetime.datetime.now()}] Backup já existe: {arquivo}")
            return True, os.path.join(pasta_backup, arquivo)
    
    # Se não existe, faz backup
    return realizar_backup_automatico()

if __name__ == "__main__":
    sucesso, resultado = verificar_e_executar()
    if not sucesso:
        sys.exit(1)