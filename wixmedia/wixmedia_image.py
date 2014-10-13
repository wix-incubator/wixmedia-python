
class WixMediaImage(object):

    def __init__(self, file_uri):
        self.file_uri = file_uri
        self.text = ''

    def srz(self, w, h, q=85, a=1, radius=0.0, amount=1.1, threshold=2.2):
        self.text += ' srz'
        print "srz: %s" % self
        return self

    def srb(self, w, h, q=85, radius=0.0, amount=1.1, threshold=2.2):
        self.text += ' srb'
        print "srb: %s" % self
        return self

    def canvas(self):
        self.text += ' canvas'
        print "canvas: %s" % self
        return self

    def crop(self):
        self.text += ' crop'
        print "crop: %s" % self
        return self

    def fill(self):
        self.text += ' fill'
        print "fill: %s" % self
        return self

    def adjust(self, **adjust_props):
        self.text += ' adjust'
        print "adjust: %s" % self
        return self

    def filter(self, **filter_funcs):
        self.text += ' filter'
        print "filter: %s" % self
        return self

    def reset(self):
        self.text = ''
        pass

    def get_rest_url(self):
        return self.text.strip()

    def get_img_tag(self, **kwargs):

        img_params = ''.join([' %s="%s"' % (name, value) for name, value in kwargs.iteritems()])

        return '<img src="%s"%s>' % (self.get_rest_url(), img_params)