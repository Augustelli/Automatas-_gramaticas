from enum import Enum


class TokenType(Enum):
    ID = 0
    PLUS = 1
    MINUS = 2
    MOD = 3
    LPAREN = 4
    RPAREN = 5
    EOF = 6


class Token:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value


def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isdigit():
            num = char
            while i + 1 < len(expression) and expression[i + 1].isdigit():
                num += expression[i + 1]
                i += 1
            tokens.append(Token(TokenType.ID, int(num)))
        elif char == '+':
            tokens.append(Token(TokenType.PLUS))
        elif char == '-':
            tokens.append(Token(TokenType.MINUS))
        elif char == '%':
            tokens.append(Token(TokenType.MOD10))
        elif char == '(':
            tokens.append(Token(TokenType.LPAREN))
        elif char == ')':
            tokens.append(Token(TokenType.RPAREN))
        i += 1
    tokens.append(Token(TokenType.EOF))
    return tokens


def parse_E(tokens):
    left_node = parse_T(tokens)
    return parse_E_prime(tokens, left_node)


def parse_E_prime(tokens, left_node):
    if tokens[0].token_type in [TokenType.PLUS, TokenType.MINUS]:
        node = tokens.pop(0)
        node.children = [left_node, parse_T(tokens)]
        return parse_E_prime(tokens, node)
    return left_node


def parse_T(tokens):
    left_node = parse_F(tokens)
    return parse_T_prime(tokens, left_node)


def parse_T_prime(tokens, left_node):
    if tokens[0].token_type == TokenType.MOD:
        node = tokens.pop(0)
        node.children = [left_node, parse_F(tokens)]
        return parse_T_prime(tokens, node)
    return left_node


def parse_F(tokens):
    if tokens[0].token_type == TokenType.LPAREN:
        tokens.pop(0)
        node = parse_E(tokens)
        tokens.pop(0)
        return node
    return tokens.pop(0)


def evaluate(node):
    if node.token_type == TokenType.ID:
        return node.value
    elif node.token_type == TokenType.PLUS:
        return evaluate(node.children[0]) + evaluate(node.children[1])
    elif node.token_type == TokenType.MINUS:
        return evaluate(node.children[0]) - evaluate(node.children[1])
    elif node.token_type == TokenType.MOD:
        return evaluate(node.children[0]) % evaluate(node.children[1])


def calculate(expression):
    tokens = tokenize(expression)
    root = parse_E(tokens)
    return evaluate(root)


def print_tree(node, depth=0):
    if node.token_type == TokenType.ID:
        print(f"{' ' * depth * 2}{node.token_type.name}({node.value})")
    else:
        print(f"{' ' * depth * 2}{node.token_type.name}")
        for child in node.children:
            print_tree(child, depth + 1)


def main():
    print("Ingrese una expresión matemática válida.")
    print("Ejemplo: 10+5-2")
    print("Escriba 'salir' para finalizar.")

    while True:
        try:
            expression = input(">> ")
            if expression.lower() == "salir":
                break
            tokens = tokenize(expression)
            root = parse_E(tokens)
            result = evaluate(root)
            print("\nÁrbol sintáctico:")
            print_tree(root)
            print(f"\nEl resultado es: {result}")
        except ValueError:
            print("Entrada inválida. Verifique la expresión.")
        except IndexError:
            print("Error de sintaxis. Verifique la expresión.")
        except Exception as e:
            print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()
