# TPC2: Intervalos - Definição Sintática e Verificação Simples(lark)

Este código foi desenvolvido para analisar uma sequência de intervalos e verificar se os números dentro de cada intervalo seguem uma ordem específica de acordo com o sinal fornecido (`+` ou `-`). Esta gramática corresponde à gramática também utilizada no TPC1.

```
Considere o Terminal variável "num" (número decimal) e a seguinte Gramática independente
de Contexto (G) em que 'S' é o Axioma e '&' representa a string nula.
T  = { '.', ';', '[', ']', num }
NT = { S, Is, RI, I }
P = { p1: Sentence  : Signal Intervals '.'
         p6: Signal : '+'
parser.sentido = 1
         p7: Signal : '-'		
parser.sentido = -1
         p2: Intervals : Interval RemainingIntervals
         p3: RemainingIntervals : 
         p4: RemainingIntervals : Interval RemainingIntervals
         p5: Interval  : '[' num ':' num ']'   
		CC1:    p[4] > p[2]  &
		CC2:    p[2] >= parser.anterior
		parser.anterior = p[4]
		parser.erro = not (CC1) or not (CC2)

 }

```
 A verificação ocorre de forma simples, extraindo os números dos intervalos e garantindo que estejam em ordem crescente ou decrescente, dependendo do sinal.

## Descrição do Código

O código contém duas partes principais:

### 1. **Definição Sintática (Gramática)**

A gramática utilizada define a estrutura para os intervalos que são passados como entradas. A estrutura é simples e inclui os seguintes elementos:

- **Sinal** (`+` ou `-`): Indica a ordem dos números (crescente ou decrescente).
- **Intervalos**: Um ou mais intervalos, que são definidos como um par de números entre colchetes `[num1; num2]`.
- **Ponto final** (`.`): Indica o fim da entrada.

Exemplo de entradas válidas:

- `+ [1;2][3;4][5;6].`
- `- [5;2][2;0].`

A gramática é representada no formato Lark, um analisador de sintaxe, e descreve as regras para reconhecer essas estruturas de intervalos e sinais.

#### Alterações Importantes na Gramática:

- **Uso de `intervals+`**: 
    - A parte `intervals : interval+` significa que **pelo menos um intervalo** deve ser fornecido. O operador `+` após `interval` indica que um ou mais intervalos podem ser presentes.
    - Essa modificação permite que a entrada tenha múltiplos intervalos. Por exemplo, a entrada `+ [1;2][3;4][5;6].` é válida, pois contém três intervalos, enquanto `+ [1;2].` também é válida com apenas um intervalo.
    - Sem o `+`, a gramática só aceitaria um único intervalo.

    A definição completa da regra para `intervals` e `interval` é a seguinte:

    ```text
    intervals : interval+
    interval : PA NUM COMMA NUM PF
    ```

    Isso permite que a entrada seja composta por múltiplos intervalos de forma sequencial e permite simplificar a gramática anterior, uma vez que reduzimos o número de regras mantendo o mesmo signficado. 



### 2. **Verificação de Ordem**

A função `verificar_ordem` tem como objetivo garantir que os números dentro dos intervalos estejam ordenados de acordo com o sinal especificado:

- Se o sinal for **`+`**, os números devem estar **estritamente crescentes**.
- Se o sinal for **`-`**, os números devem estar **estritamente decrescentes**.

A função percorre todos os intervalos extraindo os números, organiza-os de acordo com o sinal e compara com a ordem esperada. Se os números não estiverem na ordem correta, a função retornará um erro semântico indicando que a entrada está incorreta. Caso contrário, ela indicará que a entrada está correta.

### 3. **Exemplos de Entradas e Saídas**

Exemplos de entradas e as saídas esperadas:

#### Exemplos de entradas:
- `+ [1;2][3;4][5;6].`
- `+ [3;1].`
- `- [5;2][2;0].`
- `- [5;2][1;3].`
- `- [6;5][6,1].`

#### Saídas esperadas:
- **Para `+ [1;2][3;4][5;6].`**
    - **Saída**: `"Números ordenados"`, `"Frase correta"`

- **Para `+ [3;1].`**
    - **Saída**: `"Erro: Números fora de ordem para '+'."`, `"Erro semântico"`

- **Para `- [5;2][2;0].`**
    - **Saída**: `"Números ordenados"`, `"Frase correta"`

- **Para `- [5;2][1;3].`**
    - **Saída**: `"Erro: Números fora de ordem para '-'."`, `"Erro semântico"`

#### Exemplo de saída no terminal:
```text
Verificando: + [1;2][3;4][5;6].
Números extraídos: [1, 2, 3, 4, 5, 6]
Números ordenados
Frase correta

Verificando: + [3;1].
Números extraídos: [3, 1]
Erro: Números fora de ordem para '+'.
Erro semântico
