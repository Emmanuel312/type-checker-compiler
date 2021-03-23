# Generated from antlr4-python3-runtime-4.7.2/src/autogen/Grammar.g4 by ANTLR 4.7.2
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .GrammarParser import GrammarParser
else:
    from GrammarParser import GrammarParser

# This class defines a complete generic visitor for a parse tree produced by GrammarParser.

'''
COMO RESGATAR INFORMAÇÕES DA ÁRVORE

Observe o seu Grammar.g4. Cada regra sintática gera uma função com o nome corespondente no Visitor e na ordem em que está na gramática.

Se for utilizar sua gramática do projeto 1, por causa de conflitos com Python, substitua as regras file por fiile e type por tyype. Use prints temporários para ver se está no caminho certo.  
"make tree" agora desenha a árvore sintática, se quiser vê-la para qualquer input, enquanto "make" roda este visitor sobre o a árvore gerada a partir de Grammar.g4 alimentada pelo input.

Exemplos:

# Obs.: Os exemplos abaixo utilizam nós 'expression', mas servem apra qualquer tipo de nó

self.visitChildren(ctx) # visita todos os filhos do nó atual
expr = self.visit(ctx.expression())  # visita a subárvore do nó expression e retorna o valor retornado na função "visitRegra"

for i in range(len(ctx.expression())): # para cada expressão que este nó possui...
    ident = ctx.expression(i) # ...pegue a i-ésima expressão


if ctx.FLOAT() != None: # se houver um FLOAT (em vez de INT ou VOID) neste nó (parser)
    return Type.FLOAT # retorne tipo float

ctx.identifier().getText()  # Obtém o texto contido no nó (neste caso, será obtido o nome do identifier)

token = ctx.identifier(i).IDENTIFIER().getPayload() # Obtém o token referente à uma determinada regra léxica (neste caso, IDENTIFIER)
token.line      # variável com a linha do token
token.column    # variável com a coluna do token
'''


# Dica: Retorne Type.INT, Type.FLOAT, etc. Nos nós e subnós das expressões para fazer a checagem de tipos enquanto percorre a expressão.
class Type:
    VOID = "void"
    INT = "int"
    FLOAT = "float"
    STRING = "char *"
    ERROR = "ERROR"


