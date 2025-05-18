from lark import Lark, Transformer, v_args

grammar = """
start: signal intervals "."       -> sentence

signal: "+"                    -> plus_signal
      | "-"                    -> minus_signal

intervals: interval remaining_intervals -> intervals
remaining_intervals:          -> empty
                   | interval remaining_intervals -> remaining_intervals
interval: "[" NUMBER ";" NUMBER "]"    -> interval

%import common.NUMBER
%import common.WS_INLINE
%ignore WS_INLINE
"""

grammar2 = """
start: signal intervals "."

signal: "+"
      | "-"

intervals: interval remaining_intervals
remaining_intervals:
                   | interval remaining_intervals
interval: "[" NUMBER ";" NUMBER "]"

%import common.NUMBER
%import common.WS_INLINE
%ignore WS_INLINE
"""

class IntervalTransformer(Transformer):
    """
    Handles transformations and applies constraints to parsed intervals.

    Attributes:
        sentido (int): Indicates the current signal direction (+1 or -1).
        anterior (float): Tracks the end value of the previous interval.
        erro (bool): Flag indicating if a constraint was violated.
    """
    def __init__(self):
        self.sentido = 0
        self.anterior = float('-inf')
        self.erro = False
        self.dados = {
            "is_valid": True,
            "first": 0,
            "second": 0,
            "range": 0
        }

    @v_args(inline=True)
    def sentence(self, signal, intervals):
        """Returns the parsed intervals."""
        if self.erro:
            self.dados["is_valid"] = False
        return self.dados  


    @v_args(inline=True)
    def plus_signal(self):
        """Sets the signal direction to +1 (growing)."""
        self.sentido = 1
        print("Signal set to + (growing).")
        return self.sentido

    @v_args(inline=True)
    def minus_signal(self):
        """Sets the signal direction to -1 (decreasing)."""
        self.sentido = -1
        self.anterior = float('inf')
        print("Signal set to - (decreasing).")
        return self.sentido

    @v_args(inline=True)
    def interval(self, start, end):
        """
        Processes an interval and checks constraints based on signal direction.
        """
        start = int(start)
        end = int(end)    
        amplitude = abs(end - start)    

        if self.sentido == 1:
            if end <= start:
                print(f"Error: Constraint CC1 violated. End ({end}) must be greater than Start ({start}).")
                self.erro = True
            if start < self.anterior:
                print(f"Error: Constraint CC2 violated. Start ({start}) must be greater than or equal to the previous End ({self.anterior}).")
                self.erro = True
            if self.erro == False and self.dados['range'] < amplitude:
                self.dados['range'] = amplitude
                self.dados['first'] = start
                self.dados['second'] = end
        elif self.sentido == -1:
            if end >= start:
                print(f"Error: Constraint CC1 violated. End ({end}) must be less than Start ({start}).")
                self.erro = True
            if start > self.anterior:
                print(f"Error: Constraint CC2 violated. Start ({start}) must be less than or equal to the previous End ({self.anterior}).")
                self.erro = True
            if self.erro == False and self.dados['range'] < amplitude:
                self.dados['range'] = amplitude
                self.dados['first'] = start
                self.dados['second'] = end

        self.anterior = end
        return (start, end)

    def empty(self, _):
        """Represents an empty remaining interval."""
        return []

parser = Lark(grammar, parser='lalr', transformer=None)

def parse_input(input_text):
    """
    Parses the input text, applies transformations, and checks constraints.

    Args:
        input_text (str): The input string to parse.

    Returns:
        None
    """
    try:
        tree = parser.parse(input_text)
        transformer = IntervalTransformer()
        result = transformer.transform(tree)
        if transformer.erro:
            print("\nParsing failed: One or more constraints were violated.")
        else:
            print("\nParsing successful: All constraints satisfied.")
            print("Parsed intervals:", result)
    except Exception as e:
        print(f"\nParsing error: {e}")

if __name__ == "__main__":
    input_text = "+ [1;2] [3;5] [7;15] ."
    print("Input:", input_text)
    parse_input(input_text)

    input_text = "- [8;6] [6;4] [4;2] ."
    print("\nInput:", input_text)
    parse_input(input_text)

    input_text = "+ [1;2] ."
    print("\nInput:", input_text)
    parse_input(input_text)

    input_text = "- [1;3] [2;4] [5;2] ."
    print("\nInput:", input_text)
    parse_input(input_text)


"""
Input: + [1;3] [3;5] [6;8] .
sentence
  plus_signal
  intervals
    interval
      1
      3
    remaining_intervals
      interval
        3
        5
      remaining_intervals
        interval
          6
          8
        empty
"""

