import re

import settings
from instr.ast_tree import AST
from instr.operands import operands


class cparser:

    def __iter_bb_fin(self, text, index):
        i = 0
        fi = 0
        while (True):
            if text[index + i] == '{':
                fi = fi + 1
            elif text[index + i] == '}':
                fi = fi - 1
                if fi == 0:
                    return index + i
            i = i + 1

    def __iter_bb(self, text):
        indexes_bb = []
        iter = 0
        while iter < len(text):
            if text[iter] == "{":
                ifin = self.__iter_bb_fin(text, iter)
                indexes_bb.append((iter, ifin))
                iter = ifin
            iter = iter + 1
        return indexes_bb

    def __get_func_bb(self, text, indexes_bb):
        indexes_fun = []
        for match in re.finditer("\)[ \t]*\n?[ \t]*\{", text):
            for index in indexes_bb:
                if (match.end() - 1) == index[0]:
                    indexes_fun.append((index[0],index[1]))
        return indexes_fun

    def __get_bb(self, text):
        i = self.__iter_bb(text)
        f = self.__get_func_bb(text, i)
        return f

    def __create_ast_tree(self, bb):
        operand = operands()
        i = 0
        state = operand.get_state(bb, i)
        i = state[1][1]
        ast = AST(state, bb[0:i]) #state indexes, text
        while i < len(bb):
            state = operand.get_state(bb, i)
            i2 = state[1][1]
            ast.set_next(AST(state, bb[i:i2]))
            i = i2
        return ast

    def __nullstr_remover(self, text):
        lines = text.split('\n')
        new_lines = []
        for line in lines:
            if len(line) > 0 and not line.isspace():
                new_lines.append(line)
        return '\n'.join(new_lines)

    def __comment_remover(self, text):
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return " "  # note: a space and not an empty string
            else:
                return s

        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        return re.sub(pattern, replacer, text)

    def clean_text(self, text):
        data = self.__comment_remover(text)
        data = self.__nullstr_remover(data)
        return data

    def parse(self, file, uinst):
        instr_file = ["#include <Library/UefiAflProxy2.h>\n"]
        i = 0
        with open(file, "r") as cf:
            text = cf.read()
        text = self.clean_text(text)
        bb = self.__get_bb(text)
        for b in bb:
            instr_file.append(text[i:b[0]])
            i = b[1] + 1
            ast = self.__create_ast_tree(text[b[0]: b[1] + 1])
            ast.ast_analyze()
            ast.instr(uinst)
            instr_file.append(ast.ast_to_str())
            print(ast.ast_to_str())
        print('finish')
        print(''.join(instr_file))
        return ''.join(instr_file)
'''
settings.init()
test = "qwe ){ wer } asd ){ fgh { zxc } do { asdas; asd;} while  ( sdfs )  ; }"
test2 = "C:\\UefiAfl\\ForVisual\\vipnet_safeboot_3_0_1_EDK\\InfotecsPkg\\Common\\modules.c"
cp = cparser()
f = cp.parse(test2)
#print(test[f[1][0]:f[1][1] + 1])
'''