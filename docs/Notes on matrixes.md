# Ossos

Osso -> ponto e vetor que dá a direção do osso
Cada osso tem um pai exceto o osso raiz -> o que dá a posição do corpo


# Movimentar ossos

Para calcular transformações é necessário usar diversas matrizes:

- Matriz modelo -> define uma transformação do osso relativa à raiz do cortpo; para calcular a matriz modelo de um osso multiplica-se todas as matrizes locais recursivamente até à raiz
- Matriz modelo inversa -> define a mesma transformação mas do ponto de vista do osso
- Matriz local -> define uma transformação do osso relativa ao pai desse osso

Para computar a matriz que descreve o movimento precisamos da:

- Matriz modelo inversa
- Matriz modelo destino (após a movimentação)


$MatrizModeloFinal = MatrizModeloFinalPai \times MatrizLocal \times MatrizAnimacao$

$MatrizTransformacao = MatrizModeloFinal \times MatrizModeloInversa$

