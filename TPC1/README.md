# Resumo dos Ficheiros

## Ficheiro 1: Analisador Léxico(TPC1-lex)

Este ficheiro define o analisador léxico usando a biblioteca `ply.lex`. O objetivo principal é identificar e classificar tokens.

### Tokens Definidos

- **MENOS** (`-`): Representa o sinal negativo.
- **MAIS** (`+`): Representa o sinal positivo.
- **PA** (`[`) : Abre um intervalo.
- **PF** (`]`) : Fecha um intervalo.
- **COMMA** (`,` ou `;`): Separador de valores.
- **POINT** (`.`): Ponto final de uma expressão.
- **NUM** (números inteiros): Representa números inteiros, podendo ser positivos ou negativos.

### Funções

- **t_MAIS**: Expressão regular para reconhecer o sinal `+`.
- **t_MENOS**: Expressão regular para reconhecer o sinal `-`.
- **t_PA**: Expressão regular para reconhecer o símbolo de abertura de intervalo `[` (abre um intervalo).
- **t_PF**: Expressão regular para reconhecer o símbolo de fechamento de intervalo `]` (fecha um intervalo).
- **t_COMMA**: Expressão regular para reconhecer o símbolo de separação de valores (`,` ou `;`).
- **t_POINT**: Expressão regular para reconhecer o ponto final `.`.
- **t_NUM**: Reconhece números inteiros, podendo ser positivos ou negativos.
- **t_NEWLINE**: Atualiza o contador de linha para quando houver quebras de linha.
- **t_error**: Função que trata os erros lexicais, imprimindo uma mensagem de erro para caracteres ilegais.
- **t_ignore**: Ignora espaços e tabulações.

### Como o Lexer Funciona

O lexer usa expressões regulares para identificar os diferentes tokens no texto de entrada. Ele converte a entrada em tokens, que são usados pelo parser para análise sintática.

---

## Ficheiro 2: Analisador Sintático(TPC1_sint.py)

Este ficheiro define o analisador sintático (ou *parser*) utilizando a biblioteca `ply.yacc` para analisar expressões envolvendo intervalos e sinais.

### Produções Definidas

#### Sentença

1. **Sentence 1**: Quando a sentença começa com um sinal negativo (`-`), seguida por uma lista de intervalos, e termina com um ponto (`.`).
   - A função **p_Sentence_1** verifica se os intervalos estão ordenados em ordem decrescente.
2. **Sentence 2**: Quando a sentença começa com um sinal positivo (`+`), seguida por uma lista de intervalos, e termina com um ponto (`.`).
   - A função **p_Sentence_2** verifica se os intervalos estão ordenados em ordem crescente.

#### Sinal

- **SignalPos**: Define o sinal positivo (`+`).
- **SignalNeg**: Define o sinal negativo (`-`).

#### Intervalos

- **Intervals**: Define a sequência de intervalos.
- **RemainingIntervals**: Define a continuação dos intervalos, que pode ser vazia ou composta por mais intervalos.
- **Interval**: Define o formato de um intervalo como `[NUM, NUM]`, onde `NUM` são números inteiros.

### Funções do Parser

- **p_Sentence_1**: Processa uma sentença com o sinal negativo e verifica a ordem dos intervalos.
- **p_Sentence_2**: Processa uma sentença com o sinal positivo e verifica a ordem dos intervalos.
- **p_SignalPos**: Define a produção para o sinal positivo (`+`).
- **p_SignalNeg**: Define a produção para o sinal negativo (`-`).
- **p_Intervals**: Concatena um intervalo com os intervalos seguintes.
- **p_RemainingIntervals**: Define a continuação de intervalos ou termina a lista de intervalos.
- **p_Interval**: Define o formato de um intervalo como uma lista com dois números inteiros.
- **p_error**: Lida com erros sintáticos e imprime uma mensagem de erro quando há um erro no input.

### Como o Parser Funciona

O parser analisa uma cadeia de tokens gerados pelo lexer. Ele usa as produções definidas para construir uma árvore sintática e verificar a estrutura da expressão. O parser verifica a ordem dos intervalos com base no sinal de entrada (`+` ou `-`).

---

### Execução Interativa

- O parser é executado em um loop interativo que permite ao utilizador inserir entradas até que o comando `'s'` seja dado para sair.
- Quando a entrada é dada, o parser analisa a sentença e imprime se os intervalos estão "ordenados" ou "desordenados", conforme a lógica definida.

---

Este resumo proporciona uma visão geral do funcionamento e da estrutura dos dois ficheiros, com ênfase nos tokens definidos, nas produções sintáticas e nas funções principais do lexer e do parser.
