class CalculationParser:
    def __init__(self, raw_string, priority = None, convert_table = None, do_simplify=True, to_rpn=False):
        if convert_table is None: convert_table = {"^":"pow","§":"eucdiv","+": "add","-": "sub","*": "mul","/": "div"}
        self.convert_table_invert = dict(zip(convert_table.values(), convert_table.keys()))
        if priority is None: priority = {"+": 3,"-": 3,"*": 2,"/": 2,"§":1,"^":1}
        self.raw_string = raw_string
        self.priority = priority
        self.convert_table = convert_table
        self.do_simplify = do_simplify
        self.to_rpn = to_rpn
    
    def get_priority(self, x):
        return self.priority[x]
    
    def get_index_best_priority(self, inp):
        best_priority = 0
        best_index = 0
        for i in range(len(inp)):
            if inp[i]["type"] == "op" and self.get_priority(inp[i]["cnt"]) > best_priority:
                best_priority = self.get_priority(inp[i]["cnt"])
                best_index = i
        return best_index
    
    def ast(self, inp):
        if len(inp) == 1:
            return inp[0]
        best_index = self.get_index_best_priority(inp)
        return {"type": "func","cnt": self.convert_table[inp[best_index]["cnt"]],"args": [self.ast(inp[:best_index]),self.ast(inp[best_index + 1:])]}
    
    def to_list(self, entree : str):
        if any(char for char in self.priority if char not in f"{self.priority}1234567890"): raise Exception("bad string in input of the CalculationParser")
        entree = entree.replace("**", "^").replace("//", "§")
        liste = []
        acc = 0
        var_acc = ""
        for char in entree:
            if char.isdecimal() and var_acc == "":
                acc = acc*10+int(char)
            elif char in self.priority:
                liste.extend(({"type": "int", "cnt": acc or var_acc}, {"type": "op", "cnt": char}))
                acc = 0
                var_acc = ""
            else:
                var_acc += char
        liste.append({"type": "int", "cnt": acc or var_acc})
        return liste
    
    def calculate(self, func, op1, op2):
        match func:
            case "add":
                return op1+op2
            case "mul":
                return op1*op2
            case "sub":
                return op1-op2
            case "div":
                return op1/op2
            case "pow":
                return op1**op2
            case "eucdiv":
                return op1//op2
    
    def simplify(self, entree):
        # simplifie les constantes pour éviter des calculs inutiles
        if entree["type"] == "func":
            args = [self.simplify(entree["args"][0]), self.simplify(entree["args"][1])]
            if isinstance(args[0]["cnt"], int) and isinstance(args[1]["cnt"], int):
                return {"type":"int", "cnt":self.calculate(entree["cnt"],args[0]["cnt"], args[1]["cnt"])}
            else:
                return {'type': 'func', 'cnt': entree["cnt"], 'args':args}
        elif entree["type"] == "int" and str(entree["cnt"]).isnumeric():
            return {"type":"int", "cnt":int(entree["cnt"])}
        elif entree["type"] == "int" and not str(entree["cnt"]).isnumeric():
            return {"type":"int", "cnt":entree["cnt"]}
        
    def rpn_convert(self, entree):
        # convertit la sortie du programme en rpn
        string_rpn = ""
        if entree["type"] == "int":
            return entree["cnt"]
        string_rpn = f"{str(self.rpn_convert(entree['args'][0]))} {str(self.rpn_convert(entree['args'][1]))} {str(self.convert_table_invert[entree['cnt']])}"
        return string_rpn
        
    def run(self):
        if self.to_rpn:
            return self.rpn_convert(self.simplify(self.ast(self.to_list(self.raw_string))))
        if self.do_simplify:
            return self.simplify(self.ast(self.to_list(self.raw_string)))
        else:
            return self.ast(self.to_list(self.raw_string))

if __name__ == "__main__":
    def tests():
        sortie = CalculationParser('1+2**3').run()
        print("TEST 1 OK") if sortie == {'type': 'int', 'cnt': 9} else print("TEST 1 RATE")
        sortie = CalculationParser('1+2+3', do_simplify=False).run()
        print("TEST 2 OK") if sortie == {'type': 'func', 'cnt': 'add', 'args': [{'type': 'int', 'cnt': 1}, {'type': 'func', 'cnt': 'add', 'args': [{'type': 'int', 'cnt': 2}, {'type': 'int', 'cnt': 3}]}]} else print("TEST 2 RATE")
        sortie = CalculationParser('3**2+a').run()
        print("TEST 3 OK") if sortie == {'type': 'func', 'cnt': 'add', 'args': [{'type': 'int', 'cnt': 9}, {'type': 'int', 'cnt': 'a'}]} else print("TEST 3 RATE")
        sortie = CalculationParser('a+2+3').run()
        print("TEST 4 OK") if sortie == {'type': 'func', 'cnt': 'add', 'args': [{'type': 'int', 'cnt': 'a'}, {'type': 'int', 'cnt': 5}]} else print("TEST 4 RATE")
        sortie = CalculationParser('2-a*6', to_rpn=True).run()
        print("TEST 5 OK") if sortie == "2 a 6 * -" else print("TEST 5 RATE")
        sortie = CalculationParser('2*4*5+1', to_rpn=True).run()
        print("TEST 6 OK") if sortie == 41 else print("TEST 6 RATE")
    tests()
