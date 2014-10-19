from .exceptions import WixMediaCmdNotAllowed
from .exceptions import WixMediaValueError
import os


class WixMediaImage(object):
    COMMAND_NONE      = ""
    COMMAND_SRZ       = "srz"
    COMMAND_SRB       = "srb"
    COMMAND_CANVAS    = "canvas"
    COMMAND_FILL      = "fill"
    COMMAND_CROP      = "crop"
    COMMAND_WATERMARK = "wm"

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
        "pixelate_faces": "pixfs",
        "blur":           "blur",
        "unsharp":        "us",   # TODO: these command are built from 3 parameters so we need to combing and emit one in url
        "sharpen":        "shrp"  # TODO: these command are built from 3 parameters so we need to combing and emit one in url
    }

    alignment_value_map = {
        "center":       "c",
        "top":          "t",
        "top-left":     "tl",
        "top-right":    "tr",
        "bottom":       "b",
        "bottom-left":  "bl",
        "bottom-right": "br",
        "left":         "l",
        "right":        "r",
        "face":         "f",
        "faces":        "fs"
    }

    def __init__(self, file_uri):
        """
        @param file_uri: must be of a format: http(s)://host/...
        """
        self.transform_command = None
        self.transform_params  = None
        self.adjustment_params = None
        self.filter_params     = None
        self.file_uri          = file_uri

        self.reset()

    def reset(self):
        self.transform_command = WixMediaImage.COMMAND_NONE
        self.transform_params  = {}
        self.adjustment_params = {}
        self.filter_params     = {}

    @staticmethod
    def check_param(param_name, val, type_expected, min_val=None, max_val=None):
        if val is not None:

            if type(val) is not type_expected:
                raise WixMediaValueError('"%s" should be of type %s. type received: %s' % ( param_name, str(type_expected), str(type(val))))

            if min_val is not None and max_val is not None:
                if val > max_val or val < min_val:
                    raise WixMediaValueError("'%s' parameter's value should be between %s to %s. Value received: %s" % (param_name, str(min_val), str(max_val), str(val)))

            elif min_val is not None:
                if val < min_val:
                    raise WixMediaValueError("'%s' parameter's value should be above %s. Value received: %s" % (param_name, str(min_val), str(val)))

            elif max_val is not None:
                if val > max_val:
                    raise WixMediaValueError("'%s' parameter's value should be under %s. Value received: %s" % (param_name, str(max_val), str(val)))

            if param_name == 'alignment':
                if val not in WixMediaImage.alignment_value_map.keys():
                    raise WixMediaValueError("'alignment' parameter's value should be a String from the expected position-describing strings. Received: %s" % val)

    @staticmethod
    def check_transform_params(width, height, quality=None, alignment=None, radius=None, amount=None, threshold=None, x=None, y=None):
        check = WixMediaImage.check_param
        check('width', width, int, 0)
        check('height', width, int, 0)
        check('quality', quality, int, 0, 100)
        check('alignment', alignment, str)
        check('radius', radius, float)
        check('amount', amount, float)
        check('threshold', threshold, float)
        check('x', x, int, 0)
        check('y', y, int, 0)

    @staticmethod
    def check_watermark_params(opacity=None, alignment=None, scale=None):
        check = WixMediaImage.check_param
        check('opacity', opacity, int, 0, 100)
        check('scale', scale, int, 0, 100)
        check('alignment', alignment, str)


    def srz(self, width, height, quality=None, alignment=None, radius=None, amount=None, threshold=None):
        '''
        default values: quality=75, alignment="center", radius=0.5, amount=0.2, threshold=0.0
        '''

        if self.transform_command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = WixMediaImage.COMMAND_SRZ

        WixMediaImage.check_transform_params(width, height, quality, alignment, radius, amount, threshold)

        self.transform_params = {
            "w":  width,
            "h":  height
        }

        if quality is not None:
            self.transform_params["q"] = quality

        if alignment:
            self.transform_params["a"] = WixMediaImage.alignment_value_map[alignment]

        if radius or amount or threshold:
            radius    = radius or 0.5
            amount    = amount or 0.2
            threshold = threshold or 0.0

            self.transform_params["us"] = "%.2f_%.2f_%.2f" % (radius, amount, threshold)

        return self

    def srb(self, width, height, quality=None, radius=None, amount=None, threshold=None):
        '''
        default values: quality=75, radius=0.5, amount=0.2, threshold=0.0
        '''

        if self.transform_command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = WixMediaImage.COMMAND_SRB

        WixMediaImage.check_transform_params(width, height, quality, radius=radius, amount=amount, threshold=threshold)

        self.transform_params = {
            "w":  width,
            "h":  height
        }

        if quality is not None:
            self.transform_params["q"] = quality

        if radius or amount or threshold:
            radius    = radius or 0.5
            amount    = amount or 0.2
            threshold = threshold or 0.0

            self.transform_params["us"] = "%.2f_%.2f_%.2f" % (radius, amount, threshold)

        return self

    def canvas(self, width, height, quality=None, alignment=None):
        '''
        default values: quality=75, alignment="center"
        '''

        if self.transform_command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = WixMediaImage.COMMAND_CANVAS

        WixMediaImage.check_transform_params(width, height, quality=quality, alignment=alignment)

        self.transform_params = {
            "w": width,
            "h": height
        }

        if quality is not None:
            self.transform_params["q"] = quality

        if alignment:
            self.transform_params["a"] = WixMediaImage.alignment_value_map[alignment]

        return self

    def crop(self, x, y, width, height, quality=None):
        '''
        default value: quality=75
        '''

        if self.transform_command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = WixMediaImage.COMMAND_CROP

        WixMediaImage.check_transform_params(width, height, quality=quality, x=x, y=y)

        self.transform_params = {
            "w": width,
            "h": height,
            "x": x,
            "y": y
        }

        if quality is not None:
            self.transform_params["q"] = quality

        return self

    def fill(self, width, height, quality=None):
        '''
        default value: quality=75
        '''

        if self.transform_command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = WixMediaImage.COMMAND_FILL

        WixMediaImage.check_transform_params(width, height, quality=quality)

        self.transform_params = {
            "w": width,
            "h": height
        }

        if quality is not None:
            self.transform_params["q"] = quality

        return self

    def watermark(self, opacity=None, alignment=None, scale=None):
        '''
        default values: opacity=100, alignment='center', scale=0
        '''
        if self.transform_command != WixMediaImage.COMMAND_NONE:
            raise WixMediaCmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = WixMediaImage.COMMAND_WATERMARK

        WixMediaImage.check_watermark_params(opacity, alignment, scale)

        self.transform_params = {}

        if opacity is not None:
            self.transform_params["op"] = opacity

        if alignment:
            self.transform_params["a"] = WixMediaImage.alignment_value_map[alignment]

        if scale is not None:
            self.transform_params["scl"] = scale

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

        file_uri_path, org_file_name = os.path.split(self.file_uri)
        params = [file_uri_path]

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

        params.append(org_file_name)

        url = "/".join(params)

        return url

    def get_img_tag(self, **kwargs):
        img_params = ''.join([' %s="%s"' % (name, value) for name, value in kwargs.iteritems()])

        return '<img src="%s"%s>' % (self.get_rest_url(), img_params)
    
    def __str__(self):
        return "<WixMediaImage %s, command=%s [%s]>" % (
            self.file_uri, self.transform_command, self.transform_params
        )
