from random import randint


def color_outfit(closet, color):
    color_closet = {key: [piece for piece in closet[key] if piece['primaryColor'] == color] for key in closet.keys()}
    # print(color_closet)
    outfit_result1 = {key: color_closet[key][randint(0, len(color_closet[key])-1)]['id'] for key in
                      color_closet.keys()}
    outfit_result2 = {key: color_closet[key][randint(0, len(color_closet[key]) - 1)]['id'] for key in
                      color_closet.keys()}
    outfit_result3 = {key: color_closet[key][randint(0, len(color_closet[key]) - 1)]['id'] for key in
                      color_closet.keys()}
    return [outfit_result1, outfit_result2, outfit_result3]


def theme_outfit(closet, theme):
    guide = {'EARTH': [(145, 109, 51), (70, 140, 50)], 'GOTH': [(0, 0, 0)]}
    return [{
        'headWear': pick_piece(closet['headWear'], guide[theme]),
        'tops': pick_piece(closet['tops'], guide[theme]),
        'bottoms': pick_piece(closet['bottoms'], guide[theme]),
        'shoes': pick_piece(closet['shoes'], guide[theme]),
        'accessories': pick_piece(closet['accessories'], guide[theme]),
        'outerWear': pick_piece(closet['outerWear'], guide[theme])
    } for i in range(0, 3)]


def pick_piece(drawer, colors):
    if colors == [(0, 0, 0)]:
        return pick_piece_goth(drawer)

    drawer_diffs = {piece['id']: [1000, piece] for piece in drawer}
    for i_d in drawer_diffs:
        drawer_diffs[i_d][0] = min(color_diff(drawer_diffs[i_d][1]['averageColor'], color) for color in colors)
    choice = min(drawer_diffs, key=lambda key: drawer_diffs[key][0])
    drawer.remove(drawer_diffs[choice][1])
    return choice


def pick_piece_goth(drawer):
    drawer_spread = {piece['id']: [1000, piece] for piece in drawer}
    for i_d in drawer_spread:
        drawer_spread[i_d][0] = sum([
            abs(drawer_spread[i_d][1]['averageColor'][0] - drawer_spread[i_d][1]['averageColor'][1]),
            abs(drawer_spread[i_d][1]['averageColor'][1] - drawer_spread[i_d][1]['averageColor'][2]),
            abs(drawer_spread[i_d][1]['averageColor'][2] - drawer_spread[i_d][1]['averageColor'][0])
        ])
    # print(drawer_spread)
    return min(drawer_spread, key=lambda key: drawer_spread[key][0])


def color_diff(piece_color, color):
    return sum(abs(color[i] - piece_color[i]) for i in range(0, 3))
