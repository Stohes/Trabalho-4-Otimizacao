import math
import operator
import random
import cProfile

    

def crialistaDasCidadesDoTXT(arquivo="data.txt"):
    dicionarioDasCidades = {}
    
    with open(arquivo) as file:
        for linha in file.readlines():
            try:
                
                linhaSeparada = linha.rsplit()
                coordenadas = [float(linhaSeparada[0]), float(linhaSeparada[1])]
                cidade = linhaSeparada[2]
                dicionarioDasCidades.update({cidade: coordenadas})
                
            except Exception as e:
                pass
                
    return dicionarioDasCidades

listaDasCidadesDoTXT = crialistaDasCidadesDoTXT()

def geraCaminho(quantiaDeCidades):
    caminhoEmbaralhado = [f"Cid{cidade}" for cidade in range(2, quantiaDeCidades + 2)]
    random.shuffle(caminhoEmbaralhado)
    caminhoEmbaralhado.insert(0, "Cid1")
    caminhoEmbaralhado.append("Cid1")
    return caminhoEmbaralhado

def geraPopulacao(tamanhoDaPopulacao, quantiaDeCidadesNaPopulacao):
    return [geraCaminho(quantiaDeCidadesNaPopulacao) for _ in range(tamanhoDaPopulacao)]

def valorDoCaminho(caminho, listaDasCidadesDoTXT=listaDasCidadesDoTXT):
    
    distanciaTotal = 0

    for i in range(0, len(caminho) - 1):
        cidade1 = caminho[i]
        cidade2 = caminho[i + 1]
        
        distancia = math.dist(listaDasCidadesDoTXT.get(cidade1), listaDasCidadesDoTXT.get(cidade2))
        
        distanciaTotal += distancia
        
    return 1 / distanciaTotal

def valoresDosCaminhosDaPopulacao(populacao):
    dicValoresDosCaminhosDaPopulacao = {}
    
    for i in range(len(populacao)):
        dicValoresDosCaminhosDaPopulacao[i] = valorDoCaminho(populacao[i])
        
    return sorted(dicValoresDosCaminhosDaPopulacao.items(), key=operator.itemgetter(1), reverse=True)
        
def selecionaPais(populacao: list):
    valoresDasCidades = valoresDosCaminhosDaPopulacao(populacao)
    
    pesos = [0 for _ in range(len(populacao))]
    for i in range(len(valoresDasCidades)):
        pesos[valoresDasCidades[i][0]] = valoresDasCidades[i][1]
    
    paisEscolhidos = random.choices(population=populacao, weights=pesos, k=2)
    
    return paisEscolhidos

def elitismo(populacao):
    valoresDasCidades = valoresDosCaminhosDaPopulacao(populacao)
    
    melhor = populacao[valoresDasCidades[0][0]]
    segundoMelhor = populacao[valoresDasCidades[1][0]]
    
    elites = [melhor, segundoMelhor]
    return elites

def caminhosQueContinuamNaProximaGeracao(populacao):
    caminhos = elitismo(populacao) + selecionaPais(populacao)
    return caminhos

def juntaOsDoisPais(pai1: list, pai2: list):
    filho = []
    filhoParte1 = []
    filhoParte2 = []

    geneA = int(random.random() * len(pai1))
    geneB = int(random.random() * len(pai1))

    inicioDoGene = min(geneA, geneB)
    fimDoGene = max(geneA, geneB)

    for i in range(inicioDoGene, fimDoGene):
        filhoParte1.append(pai1[i])

    filhoParte2 = [cidade for cidade in pai2 if cidade not in filhoParte1]

    # filho = filhoParte2[:inicioDoGene] + filhoParte1 + filhoParte2[inicioDoGene:]
    
    filho = [cidade for cidade in pai2 if cidade not in filhoParte2]

    filho[inicioDoGene:inicioDoGene] = filhoParte2

    return filho

def juntaOsDoisPaisPopulacao(populacao):
    filhos = []
    
    for i in range((len(populacao) - 4)):
        pais = selecionaPais(populacao)
        filho = juntaOsDoisPais(pais[0], pais[1])
        filhos.append(filho)
        
    return filhos

def mutacao(caminho):
    probabilidade = random.randint(1, 100)
    
    if probabilidade > 90:
        trocarEm = [random.randint(1, len(caminho) - 2) for _ in range(2)]

        caminho[trocarEm[0]], caminho[trocarEm[1]] = caminho[trocarEm[1]], caminho[trocarEm[0]]

    return caminho

def mutaPopulacao(populacao):
    populacaoMutada = []
    
    for caminho in populacao:
        populacaoMutada.append(mutacao(caminho))
        
    return populacaoMutada

def proximaGeracao(geracaoAtual):
    
    varCaminhosQueContinuamNaProximaGeracao = caminhosQueContinuamNaProximaGeracao(geracaoAtual)
    
    filhos = juntaOsDoisPaisPopulacao(geracaoAtual)
    populacaoMutada = mutaPopulacao(filhos)
    
    # varProximaGeracao.append(varCaminhosQueContinuamNaProximaGeracao)
    # varProximaGeracao.append(populacaoMutada)
    
    varProximaGeracao = varCaminhosQueContinuamNaProximaGeracao + populacaoMutada
    
    return varProximaGeracao

def evolucao(tamanhoDaPopulacao, quantiaDeCidadesNaPopulacao, quantiaDeGeracoes, listaDasCidadesDoTXT=listaDasCidadesDoTXT):
    populacao = geraPopulacao(tamanhoDaPopulacao, quantiaDeCidadesNaPopulacao)

    distanciaInicial = 1 / valoresDosCaminhosDaPopulacao(populacao)[0][1]
    print(f"Distancia Inicial: {distanciaInicial}")

    melhorCaminho = distanciaInicial
    
    
    for i in range(1, quantiaDeGeracoes):
        distanciaAtual = 1 / valoresDosCaminhosDaPopulacao(populacao)[0][1]
        
        if distanciaAtual < melhorCaminho:
            melhorCaminho = distanciaAtual
            print(f"Novo Melhor Caminho: {melhorCaminho}")
        # print(f"Geracao Atual: {i} Distancia Atual: {distanciaAtual}")
        
        populacao = proximaGeracao(populacao)
        
    print(f"Melhor Caminho Encontrado: {melhorCaminho}")
    
    # melhorCaminhoString = populacao[valoresDosCaminhosDaPopulacao(populacao)[0][0]]
    # print(f"Melhor Caminho: {melhorCaminhoString}")
        
        
# evolucao(6, 2007, 10000) melhores parametros ate entao
evolucao(6, 2007, 100000)

