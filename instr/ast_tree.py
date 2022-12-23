import settings

class AST:
    def __init__(self, state, text):
        self.__state = state
        self.__next_state = None
        #   self.__indexes = indexes
        self.__text = text

    def set_entre(self, state):
        bstate = self.__get_next()
        state.set_next(bstate)
        self.__next_state = state

    def __get_next(self):
        return self.__next_state

    def __get_name(self):
        return self.__state[0]

    def __instr_node(self, comm):
        if self.__state == "MUST":
            if self.__text != None:
                return "{\n" + comm.format(settings.rnd.rand())
            else:
                return self.__text + comm.format(settings.rnd.rand())
        elif self.__state == "MEND":
            if self.__text != None:
                return comm.format(settings.rnd.rand()) + "}"
            else:
                return comm.format(settings.rnd.rand()) + self.__text
        elif self.__state in ["CASE", "DEF"]:
            return self.__text + comm.format(settings.rnd.rand())
        elif self.__state in ["RET", "BRE", "CONT",  "IF", "FOR","DO", "SWIT"]:
            return comm.format(settings.rnd.rand()) + self.__text

    def __check_next(self):
        state = self.__next_state
        if state.__get_name() == "EMPT":
            state = state.__check_next()
        return state


    def set_next(self, next):
        if self.__next_state == None:
            self.__next_state = next
        else:
            n_state = self.__get_next()
            n_state.set_next(next)

    def instr(self, ins):
        node = self
        node.set_entre(AST(("INST", (0, 1)), ins[0] % settings.rnd.rand()))
        node = node.__get_next()
        node = node.__check_next()
        while node != None:
            if node.__get_name() in ["MUST", "END", "CASE", "DEF"]:
                node.set_entre(AST(("INST", (0, 1)), ins[1] % settings.rnd.rand()))
                node = node.__get_next()
                node = node.__get_next()
                continue
            if node.__get_name() == "MEND":
                if node.__get_next() != None and node.__check_next().__get_name() not in ["ELSE", "WHIL"]:
                    node.set_entre(AST(("INST", (0, 1)), ins[1] % settings.rnd.rand()))
                    node = node.__get_next()
                    node = node.__get_next()
                elif node.__get_next() == None:
                    break
            node_next = node.__check_next()
            if node_next.__get_name() in ["IF", "FOR", "DO", "SWIT", "RET", "BRE", "CONT"]:
                node.set_entre(AST(("INST", (0, 1)), ins[1] % settings.rnd.rand()))
                node = node_next
            node = node.__check_next()

    def __get_end_block(self):
        cicle_done = ["IF", "ELSE", "FOR", "WHIL", "DO"]
        state = self
        if state.__get_name() in cicle_done:
            next_state = state.__check_next()
            if next_state.__get_name() != "MUST":
                state.set_entre(AST(("MUST", (0, 1)), "{"))
                next_state = next_state.__get_end_block()
                next_state.set_entre(AST(("MEND", (0, 1)), "}"))
                state = next_state.__get_next()
            else:
                while next_state.__get_name() != "MEND":
                    next_state = next_state.__get_next()
                    next_state = next_state.__get_end_block()
                state = next_state
        return state

    def ast_analyze(self):
        cicle_done = ["IF", "ELSE", "FOR", "WHIL", "DO"]
        state = self
        while state != None:
            if state.__get_name() in cicle_done:
                next_state = state.__check_next()
                if next_state.__get_name() != "MUST":
                    state.set_entre(AST(("MUST", (0, 1)), "{"))
                    next_state = next_state.__get_end_block()
                    next_state.set_entre(AST(("MEND", (0, 1)), " }"))
                    state = next_state.__get_next()
            state = state.__get_next()

    def ast_to_str(self):
        out = []
        state = self
        while state != None:
            out.append(state.__text)
            state = state.__get_next()
        return ''.join(out)


'''
ast = AST(0,0)
ast.set_next(AST(1,1))
ast.set_next(AST(2,2))
ast.set_entre(AST(-1, -1))
ast.set_entre(AST(-2, -2))
'''