class GrammarCheckerVisitor(ParseTreeVisitor):
    ids_defined = {}  # Dicionário para armazenar as informações necessárias para cada identifier definido
    inside_what_function = ""  # String que guarda a função atual que o visitor está visitando. Útil para acessar dados da função durante a visitação da árvore sintática da função.

    def get_current_function_definition(self):
        return self.ids_defined[self.inside_what_function]

    # Visit a parse tree produced by GrammarParser#fiile.
    def visitFiile(self, ctx: GrammarParser.FiileContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#function_definition.
    def visitFunction_definition(self, ctx: GrammarParser.Function_definitionContext):
        tyype = ctx.tyype().getText()
        name = ctx.identifier().getText()
        params = self.visit(ctx.arguments())
        self.ids_defined[name] = tyype, params
        self.inside_what_function = name
        self.visit(ctx.body())

        return

    # Visit a parse tree produced by GrammarParser#body.
    def visitBody(self, ctx: GrammarParser.BodyContext):
        function_return_type = self.get_current_function_definition()[0]
        # print(f"começo da funcao {self.inside_what_function}")
        for i in range(len(ctx.statement())):
            # throw a non void error
            return_statement = ctx.statement(i).RETURN()

            if return_statement is not None:
                # current_return_statement_type = self.visit(ctx.statement(i))
                if function_return_type == Type.VOID:
                    print(f"ERROR: trying to return a non void expression from void function"
                        f" 'doing' in line {return_statement.getPayload().line} and "
                        f"{return_statement.getPayload().column}")
                # function with return a diferent type
                # if function_return_type !=


        # print("fim da funcao")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#statement.
    def visitStatement(self, ctx: GrammarParser.StatementContext):
        # print(ctx.if_statement())
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#if_statement.
    def visitIf_statement(self, ctx: GrammarParser.If_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#else_statement.
    def visitElse_statement(self, ctx: GrammarParser.Else_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#for_loop.
    def visitFor_loop(self, ctx: GrammarParser.For_loopContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#for_initializer.
    def visitFor_initializer(self, ctx: GrammarParser.For_initializerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#for_condition.
    def visitFor_condition(self, ctx: GrammarParser.For_conditionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#for_step.
    def visitFor_step(self, ctx: GrammarParser.For_stepContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#variable_definition.
    def visitVariable_definition(self, ctx: GrammarParser.Variable_definitionContext):
        for i in range(len(ctx.array())):
            text = ctx.array(i).identifier().getText()
            self.ids_defined[text] = ctx.tyype().getText()

        for i in range(len(ctx.identifier())):
            text = ctx.identifier(i).getText()
            token = ctx.identifier(i).IDENTIFIER().getPayload()
            self.ids_defined[text] = ctx.tyype().getText()

            if ctx.expression(i):
                expr_type = self.visitExpression(ctx.expression(i))
                var_type = self.ids_defined.get(text, Type.VOID)
                if expr_type != var_type:
                    if var_type == Type.FLOAT and expr_type == Type.INT:
                        continue
                    elif var_type == Type.INT and expr_type == Type.FLOAT:
                        print(f"WARNING: possible loss of information assigning float expression to int "
                              f"variable '{text}' in line {token.line} and column {token.column}")
                    else:
                       print(f"ERROR: trying to assign 'void' expression to variable '{text}' in "
                             f"line {token.line} and column {token.column}")

        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#variable_assignment.
    def visitVariable_assignment(self, ctx: GrammarParser.Variable_assignmentContext):
        if ctx.identifier():
            variable_name = ctx.identifier().getText()
            token = ctx.identifier().IDENTIFIER().getPayload()

            if not self.ids_defined.get(variable_name, None):
                print(f"ERROR: undefined variable '{variable_name}' in line {token.line} and column {token.column}")

        if ctx.expression():
            expr_type = self.visitExpression(ctx.expression())
            text = None

            if ctx.identifier():
                token = ctx.identifier().IDENTIFIER().getPayload()
                text = ctx.identifier().getText()
                id_type = self.ids_defined.get(text, Type.VOID)

            else:
                token = ctx.array().identifier().IDENTIFIER().getPayload()
                text = ctx.array().identifier().getText()
                id_type = self.ids_defined.get(text, Type.VOID)

            # Check the types of the variable that is receiving the assignment and the value being assigned.
            # if not (id_type == expr_type or (id_type == Type.INT and expr_type == Type.FLOAT)):
            #     print("[ERROR]::[Oh. My. God. You just tried to assign <{}> to <{}>. Wow.] ({},{})".format(expr_type,
            #                                                                                                id_type, str(
            #             token.line), str(token.column)))
            if id_type == Type.INT and expr_type == Type.FLOAT:
                print(f"WARNING: possible loss of information assigning float expression to int variable "
                      f"'{text}' in line {token.line} and column {token.column}")
            return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#expression.
    def visitExpression(self, ctx: GrammarParser.ExpressionContext):
        tyype = Type.VOID
        if len(ctx.expression()) == 0:
            if ctx.integer():
                text = ctx.integer().getText()
                token = ctx.integer().INTEGER().getPayload()
                tyype = Type.INT

            elif ctx.floating():
                text = ctx.floating().getText()
                token = ctx.floating().FLOATING().getPayload()
                tyype = Type.FLOAT

            elif ctx.string():
                tyype = Type.STRING

            elif ctx.identifier():
                text = ctx.identifier().getText()
                token = ctx.identifier().IDENTIFIER().getPayload()
                tyype = self.ids_defined.get(text, Type.VOID)

            elif ctx.array():
                text = ctx.array().identifier().getText()
                token = ctx.array().identifier().IDENTIFIER().getPayload()
                tyype = self.ids_defined.get(text, Type.VOID)

            elif ctx.function_call():
                token = ctx.function_call().identifier().IDENTIFIER().getPayload()
                function_name = ctx.function_call().identifier().IDENTIFIER().getText()
                function_type = self.ids_defined[function_name][0]
                defined_function_params = self.ids_defined[function_name][1]
                called_function_params = self.visit(ctx.function_call())

                if len(defined_function_params) != len(called_function_params):
                    print(f"ERROR: incorrect number of parameters for function '{function_name}' in "
                          f"line {token.line} and column {token.column}. Expecting {len(defined_function_params)}, "
                          f"but {len(called_function_params)} were given")

                # check possible loss of information param by param
                param_index = 0
                for defined_function_param, called_function_param in zip(defined_function_params, called_function_params):
                    if called_function_param == Type.FLOAT and defined_function_param == Type.INT:
                        print(f"WARNING: possible loss of information converting float expression to "
                              f"int expression in parameter {param_index} of function '{function_name}' "
                              f"in line {token.line} and column {token.column}")
                    param_index += 1



                tyype = function_type

        elif len(ctx.expression()) == 1:
            if ctx.OP:
                text = ctx.OP.text
                token = ctx.OP
                tyype = self.visit(ctx.expression(0))

            else:
                tyype = self.visit(ctx.expression(0))

        elif len(ctx.expression()) == 2:
            text = ctx.OP.text
            token = ctx.OP
            left = self.visit(ctx.expression(0))
            right = self.visit(ctx.expression(1))

            if text in ['+', '-', '*', '/']:
                if not (left == right or (left == Type.INT and right == Type.FLOAT)):
                    print(f"ERROR: binary operator '{text}' used on type void in line {token.line} and column {token.column}")

            tyype = right
        return tyype

    # Visit a parse tree produced by GrammarParser#array.
    def visitArray(self, ctx: GrammarParser.ArrayContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#array_literal.
    def visitArray_literal(self, ctx: GrammarParser.Array_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#function_call.
    def visitFunction_call(self, ctx: GrammarParser.Function_callContext):
        params_type = []
        for i in range(len(ctx.expression())):
            param_type = self.visit(ctx.expression(i))
            params_type.append(param_type)

        return params_type

    # Visit a parse tree produced by GrammarParser#arguments.
    def visitArguments(self, ctx: GrammarParser.ArgumentsContext):
        params_type = []
        for i in range(len(ctx.identifier())):
            # id = ctx.identifier(i).getText()
            tyype = ctx.tyype(i).getText()
            # self.ids_defined[id] = tyype
            params_type.append(tyype)
        return params_type

    # Visit a parse tree produced by GrammarParser#tyype.
    def visitTyype(self, ctx: GrammarParser.TyypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#integer.
    def visitInteger(self, ctx: GrammarParser.IntegerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#floating.
    def visitFloating(self, ctx: GrammarParser.FloatingContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#string.
    def visitString(self, ctx: GrammarParser.StringContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GrammarParser#identifier.
    def visitIdentifier(self, ctx: GrammarParser.IdentifierContext):
        return self.visitChildren(ctx)
