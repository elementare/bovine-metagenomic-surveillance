import subprocess
import os

# Defina o diretório onde estão os arquivos
diretorio = "/home/llemos/metagenomicDataIP2/inputKraken"

# Construa os caminhos completos para os arquivos
for c in range(1, 60):
    db = os.path.join(diretorio, "kraken2_viral_db")
    relatorio = os.path.join(diretorio, f"Meta_{c}.report")
    input1 = os.path.join(diretorio, f"Meta_{c}_1.fq.filtered")
    input2 = os.path.join(diretorio, f"Meta_{c}_2.fq.filtered")
    saida = os.path.join(diretorio, f"Meta_{c}.kraken")

    # Construa o comando completo
    comando = f"kraken2 --db {db} --report {relatorio} --paired {input1} {input2} -t 40 > {saida}"

    # Execute o comando
    subprocess.run(comando, shell=True)



