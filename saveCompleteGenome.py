import pandas as pd
import os
import subprocess

def toDict(file):
    
    with open(file, "r") as f:
        data = f.read()
    
    data = data.split(">")
    
    dicio = {}
    
    for linha in data:
        if linha:
            sp = linha.split('\n')
            dicio[sp[0]] = sp[1]
    
    return dicio

def readKeys(file):
    data = pd.read_csv(f"{file}/complete_genomes.tsv", sep="\t")
    keys = data["contig_id"]
    
    return keys

def saveFile(dicio, keys, name):
    string = ""
    for key in keys:
        genome = dicio[key]
        string += f">{key}\n{genome}\n"
    string = string[:-1]

    with open(name, "w+") as f:
        f.write(string)
        
def splitGenomes(dicio, keys, folder):
    folderSplit = folder.split(".")
    name = f"{folderSplit[0]}_"
    n = len(keys)
    i = 1
    for key in keys:
        print(f"Saving ({i}/{n})")
        genome = dicio[key]
        line = f">{key}\n{genome}"
        with open(f"{folder}/{name}{key}.fasta", "w+") as f:
            f.write(line)
        i += 1        

def runBlast():
   
    for i in range(1, 60):
        print(f"Analysing Meta_{i}")
        fastaFile = f"Meta_{i}.onlyPhages.fasta" 
        fastaFolder = f"Meta_{i}.onlyPhages.fasta.checkv"
        
        if os.path.isfile(fastaFile):
            keys = readKeys(fastaFolder)
            for key in keys:
                print(f"Running Blast on: {key}")
                virusFile = f"Meta_{i}_{key}.fasta"
                result = subprocess.run(["blastn", "-query", f"Meta_{i}.onlyPhages.fasta.checkv/Meta_{i}_{key}.fasta", "-db", "library.fna", "-evalue", "1e-6", "-num_threads", "10", "-out", f"Meta_{i}.onlyPhages.fasta.checkv/Blast_{key}.txt"], capture_output=True, text=True)

                print(result.stdout)

def pipeLine():
    for i in range(1, 60):
        fastaFile = f"Meta_{i}.onlyPhages.fasta"
        if os.path.isfile(fastaFile):
            checkv = f"Meta_{i}.onlyPhages.fasta.checkv"
            saveName = f"Meta_{i}.onlyPhages.complete.fasta"
            dicio = toDict(fastaFile)
            
            keys = readKeys(checkv)
            
            saveFile(dicio, keys, saveName)
            splitGenomes(dicio, keys, checkv)
# pipeLine()
runBlast()
