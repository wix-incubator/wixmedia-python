
class WixMediaCommandException(Exception):
    pass


class WixMediaImage(object):
    COMMAND_NONE   = ""
    COMMAND_SRZ    = "srz"
    COMMAND_SRB    = "srb"
    COMMAND_CANVAS = "canvas"
    COMMAND_FILL   = "fill"
    COMMAND_CROP   = "crop"

    def __init__(self, file_uri, org_name):
        self.file_uri = file_uri
        self.org_name = org_name

        self.reset()

    def srz(self, w, h, q=85, a=1, radius=0.0, amount=1.1, threshold=2.2):
        if self.command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCommandException("Command already set: %s. Reset image before applying command." % self.command)

        self.command = WixMediaImage.COMMAND_SRZ
        self.command_params = {"w": w, "h": h,
                               "q": q, "a": a,
                               "radius": radius,
                               "amount": amount,
                               "threshold": threshold}
        return self

    def srb(self, w, h, q=85, radius=0.0, amount=1.1, threshold=2.2):
        if self.command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCommandException("Command already set: %s. Reset image before applying command." % self.command)

        self.command = WixMediaImage.COMMAND_SRB
        self.command_params = {"w": w, "h": h,
                               "q": q,
                               "radius": radius,
                               "amount": amount,
                               "threshold": threshold}
        return self

    def canvas(self, w, h, q=85, a = 1):
        if self.command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCommandException("Command already set: %s. Reset image before applying command." % self.command)

        self.command = WixMediaImage.COMMAND_CANVAS
        self.command_params = {"w": w, "h": h,
                               "q": q, "a": a}
        return self

    def crop(self, x, y, w, h, q=85):
        if self.command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCommandException("Command already set: %s. Reset image before applying command." % self.command)

        self.command = WixMediaImage.COMMAND_CROP
        self.command_params = {"x": x, "y": y,
                               "w": w, "h": h,
                               "q": q}
        return self

    def fill(self, w, h, q=85):
        if self.command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCommandException("Command already set: %s. Reset image before applying command." % self.command)

        self.command = WixMediaImage.COMMAND_FILL
        self.command_params = {"w": w, "h": h,
                               "q": q}
        return self

    def adjust(self, *props, **adjust_props):
        adjust_props.update({p: True for p in props})
        self.adjustment_params.update(adjust_props)

        return self

    def filter(self, *funcs, **filter_funcs):
        filter_funcs.update({f: True for f in funcs})
        self.filter_params.update(filter_funcs)

        return self

    def reset(self):
        self.command = WixMediaImage.COMMAND_NONE
        self.command_params = {}
        self.adjustment_params = {}
        self.filter_params = {}

    def get_rest_url(self):
        if self.command != WixMediaImage.COMMAND_NONE:
            params = [self.file_uri,
                      self.command,
                      ",".join(["%s_%s" % (key, val) for key, val in self.command_params.iteritems()])]
        else:
            params = [self.file_uri]

        if self.adjustment_params:
            params.extend(["adjust",
                           ",".join(["%s_%s" % (key, val) if val != True else key
                                      for key,val in self.adjustment_params.iteritems()])
                           ])
        if self.filter_params:
            params.extend(["filter",
                           ",".join(["%s_%s" % (key, val) if val != True else key
                                     for key,val in self.filter_params.iteritems()])
                           ])
        params.append(self.org_name)
        url = "/".join(params)
        return url

    def get_img_tag(self, **kwargs):
        img_params = ""
        if kwargs:
            img_params = ''.join([' %s="%s"' % (name, value) for name, value in kwargs.iteritems()])

        return '<img src="%s"%s>' % (self.get_rest_url(), img_params)
    
    def __str__(self):
        return "<WixMediaImage %s (%s ), command=%s [%s]>" % (self.file_uri,
                                                              self.org_name,
                                                              self.command,
                                                              self.command_params)
