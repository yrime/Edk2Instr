
import os.path
import json
import os

from os import path

from infParser import infParser
from instr.cinstr import cInstr
from instr.cparser import cparser

simple_json = "{" \
              "\"files\":[" \
              "\"file1\",\"file2\"]," \
              "\"iFunc\":[" \
              "{\"package\":\"package1\"}," \
              "{\"init\":\"init1\"}," \
              "{\"func\":\"func1\"}]" \
              "}"

class parseConfig:
    files = None
    packages = None
    init = None
    func = None

    def __init__(self, str):
        jTable = json.loads(str)
        print(jTable["iFunc"][0]["package"])
        self.files = jTable["files"]
        self.packages = jTable["iFunc"][0]
        self.init = jTable["iFunc"][1]
        self.func = jTable["iFunc"][2]

    def getFiles(self):
        return self.files
    def getPackages(self):
        return self.packages["package"]
    def getInit(self):
        return self.init['init']
    def getFunc(self):
        return self.func['func']


class Instr:
      #  fStr = simple_json

    def instr(self, argv):
        fStr = ""
        if path.exists(argv) == False:
            print("No such file config. error")
            return None
        else:
            with open(argv, "r") as configFile:
                fStr = configFile.read()
        self.__files_instr(fStr)

    def restore(self, argv):
        fStr = ""
        if path.exists(argv) == False:
            print("No such file config. error")
            return None
        else:
            with open(argv, "r") as configFile:
                fStr = configFile.read()
        ps = parseConfig(fStr)
        for f in ps.getFiles():
            self.__restore_copy(f)
            with open(f, "r") as cf:
                str = cf.read()
            ip = infParser()
            gic = ip.getInfClasses(str)
            dirname = os.path.dirname(f) + "\\"
            for cfgic in gic:
                if os.path.isfile(dirname + cfgic + ".copy"):
                    self.__restore_copy(dirname + cfgic)

    def infmode(self, dir, func):
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith('.inf'):
                    print(os.path.join(root,file))
                    if os.path.isfile(os.path.join(root,file) + ".copy"):
                        self.__restore_copy(os.path.join(root,file))
                    else:
                        self.__create_copy(os.path.join(root,file))
                    with open(os.path.join(root,file), "r") as cf:
                        str = cf.read()
                    ip = infParser()
                    infupd = ip.setLibraryClasses(func, str)
                    with open(os.path.join(root,file), "w") as cf:
                        cf.write(infupd)

    def infrestore(self, dir):
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith('.inf'):
                    print(os.path.join(root, file))
                    if os.path.isfile(os.path.join(root, file) + ".copy"):
                        self.__restore_copy(os.path.join(root, file))


    def __files_instr(self, text):
        ps = parseConfig(text)
        fss = ps.getFunc()
        iss = ps.getInit()
        pss = ps.getPackages()
        for f in ps.getFiles():
            self.__file_instr(f, [iss, fss, pss])
        #print(ps.getFiles()[1])

    def __create_copy(self,file):
        if not os.path.isfile(file + ".copy"):
            with open(file, "r") as cf:
                str = cf.read()
            with open(file + ".copy", "w") as cf:
                cf.write(str)

    def __restore_copy(self, file):
        if os.path.isfile(file + ".copy"):
            with open(file+ ".copy", "r") as cf:
                str = cf.read()
            with open(file, "w") as cf:
                cf.write(str)

    def __file_instr(self, text, funcs):
        if os.path.isfile(text + ".copy"):
            self.__restore_copy(text)
        else:
            self.__create_copy(text)
        with open(text, "r") as cf:
            str = cf.read()
        ip = infParser()
        gic = ip.getInfClasses(str)
        infupd = ip.setLibraryClasses(funcs[2], str)
        with open(text, "w") as cf:
            cf.write(infupd)
        print(gic)
        dirname = os.path.dirname(text) + "\\"
        print(dirname)
        for cfgic in gic:
            if os.path.isfile(dirname + cfgic + ".copy"):
                self.__restore_copy(dirname + cfgic)
            else:
                self.__create_copy(dirname + cfgic)
     #       ci = cInstr(dirname + cfgic)
            cp = cparser()
            f = cp.parse(dirname + cfgic,funcs)

         #   iText = ci.instr(funcs)
            print(dirname + cfgic)
            with open(dirname + cfgic, "w") as cf:
                cf.write(f)

        # self.get_files_list(fStr)