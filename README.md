# Simulador-de-algoritmos-de-substituicao-de-paginas-na-memoria

Diferentes algoritmos de substituição de página podem ser empregados para escolher qual página deve ser substituída da memória. 
O objetivo deste trabalho é comparar o desempenho dos algoritmos FIFO, Menos Recentemente Usada (MRU), 
Não usada frequentemente (NUF) com relação ao algoritmo ótimo em termos de número de troca de páginas.

O programa receberá como entrada um arquivo contendo múltiplas linhas, sendo uma linha referente a cada caso de teste. 
O formato da linha é o seguinte

Número de molduras de página na memória|número de páginas do processo|sequência em que as páginas são acessadas

Exemplo:

4|8|1 2 2 2 3 4 3 4 5 5 6 1 3 2 6 7 7 7 8

Esta linha indica que a memória possui 4 molduras, o projeto tem 8 páginas e são referenciadas na ordem 1 2 2 2 3 4 ...

Para cada caso de teste, o programa deverá produzir como saída uma linha contendo:

Número de trocas de página no algoritmo FIFO|Número de trocas de página no algoritmo MRU|Número de trocas de página no algoritmo NUF|Número de trocas de página no algoritmo ótimo|nome do algoritmo com desempenho mais próximo do ótimo

Além do programa, os alunos deverão produzir um pequeno relatório (3 páginas no máximo) comentando sobre o desempenho observado dos algoritmos. 
Por exemplo, como a quantidade de molduras afeta o desempenho dos algoritmos? como a quantidade de páginas afeta o desempenho dos algoritmos? 
Existe alguma relação entre o número de molduras e o número de páginas que afeta o desempenho dos algoritmos? 
Como a ordem de referenciamento das páginas afeta o desempenho dos algoritmos? As explicações devem ser embasadas com exemplos.
