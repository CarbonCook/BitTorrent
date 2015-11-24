import re, types

class BDecoder:
    def __init__(self):
        self.lenparser = re.compile(r'([0-9]+)')
        self.intparser = re.compile(r'(-?[1-9][0-9]*)|(0)')

    def init(self, string):
        self.string = string
        if string[0] != 'd':
            raise Exception('Bencoding Syntax Error')

    def parse(self, string):
        self.init(string)
        return self.parseDict()

    def parseDict(self):
        dic = {}
        self.string = self.string[1:]
        self.parseItems(dic)
        self.string = self.string[1:]
        return dic

    def parseItems(self, dic):
        while self.string[0] != 'e':
            key = self.parseKey()
            dic[key] = self.parseValue()

    def parseKey(self):
        mobj = self.lenparser.match(self.string)
        if mobj is None:
            raise Exception('Bencoding Key Error')
        return self.parseStr(mobj)

    def parseValue(self):
        mobj = self.lenparser.match(self.string)
        if mobj is not None:
            return self.parseStr(mobj)
        elif self.string[0] == 'd':
            return self.parseDict()
        elif self.string[0] == 'i':
            return self.parseInt()
        elif self.string[0] == 'l':
            return self.parseList()
        else:
            raise Exception('Bencoding Value Error')

    def parseStr(self, mobj):
        sint = mobj.group(0)
        if self.string[len(sint)] != ':':
            raise Exception('Bencoding String Error')
        slen = int(sint)
        self.string = self.string[(len(sint) + 1):]
        s = self.string[:slen]
        self.string = self.string[slen:]
        '''try:
            return unicode(s, 'utf-8')
        except UnicodeDecodeError:'''
        return s

    def parseInt(self):
        mobj = self.intparser.match(self.string[1:])
        if mobj is None:
            raise Exception('Bencoding Integer Error')
        sint = mobj.group(0)
        if self.string[len(sint) + 1] != 'e':
            raise Exception('Bencoding Syntax Error')
        self.string = self.string[(len(sint) + 2):]
        return int(sint)

    def parseList(self):
        li = []
        self.string = self.string[1:]
        while self.string[0] != 'e':
            li.append(self.parseValue())
        self.string = self.string[1:]
        return li


class BEncoder:
    def __init__(self):
        pass

    def dump(self, obj):
        return self.dumpValue(obj)

    def dumpValue(self, obj):
        if type(obj) is types.DictType:
            return self.dumpDict(obj)
        elif type(obj) is types.ListType:
            return self.dumpList(obj)
        elif type(obj) is types.IntType or type(obj) is types.LongType:
            return 'i' + str(obj) + 'e'
        elif type(obj) is types.StringType or type(obj) is types.UnicodeType:
            return self.dumpStr(obj)
        else:
            raise Exception('TypeError')

    def dumpDict(self, dic):
        s = 'd'
        for key in dic:
            s += self.dumpStr(key)
            s += self.dumpValue(dic[key])
            if type(s) is types.UnicodeType:
                print s
                raise Exception(s)
        return s + 'e'

    def dumpList(self, li):
        s = 'l'
        for elem in li:
            s += self.dumpValue(elem)
        return s + 'e'

    def dumpStr(self, s):
        try:
            return str(len(s)) + ':' + str(s)
        except UnicodeEncodeError:
            return str(len(s)) + ':' + s


bdecoder = BDecoder()
bencoder = BEncoder()