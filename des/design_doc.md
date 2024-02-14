# Game design doc


# Estilo

Roguelite | Metroidvania | Dungeon Crawler | Multiplayer | Fighting.

# Ideia base

Mapa proceduralmente gerado, com formato de salas predefinidas (para ajudar na learning curve).

O jogo é de luta contra um oponente.

Ambos começam o jogo totalmente desarmados e desprotegidos tendo, assim, que ganhar itens e ficando mais fortes farmando inimigos (minions) e salteando baús ou cofres.

Os jogadores têm que lutar até à morte e o que vencer ganha um ponto.

**Melhor de 3 rondas.**

## Outras ideias

### Ideia 1 - conhecimento do mapa

> De ronda para ronda o jogador fica com a informação sobre as salas que explorou e a localização dos baús/cofres que loteou.


### Ideia 2 - desenvolvimento das batalhas

> Os jogadores têm que explorar a dungeon durante um dia inteiro e a batalha será à meia noite em ponto (in game time *5min*)
>
> Caso os jogadores se encontrem no mapa podem lutar até à morte e o que vencer ganha 1 ponto.

---

# Mecânicas

## Core mechanics

### Crafting

Encontra-se várias partes de armas que se podem juntar para fazer cada uma das armas mencinadas acima

Cada parte tem uma raridade diferente e uma habilidade

As armas também poderão levar outras modificações para ficarem mais fortes


## General mechanics

### Luta

- Golpes unarmerd
- Golpes com diversas armas de melee
- Projeteis

### Armas

- Arcos
- Espadas
- Soqueiras
- Machados

![modelo das armas](modelo_das_armas.png)


#### Espada

Terá um combo de ataques médios que atingirá o inimigo dando knockback, o último ataque dará mais knockback

#### Arco

Lançará setas durante a animação

#### Soqueiras

Terá um combo de ataques rápidos, mas que causam pouco dano



### Ataques

As armas são liagadas aos ossos dos jogadores.

Quando um jogador atacar, uma animação vai ser reproduzida e a arma, que está fixa ao osso, vai acompanhar o movimento do mesmo.

Assim que a hitbox da arma colidir com a bounding box de um inimigo **durante a animação de ataque** o inimigo toma dano.

![ataque](modelo_de_ataque.png)


O objetivo é que apenas durante a animação de ataque os inimigos possam sofrer dano

#### Atordoamento

Cada ataque terá um valor de knockback que é aplicado ao inimigo assim que sofre dano

Quando o knockback é aplicado o inimigo fica atordoado por **algum tempo**, dependendo do ataque

Este tempo é medido em frames e impede que o inimigo se mova


---

# Looting

Em cada sala aparecerão baús que contém upgrades e/ou partes de armas

Os inimigos também têm uma chance de dropar estes itens



# Perks

Antes de cada jogo, o jogador escolhe 3 perks que lhe darão certas vantagens ou habilidades durante o jogo

**TBD**



---


# Tecnologia, Otimização e Algoritmos

## Mapa

O mapa é gerado através do algoritmo Wave Function Collapse que pega num conjunto de regras sobre como as diferentes salas se conectam entre si e gera um mapa com o tamanho desejado

### Salas

Começar-se-à numa sala comum (principal) e os 2 jogadores ficam sparados (podem haver várias variações)

**TAMANHO**: 30*17 tiles de 32x32


![salas](salas.png)


#### Estruturas e diferenças

Vão haver várias estruturas para cada bioma ou "nível"


#### Camadas

Para desenhar as salas, diferentes camadas precisam de ser tidas em conta, já que são diferentes camadas da pipeline de renderização.


- POIs
- colliders
- detalhes2
- blocos
- detalhes1
- parallax
- background


## Minions (inimigos)

Vão haver vários tipos de inimigos para farmar


### IA

Os mais comuns:
- vão seguir a direção do jogador assim que o virem
- enquanto não o virem andam para trás e para a frente na sua plataforma ou ficam quietos (dependendo do tipo de inimigo)

