# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import instrumentation as instr
import settings

def print_help():
    print("this help for utils instrumentation")

def check_argv(argv):
    param = argv[1]
    ii = instr.Instr()
    if param == "i": # i config.txt
        settings.init()
        ii.instr(argv[2])
        # for debug
      #  ii.infmode("C:\\UefiAfl\\ForVisual2\\SB_fuzzing\\InfotecsPkg", "UefiAflProxy2")
    elif param == "r": # r config.txt
        ii.restore(argv[2])
    elif param == "p": # p C:\UefiAfl\ForVisual2\SB_fuzzing\InfotecsPkg
       # ii.infmode(argv[2], "UefiAflProxy2")
        ii.infrestore(argv[2])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Started Edk2 instrumentation')
    if len(sys.argv) != 1:
        check_argv(sys.argv)
    else:
        print_help()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
