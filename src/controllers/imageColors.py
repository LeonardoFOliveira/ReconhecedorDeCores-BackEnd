from flask import request, jsonify, make_response
from flask_restx import Resource
import colorgram
import webcolors

from src.server.instance import server

app, api = server.app, server.api


class ImageColorsResponse:
    def __init__(self, actual_name_color, closest_name_color):
        self.predominant_color = PredominantColor(actual_name_color,closest_name_color).__dict__

class PredominantColor:
    def __init__(self, actual_name_color, closest_name_color):
        self.actual_name_color = actual_name_color
        self.closest_name_color = closest_name_color

@api.route('/imageColors')
class ImageColors(Resource):
    def post(self,):
        fileImage = request.files['image']

        predominant_color = colorgram.extract(fileImage,1)[0]
        actual_name_color_en, closest_name_color_en = get_colour_name((predominant_color.rgb.r,predominant_color.rgb.g,predominant_color.rgb.b))
        
        blue = 'Azul'
        white = 'Branco'
        aqua = 'Água'
        beige = 'Bege'
        black = 'Preto'
        purple = 'Roxo'
        brown = 'Marrom'
        green = 'Verde'
        orange = 'Laranja'
        yellow = 'Amarelo'
        red = 'Vermelho'
        golden = 'Dourado'
        grey = 'Cinza'
        khaki = 'Caqui'
        pink = 'Rosa'
        maroon = 'Bordo'
        ## Dicionario criado baseado nas cores mapeadas no css3, e a atribuindo a um nome de cor mais amigavel e já traduzido para pt-br
        ## https://www.w3.org/TR/css-color-3/#svg-color
        color_name_dict = {
            'aliceblue': blue,
            'antiquewhite': white,
            'aqua': aqua,
            'aquamarine': aqua,
            'azure': blue,
            'beige': beige,
            'bisque': beige,
            'black': black,
            'blanchedalmond': beige,
            'blue': blue,
            'blueviolet': purple,
            'brown': brown,
            'burlywood': beige,
            'cadetblue': blue,
            'chartreuse': green,
            'chocolate': brown,
            'coral': orange,
            'cornflowerblue': blue,
            'cornsilk': yellow,
            'crimson': red,
            'cyan': aqua,
            'darkblue': blue,
            'darkcyan': aqua,
            'darkgoldenrod': golden,
            'darkgray': grey,
            'darkgreen': green,
            'darkgrey': grey,
            'darkkhaki': khaki,
            'darkmagenta': purple,
            'darkolivegreen': green,
            'darkorange': orange,
            'darkorchid': purple,
            'darkred': red,
            'darksalmon': orange,
            'darkseagreen': green,
            'darkslateblue': blue,
            'darkslategray': grey,
            'darkslategrey': grey,
            'darkturquoise': aqua,
            'darkviolet': purple,
            'deeppink': pink,
            'deepskyblue': blue,
            'dimgray': grey,
            'dimgrey': grey,
            'dodgerblue': blue,
            'firebrick': red,
            'floralwhite': white,
            'forestgreen': green,
            'fuchsia': pink,
            'gainsboro': grey,
            'ghostwhite': white,
            'gold': golden,
            'goldenrod': golden,
            'gray': grey,
            'green': green,
            'greenyellow': green,
            'grey': grey,
            'honeydew': green,
            'hotpink': pink,
            'indianred': red,
            'indigo': purple,
            'ivory': beige,
            'khaki': khaki,
            'lavender': purple,
            'lavenderblush': purple,
            'lawngreen': green,
            'lemonchiffon': yellow,
            'lightblue': blue,
            'lightcoral': orange,
            'lightcyan': aqua,
            'lightgoldenrodyellow': golden,
            'lightgray': grey,
            'lightgreen': green,
            'lightgrey': grey,
            'lightpink': pink,
            'lightsalmon': orange,
            'lightseagreen': green,
            'lightskyblue': blue,
            'lightslategray': grey,
            'lightslategrey': grey,
            'lightsteelblue': blue,
            'lightyellow': yellow,
            'lime': green,
            'limegreen': green,
            'linen': beige,
            'magenta': purple,
            'maroon': maroon,
            'mediumaquamarine': aqua,
            'mediumblue': blue,
            'mediumorchid': purple,
            'mediumpurple': purple,
            'mediumseagreen': green,
            'mediumslateblue': blue,
            'mediumspringgreen': green,
            'mediumturquoise': aqua,
            'mediumvioletred': purple,
            'midnightblue': blue,
            'mintcream': aqua,
            'mistyrose': pink,
            'moccasin': beige,
            'navajowhite': white,
            'navy': blue,
            'oldlace': beige,
            'olive': green,
            'olivedrab': green,
            'orange': orange,
            'orangered': orange,
            'orchid': purple,
            'palegoldenrod': golden,
            'palegreen': green,
            'paleturquoise': aqua,
            'palevioletred': purple,
            'papayawhip': beige,
            'peachpuff': orange,
            'peru': brown,
            'pink': pink,
            'plum': purple,
            'powderblue': blue,
            'purple': purple,
            'red': red,
            'rosybrown': brown,
            'royalblue': blue,
            'saddlebrown': brown,
            'salmon': orange,
            'sandybrown': brown,
            'seagreen': green,
            'seashell': white,
            'sienna': orange,
            'silver': grey,
            'skyblue': blue,
            'slateblue': blue,
            'slategray': grey,
            'slategrey': grey,
            'snow': white,
            'springgreen': green,
            'steelblue': blue,
            'tan': brown,
            'teal': green,
            'thistle': purple,
            'tomato': red,
            'turquoise': aqua,
            'violet': purple,
            'wheat': beige,
            'white': white,
            'whitesmoke': white,
            'yellow': yellow,
            'yellowgreen': yellow
        }

        actual_name_color_ptbr = None
        if (actual_name_color_en != None):
            actual_name_color_ptbr = color_name_dict[actual_name_color_en]
            closest_name_color_ptbr = actual_name_color_ptbr
        else:
            closest_name_color_ptbr = color_name_dict[closest_name_color_en]

        return make_response(jsonify(ImageColorsResponse(actual_name_color_ptbr,closest_name_color_ptbr).__dict__), 200)


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        Gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + Gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

        
