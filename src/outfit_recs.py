from random import randint


def color_outfit(closet, color):
    color_closet = {key: [piece for piece in closet[key] if piece['primaryColor'] == color] for key in closet.keys()}
    print(color_closet)
    outfit_result = {key: color_closet[key][randint(0, len(color_closet[key])-1)] for key in color_closet.keys()}
    return outfit_result
