# devan_lexer.py

import re

class Token:
    def __init__(self, type_, value, line_num):
        self.type = type_
        self.value = value
        self.line_num = line_num

    def __repr__(self):
        return f"{self.type}({self.value}) at line {self.line_num}"

class DevanLexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        lines = self.code.splitlines()
        for line_num, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Basic token patterns (can be expanded later)
            string_match = re.findall(r'"[^"]*"|\'[^\']*\'', line)
            for s in string_match:
                self.tokens.append(Token("STRING", s, line_num))
                line = line.replace(s, "", 1)

            words = line.split()
            for word in words:
                if word.isdigit():
                    self.tokens.append(Token("NUMBER", word, line_num))
                elif re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", word):
                    self.tokens.append(Token("IDENTIFIER", word, line_num))
                elif re.match(r"[^\w\s]", word):
                    self.tokens.append(Token("SYMBOL", word, line_num))
                else:
                    self.tokens.append(Token("UNKNOWN", word, line_num))

        return self.tokens

# Example usage (for dev/testing)
if __name__ == "__main__":
    code = """
    आयातः "गणकसंग्रहः"
    मान = गणकसंग्रहः.sqrt(१६)
    लेखय "उत्तर:", मान
    """
    lexer = DevanLexer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
