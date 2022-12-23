import re

class operands:
    def __init__(self):
        self.statetment = [
            ("IF",      "if[ \t\n\r]*\("),
            ("ELSE",    "else[\{ \r\t\n]*"),
            ("FOR",     "for[ \t\n\r]*\("),
            ("WHIL",    "while[ \t\n\r]*\("),
            ("DO",      "do[ \t\n\r]*"),
            ("SWIT",    "switch[ \r\t\n]*\("),
            ("CASE",    "case[ \r\t\n]* [^:]+[ \n\t\r]*:"),
            ("RET",     "return"),
            ("BRE",     "break[ ]*;"),
            ("CONT",    "continue[ ]*;"),
            ("DEF",     "default[ ]*:"),
            ("EMPT",    "[ \n\t\r]+"),
            ("MUST",    "{"),
            ("MEND",    "}"),
            ("END",     ";[ \n\t\r]*")
        ]

    def build(self):
        return self.statetment

    def __get_first_symbol(self, text, pos, sym):
        i = 0
        for c in text[pos:]:
            if c == sym:
                return pos + i
            i = i + 1

    def __get_indexes_struct(self, text, index, symbol1, symbol2):
       # print("sdf")
        fi = 0
        i = 0
        for c in text[index:]:
            if c == symbol1:
                fi = fi + 1
                if fi == 1:
                    a1 = index + i
            elif c == symbol2:
                fi = fi - 1
                if fi <= 0 :
                    a2 = index + i
                    return (a1, a2 + 1)
            i = i + 1

    def __state_pos(self, text, state):
        match state[0]:
            case "IF":
                ind = self.__get_indexes_struct(text, state[1][0], '(', ')')
                ret = (state[1][0], ind[1])
            case "FOR":
                ind = self.__get_indexes_struct(text, state[1][0], '(', ')')
                ret = (state[1][0], ind[1])
            case "WHIL":
                ind = self.__get_indexes_struct(text, state[1][0], '(', ')')
                ret = (state[1][0], ind[1])
            case "SWIT":
                ind = self.__get_indexes_struct(text, state[1][0], '(', ')')
                ret = (state[1][0], ind[1])
            case "ELSE":
                ret = (state[1][0], state[1][0] + 3 + 1)
            case "DO":
                ret = (state[1][0], state[1][0] + 1 + 1)
            case "CASE":
                ret = (state[1][0], state[1][1])
            case "RET":
                iret = self.__get_first_symbol(text, state[1][0] + 5 + 1, ';') + 1
                ret = (state[1][0], iret)
            case "BRE":
                ret = (state[1][0], state[1][1])
            case "CONT":
                ret = (state[1][0], state[1][1])
            case "DEF":
                ret = (state[1][0], state[1][1])
            case "EMPT":
                ret = (state[1][0], state[1][1])
            case "MUST":
             #   ind = self.__get_indexes_struct(text, state[1][0], '{', '}')
             #   ret = (state[1][0], ind[1])
                ret = (state[1][0], state[1][0] + 1)
            case "MEND":
                ret = (state[1][0], state[1][0] + 1)
            case "END":
                ret = (state[1][0], state[1][0] + 1)
        return ret

    def get_state(self, text, i):
        for o in self.statetment:
           # print(o)
            prog = re.compile(o[1])
            res = prog.match(text, i)
            if res != None:
                ret = self.__state_pos(text, (o[0], (res.start(), res.end())))
                return (o[0], ret)

        iret = self.__get_first_symbol(text, i, ';') + 1
        return ("UDEF", (i, iret))