

class SymbolTable:

    def __init__(self):
        self.table = {}

    def add(self, name, cat, type, level, params=None):
        self.table[str(name)] = {}
        self.table[str(name)]["cat"] = cat
        self.table[str(name)]["type"] = type
        self.table[str(name)]["level"] = level
        self.table[str(name)]["params"] = params

    def search(self, name):
        if name in self.table:
            return True
        else:
            return False

    def remove(self, name):
        try:
            del self.table[name]
        except:
            print("Erro deletando {}".format(name))

    def remove_level(self, level):
        to_delete = []
        for name, attr in self.table.items():
            if attr["level"] == level:
                to_delete.append(name)

        for name in to_delete:
            del self.table[name]

    def print(self):
        return print(self.table)

    def print_names(self):
        l = ''
        for name, attr in self.table.items():
            l += str(print(name))

        return l


if __name__ == "__main__":
    a = SymbolTable()
    a.add("var1", "v", 1)
    a.add("var2", "f", 2)
    a.add("var3", "f", 2)
    a.add("var4", "f", 3)
    a.add("var5", "f", 2)
    a.remove_level(2)

    a.print()
