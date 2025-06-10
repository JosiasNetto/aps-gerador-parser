from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor:
    def __init__(self):
        self.variables = {} 

    def visit(self, ctx):
        if isinstance(ctx, ArithmeticParser.ProgramContext):
            return self.visitProgram(ctx)
        elif isinstance(ctx, ArithmeticParser.StatementContext):
            return self.visitStatement(ctx)
        elif isinstance(ctx, ArithmeticParser.AssignmentContext):
            return self.visitAssignment(ctx)
        elif isinstance(ctx, ArithmeticParser.ExprContext):
            return self.visitExpr(ctx)
        elif isinstance(ctx, ArithmeticParser.TermContext):
            return self.visitTerm(ctx)
        elif isinstance(ctx, ArithmeticParser.FactorContext):
            return self.visitFactor(ctx)
    
    def visitProgram(self, ctx):
        results = []
        for statement in ctx.statement():
            result = self.visit(statement)
            if result is not None:
                results.append(result)
        return results
        
    def visitStatement(self, ctx):
        if ctx.assignment():
            return self.visit(ctx.assignment())
        else:
            return self.visit(ctx.expr())
        
    def visitAssignment(self, ctx):
        var_name = ctx.VAR().getText()
        value = self.visit(ctx.expr())
        self.variables[var_name] = value
        return f"{var_name} = {value}"
    
    def visitExpr(self, ctx):
        result = self.visit(ctx.term(0)) 
        for i in range(1, len(ctx.term())):  
            if ctx.getChild(i * 2 - 1).getText() == '+':  
                result += self.visit(ctx.term(i))
            else:
                result -= self.visit(ctx.term(i))
        return result
    
    def visitTerm(self, ctx):
        result = self.visit(ctx.factor(0))  
        for i in range(1, len(ctx.factor())):  
            if ctx.getChild(i * 2 - 1).getText() == '*':  
                result *= self.visit(ctx.factor(i))
            else:
                result /= self.visit(ctx.factor(i))
        return result
    
    def visitFactor(self, ctx):
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.VAR():
            var_name = ctx.VAR().getText()
            if var_name in self.variables:
                return self.variables[var_name]
            else:
                raise ValueError(f"Erro: Variável '{var_name}' não foi definida")
        else:
            return self.visit(ctx.expr())

def main():
    visitor = ArithmeticVisitor() 
    while True:
        try:
            user_input = input(">>> ")
            if user_input == "sair":
                break

            input_stream = InputStream(user_input)
            lexer = ArithmeticLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = ArithmeticParser(token_stream)
            tree = parser.program()

            results = visitor.visit(tree)
            for res in results:
                print(res)
        except Exception as e:
            print("Erro:", str(e))
    
if __name__ == '__main__':
    main()
