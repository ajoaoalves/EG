
# Explicação do Código: Analisador de Intervalos

## Introdução

Este script em Python utiliza a biblioteca `Lark` para realizar a análise e validação de intervalos numéricos. Ele aceita entradas com intervalos crescentes (`+`) ou decrescentes (`-`), verificando se as restrições impostas são atendidas.

## Estrutura do Código

### 1. Gramática (Grammar)

A gramática define a estrutura das entradas que o parser deve analisar. Ela espera um sinal (`+` ou `-`), seguido por intervalos numéricos entre colchetes, com a seguinte estrutura:

```text
start: signal intervals "."       -> sentence
signal: "+"                    -> plus_signal
      | "-"                    -> minus_signal
intervals: interval remaining_intervals -> intervals
remaining_intervals:          -> empty
                   | interval remaining_intervals -> remaining_intervals
interval: "[" NUMBER ";" NUMBER "]"    -> interval
```

### 2. Classe `IntervalTransformer`

A classe `IntervalTransformer` valida os intervalos com base nas seguintes restrições:
- Para intervalos crescentes (`+`), o final de cada intervalo deve ser maior que o início e o início deve ser maior ou igual ao final do intervalo anterior.
- Para intervalos decrescentes (`-`), o final de cada intervalo deve ser menor que o início e o início deve ser menor ou igual ao final do intervalo anterior.

### 3. Função `parse_input`

Esta função recebe uma string de entrada e utiliza o parser `Lark` para analisar e validar os intervalos. Se ocorrer algum erro, ele será indicado na saída.

### 4. Exemplo de Execução

- **Entrada 1**: "+ [1;2] [3;5] [7;15] ."
  - Resultado: 
Signal set to + (growing).

Parsing successful: All constraints satisfied.
Parsed intervals: {'is_valid': True, 'first': 7, 'second': 15, 'range': 8}

- **Entrada 2**: "- [8;6] [6;4] [4;2] ."
  - Resultado: 
  Input: - [8;6] [6;4] [4;2] .
Signal set to - (decreasing).

Parsing successful: All constraints satisfied.
Parsed intervals: {'is_valid': True, 'first': 8, 'second': 6, 'range': 2}

## Conclusão

O código fornece uma solução robusta para a validação de intervalos numéricos com base nas direções crescente e decrescente. Ele emite mensagens claras de erro quando as restrições não são atendidas, permitindo uma fácil depuração.