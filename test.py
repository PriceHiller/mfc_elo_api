
class Test(object):
    ...

    @staticmethod
    def instantiations(*data):
        if len(data) == 1:
            try:
                return Record(*data)
            except Exception as Error:
                print("Record.instantiation (Metal) Caught Exception: ", Error, "\n", "Data: {}".format(data)); return None
        elif len(data) > 1:
            try:
                return [Record.instantiate(Item) for Item in data]
            except Exception as Error:
                print("Record.instantiations (Metal) Caught Exception: ", Error, "\n", "Data: {}".format(data)); return None
        else:
            if Table.total() == 0:
                return None
            else:
                raise ValueError("Record (Metal) *.instantiations Error: data cannot be empty")
