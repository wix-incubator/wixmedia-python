from .exceptions import WixMediaCmdNotAllowed


class WixMediaImage(object):
    COMMAND_NONE   = ""
    COMMAND_SRZ    = "srz"
    COMMAND_SRB    = "srb"
    COMMAND_CANVAS = "canvas"
    COMMAND_FILL   = "fill"
    COMMAND_CROP   = "crop"

    adjust_parameter_map = {
        "brightness": "br",
        "contrast":   "con",
        "saturation": "sat",
        "hue":        "hue",
        "vibrance":   "vib",
        "auto":       "auto"
    }

    filter_params_map = {
        "oil":            "oil",
        "negative":       "neg",
        "pixelate":       "pix",
        "pixelate-faces": "pixfs",
        "blur":           "blur",
        "unsharp":        "us",   # TODO: these command are built from 3 parameters so we need to combing and emit one in url
        "sharpen":        "shrp"  # TODO: these command are built from 3 parameters so we need to combing and emit one in url
    }

    def __init__(self, file_uri, original_filename):
        self.transform_command = None
        self.transform_params  = None
        self.adjustment_params = None
        self.filter_params     = None

        self.file_uri          = file_uri
        self.org_name          = original_filename

        self.reset()

    def reset(self):
        self.transform_command = WixMediaImage.COMMAND_NONE
        self.transform_params  = {}
        self.adjustment_params = {}
        self.filter_params     = {}

    def srz(self, width, height, quality=85, alignment=1, radius=0.5, amount=0.2, threshold=0.0):

        if self.transform_command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = WixMediaImage.COMMAND_SRZ

        self.transform_params = {
            "w":  width,
            "h":  height,
            "q":  quality,
            "a":  alignment,
            "us": "%.2f_%.2f_%.2f" % (radius, amount, threshold)
        }

        return self

    def srb(self, width, height, quality=85, radius=0.5, amount=0.2, threshold=0.0):

        if self.transform_command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = WixMediaImage.COMMAND_SRB

        self.transform_params = {
            "w":  width,
            "h":  height,
            "q":  quality,
            "us": "%.2f_%.2f_%.2f" % (radius, amount, threshold)
        }

        return self

    def canvas(self, width, height, quality=85, alignment=1):

        if self.transform_command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = WixMediaImage.COMMAND_CANVAS

        self.transform_params = {
            "w": width,
            "h": height,
            "q": quality,
            "a": alignment
        }

        return self

    def crop(self, x, y, width, height, quality=85):

        if self.transform_command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = WixMediaImage.COMMAND_CROP

        self.transform_params = {
            "w": width,
            "h": height,
            "q": quality,
            "x": x,
            "y": y
        }

        return self

    def fill(self, width, height, quality=85):

        if self.transform_command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = WixMediaImage.COMMAND_FILL

        self.transform_params = {
            "w": width,
            "h": height,
            "q": quality
        }

        return self

    def adjust(self, *props_list, **props_dict):

        self.adjustment_params.update({p: True for p in props_list})
        self.adjustment_params.update(props_dict)

        return self

    def filter(self, *funcs_list, **funcs_dict):

        self.filter_params.update({f: True for f in funcs_list})
        self.filter_params.update(funcs_dict)

        return self

    def get_rest_url(self):

        params = [self.file_uri]

        if self.transform_command != WixMediaImage.COMMAND_NONE:
            params.extend(
                [self.transform_command,
                 ",".join(["%s_%s" % (key, val) for key, val in self.transform_params.iteritems()])]
            )

        if self.adjustment_params:
            params.extend(
                ["adjust",
                 ",".join(["%s_%s" % (WixMediaImage.adjust_parameter_map.get(key, key), val) if val is not True else key
                           for key, val in self.adjustment_params.iteritems()])]
            )

        if self.filter_params:
            params.extend(
                ["filter",
                 ",".join(["%s_%s" % (WixMediaImage.filter_params_map.get(key, key), val) if val is not True else key
                          for key, val in self.filter_params.iteritems()])]
            )

        params.append(self.org_name)

        url = "/".join(params)

        return url

    def get_img_tag(self, **kwargs):
        img_params = ''.join([' %s="%s"' % (name, value) for name, value in kwargs.iteritems()])

        return '<img src="%s"%s>' % (self.get_rest_url(), img_params)
    
    def __str__(self):
        return "<WixMediaImage %s (%s ), command=%s [%s]>" % (
            self.file_uri, self.org_name, self.transform_command, self.transform_params
        )
