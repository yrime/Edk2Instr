import re

from instr import cparser


class cInstr:

    def __init__(self, file):
        with open(file) as fl:
            self.data = fl.read()

    def nullstr_remover(self, text):
        lines = text.split('\n')
        new_lines = []
        for line in lines:
            if len(line) > 0 and not line.isspace():
                new_lines.append(line)
        return '\n'.join(new_lines)

    def comment_remover(self, text):
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

    def clean_text(self):
        self.data = self.comment_remover(self.data)
        self.data = self.nullstr_remover(self.data)

    def instr(self, ins):
        instr_file = []
        vieil = 0
        cp = cparser.cparser()
        functions = cp.get_func_bb(self.data)
        for fun in functions:
            instr_file.append(self.data[vieil: fun[0]+1])
            vieil = fun[1] + 1
            texti = self.data[fun[0]: fun[1] + 1]
            cp.build_ast_func(texti)
            text_instr = cp.instr_ast(texti, ins)
            instr_file.append(text_instr)
        instr_file.append(self.data[vieil:])
        return ''.join(instr_file)

