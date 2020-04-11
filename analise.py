
import argparse
import csv
import requests
import matplotlib.pyplot as plt
import numpy as np

def dados(JUSTICA):

    if JUSTICA == 'JFPE':
        link='https://creta.jfpe.jus.br/cretape/lista_julgamento.txt'
    elif JUSTICA == 'JFAL':
        link='https://jef.jfal.jus.br/cretaal/lista_julgamento.txt'
    elif JUSTICA == 'JFRN':
        link='https://cretarn.jfrn.jus.br/cretarn/lista_julgamento.txt'
    elif JUSTICA == 'JFSE':
        link='https://wwws.jfse.jus.br/cretase/lista_julgamento.txt'
    elif JUSTICA == 'JFCE':
        link='http://wwws.jfce.gov.br/cretace/lista_julgamento.txt'
    elif JUSTICA == 'JFPB':
        link='https://jefvirtual.jfpb.jus.br/cretapb/lista_julgamento.txt'

    resposta = requests.get(link)
    arquivo = open("dados.txt", "w")
    arquivo.write(resposta.text)
    arquivo.close()

    saida = open('dados.csv', 'w') # arquivo de saida
    for x in open('dados.txt', 'r').readlines()[2:]: # arquivo de entrada
       saida.write(x.replace('\n',';\n'))
    
    Numero_Processo=[]
    Cod_CNJ=[]
    SJ=[]
    Cod_Orgao_Julgador=[]
    Orgao_Julgador=[]
    Data_Distribuicao=[]
    Data_Conclusao=[]
    Prioridade=[]
    
    with open('dados.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        for row in readCSV:
        	Numero_Processo.append(row[0])
        	Cod_CNJ.append(row[1])
        	SJ.append(row[2])
        	Cod_Orgao_Julgador.append(row[3])
        	Orgao_Julgador.append(row[4])
        	Data_Distribuicao.append(row[5])
        	Data_Conclusao.append(row[6])
        	Prioridade.append(row[7])
    
    
    Orgao_Julgador_organizado = sorted(set(Orgao_Julgador))
    Cod_CNJ_organizado = sorted(set(Cod_CNJ))
    Cod_Orgao_Julgador_organizado = sorted(set(Cod_Orgao_Julgador))
    
    sizes = []
    labels = []
    explode = []
    processo_por_codigo = {}
    for cod in range(len(Orgao_Julgador_organizado)):
        processo_por_codigo[cod] = []
        for numero in range(len(Numero_Processo)):
            linha = Numero_Processo[numero]+" "+Cod_CNJ[numero]+" "+SJ[numero]+" "+Cod_Orgao_Julgador[numero]+" "+Orgao_Julgador[numero]
            if Orgao_Julgador_organizado[cod] in linha:
                processo_por_codigo[cod].append(Numero_Processo[numero])
        print("A QUANTIDADE DE PROCESSOS: {0} POR ORGAO JULGADOR: {1} ".format(len(processo_por_codigo[cod]),Orgao_Julgador_organizado[cod]))
        sizes.append(len(processo_por_codigo[cod]))
        labels.append(Orgao_Julgador_organizado[cod])
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True)
    ax1.axis('equal')
    ax1.set(title='Quantidade de processos por orgão julgador')
    fig1.savefig('Numeros.png', dpi=90, figsize=(30, 30))
    fig1.savefig('Numeros.pdf')
    plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--justica', type=str, help="grafico de processos",choices=['JFPE','JFAL','JFPB','JFCE','JFRN','JFSE'])

    args = parser.parse_args()
    if args.justica != None:
        print(args.justica)
        dados(args.justica)
    else:
        print("python analise.py --help")

if __name__ == '__main__':
    main()    
