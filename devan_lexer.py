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

        # Regex patterns
        self.patterns = {
            "STRING": r'"[^"]*"|\'[^\']*\'',
            "NUMBER": r'\d+',
            # Accepts Devanagari (0900–097F) + Latin identifiers
            "IDENTIFIER": r'[a-zA-Z_\u0900-\u097F][a-zA-Z0-9_\u0900-\u097F]*',
            "SYMBOL": r'[^\w\s]'
        }

    def tokenize(self):
        lines = self.code.splitlines()

        for line_num, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Skip empty/comment lines

            # Extract strings first
            for match in re.finditer(self.patterns["STRING"], line):
                self.tokens.append(Token("STRING", match.group(), line_num))
                line = line.replace(match.group(), " ", 1)

            # Tokenize remaining words/symbols
            words = re.findall(r'[^\s]+', line)
            for word in words:
                if re.fullmatch(self.patterns["NUMBER"], word):
                    self.tokens.append(Token("NUMBER", word, line_num))
                elif re.fullmatch(self.patterns["IDENTIFIER"], word):
                    self.tokens.append(Token("IDENTIFIER", word, line_num))
                elif re.fullmatch(self.patterns["SYMBOL"], word):
                    self.tokens.append(Token("SYMBOL", word, line_num))
                else:
                    self.tokens.append(Token("UNKNOWN", word, line_num))

        return self.tokens

# Example usage
if __name__ == "__main__":
    code = """
    आयातः "गणकसंग्रहः"
    मान = गणकसंग्रहः.sqrt(१६)
    लेखय "उत्तर:", मान
    # यह एक टिप्पणी है
    """
    lexer = DevanLexer(code)
    for token in lexer.tokenize():
        print(token)
