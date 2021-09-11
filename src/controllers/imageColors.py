from flask import Flask, request, jsonify, make_response
from flask_restx import Api, Resource
import colorgram
import webcolors
from googletrans import Translator

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
        
        actual_name_color_ptbr = None
        translator = Translator()
        if (actual_name_color_en != None):
            actual_name_color_ptbr = translator.translate(actual_name_color_en,dest='pt',src='en').text
            closest_name_color_ptbr = actual_name_color_ptbr
        else:
            closest_name_color_ptbr = translator.translate(closest_name_color_en,dest='pt',src='en').text

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

        
