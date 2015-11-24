from bcoder import bdecoder, bencoder
from downloader import Downloader
import codecs, types, json, sys

class DictWriter():
    def __init__(self, obj):
        self.obj = obj
        self.indent = -1

    def getIndent(self):
        ind = ''
        for i in range(0, self.indent):
            ind += '&nbsp;&nbsp;&nbsp;&nbsp;'
        return ind

    def write(self):
        self.f = codecs.open('dict.html', 'wb', 'utf-8')
        if type(self.obj) is types.DictType:
            self.writeDict(self.obj)
        self.f.close()

    def writeDict(self, dic):
        self.indent += 1
        self.f.write('<br>\n')
        for key in dic:
            self.f.write(self.getIndent() + '<b>%s</b>: ' % key)
            self.writeValue(dic[key])
        self.indent -= 1

    def writeValue(self, val):
        if type(val) is types.DictType:
            self.writeDict(val)
        elif type(val) is types.ListType:
            self.writeList(val)
        elif type(val) is types.UnicodeType:
            self.f.write(val + '<br>\n')
        else:
            try:
                self.f.write(unicode(str(val), 'utf-8') + '<br>\n')
            except UnicodeDecodeError, e:
                self.writeBinary(val)
                self.f.write('<br>\n')

    def writeList(self, li):
        self.indent += 1
        self.f.write('<br>\n')
        for val in li:
            self.f.write(self.getIndent())
            self.writeValue(val)
        self.indent -= 1

    def writeBinary(self, bi):
        for c in bi:
            h = hex(ord(c))[2:]
            if len(h) == 1:
                h = '0' + h
            self.f.write(h)


if __name__ == '__main__':
    f = codecs.open(sys.argv[1], 'rb')
    string = f.read()
    f.close()
    print type(string)
    obj = bdecoder.parse(string)
    writer = DictWriter(obj)
    writer.write()
    print len(obj['info']['pieces'])
    '''trackers = []
    qparams = {}
    qparams['info_hash'] = obj['info']['pieces'][:20]
    qparams['peer_id'] = '2d0s1t2r6a1y0l9e2e4x'
    qparams['ip'] = '59.66.130.209'
    qparams['port'] = 6881
    qparams['uploaded'] = 0
    qparams['downloaded'] = 0
    qparams['left'] = obj['info']['piece length']
    qparams['compact'] = 0
    for announce in obj['announce-list']:
        dloader = Downloader(announce[0], qparams)
        response = dloader.download()
        if response is not None:
            res = bdecoder.parse(response)
            print announce[0], '\n', res, '\n'
            trackers.append((announce[0], res))
    fp = codecs.open('trackers.json', 'w', 'utf-8')
    json.dump(trackers, fp)
    fp.close()'''