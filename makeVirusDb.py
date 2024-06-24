import pandas as pd
import glob
import sys

from ncbi.datasets import GenomeApi
from ncbi.datasets.openapi import ApiException

# Initialize API client and genome API

genome_api = GenomeApi()


def getGenome(base_path, accession_id, taxon_id = None ):
    try:
        # Download genome data for the specified taxon ID
        # The download is saved as a zip file
        # You can specify the file format (e.g., fasta) and the assembly source (e.g., refseq, genbank)
        download = genome_api.download_assembly_package_post(
            v1_assembly_dataset_request= { "accessions": accession_id},
            _preload_content=False,
        )

        # Save the downloaded file
        print("Trying to save the file")
        filename = f'genome_teste.zip'
        with open(filename, 'wb') as f:
            f.write(download.data)
        print(f'Download completed: {filename}')

    except ApiException as e:
        print(f"Exception when calling GenomeApi-> download_assembly_package: {e}")
    
def getUsefulData(name, sep="\t"):
    data = pd.read_csv(name, sep=sep)
    
    return data[["assembly_accession", "taxid", "organism_name"]]

def makeDB(data, path_ncbi_dbs, path_db_save):
    tamanho_data = len(data)
    for i in range(tamanho_data):
        assembly, taxid = data[["assembly_accession", "taxid"]].iloc[i]

        files = glob.glob1(f'{path_ncbi_dbs}/{assembly}', f'{assembly}*.fna')

        for file in files:
            # print(f"Entrei no glob, filename: {file}")
            with open(f"{path_ncbi_dbs}/{assembly}/{file}", "r") as f:
                genome = f.read()
            
            try:
                index = genome.index(".")+2
            except:
                print(f"I can't find the . substring: {genome[:50]}\nAssembly: {assembly}")
                with open(f"{path_db_save}/erros.txt", "a+") as f:
                    f.write(f"Row: {i} | Assembly: {assembly}\n")
            else:
                genome = f"{genome[:index]}|kraken:taxid|{str(taxid)}{genome[index:]}"
                
                with open(f"{path_db_save}/{file}", "w") as f:           
                    f.write(genome)

        if i % 100 == 0: print(f"Modified {i}/{tamanho_data}")
data = getUsefulData("/home/carlos23001/IP/Dados/custom_db/assembly_summary.txt")


# a = data.where(data=="GCA_000847585.1").dropna(how='all').dropna(axis=1)
# print(a.index)
# print(a.columns)
makeDB(data, "/home/carlos23001/IP/Dados/custom_db/ncbi_dataset_modified/data", "/home/carlos23001/IP/Dados/custom_db/genomes_modified")


#getGenome("teste", data["assembly_accession"].tolist())


    