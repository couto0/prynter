import re

def gen_layer(x, y, z, e, v):
    """
    Turn coordinates into gcode
    ARGS:
    x: x array (array)
    y: y array (array)
    z: height (float)
    e: extrusion array (array)
    v: speed (float)

    RETURNS:
    Gcode string (str)
    """
    layer = []
    layer.append('G1 Z{0:.3f} F{1:.3f}\n'.format(z, v))
    layer.append('G1 X{0:.3f} Y{1:.3f}\n'.format(x[0], y[0]))
    layer.append('M101\n')
    layer.append('G1 E0.0000\n')
    layer.append('G92 E0.0000\n')
    for i in range(len(x)-1):
        layer.append('G1 X{0:.3f} Y{1:.3f} E{2:.4f}\n'.format(x[i+1], y[i+1], e[i+1]))
    layer.append('M102\n')
    layer.append('G92 E0.0000\n')
    layer.append('G1 E-0.5000\n')
    layer.append('M103\n')
    layer = "".join(layer)
    return layer

def gen_layer2(x, y, z, e, v):
    """
    Turn coordinates into gcode
    ARGS:
    x: x array (array)
    y: y array (array)
    z: height (float)
    e: extrusion array (array)
    v: speed (float)

    RETURNS:
    Gcode string (str)
    """
    layer = []
    layer.append('G92 E0.0000\n')
    layer.append('M106 S255\n')
    layer.append('G1 Z{0:.3f} F{1:.3f}\n'.format(z, v))
    layer.append('G1 X{0:.3f} Y{1:.3f}\n'.format(x[0], y[0]))
    for i in range(len(x)-1):
        layer.append('G1 X{0:.3f} Y{1:.3f} E{2:.4f}\n'.format(x[i+1], y[i+1], e[i+1]))
    layer = "".join(layer)
    return layer

def output_gcode(layers, output_name, header, footer):
    """
    Generates the final gcode file

    ARGS:
    layers: list containing all layers (str)
    output_name: output file name (str)
    header: gcode file header (str)
    footer: gcode file footer (str)

    """
    with open(output_name + '.gcode', 'w') as f:
        f.write(header)
        for layer in layers:
            f.write(layer)
        f.write(footer)


G1 = re.compile("G[1]",        re.IGNORECASE)
M = re.compile("M103",         re.IGNORECASE)
X = re.compile("X(\d+\.?\d*)", re.IGNORECASE)
Y = re.compile("Y(\d+\.?\d*)", re.IGNORECASE)
Z = re.compile("Z(\d+\.?\d*)", re.IGNORECASE)
E = re.compile("E(\d+\.?\d*)", re.IGNORECASE)



def parse_gcode(filename):
    """
    Turns a gcode file into a gcode object, containing the coordinate arrays

    ARGS:
    filename: gcode filename (str)

    RETURNS:
    Tuple containing the arrays, and the original gcode string
    """
    with open(filename, 'r') as f:
        gcode = f.readlines()

    z0 = 0
    layer_counter = 0
    move_counter = 0
    gcode_object = [[0, [[],[],[],[]]]]

    for line_counter in range(len(gcode)):
        line = gcode[line_counter]
        if G1.match(line):
            if Z.search(line):
                z = float(Z.findall(line)[0])
                if z != z0:
                    layer_counter += 1
                    move_counter = 0
                    gcode_object.append([z, [[], [], [], []]])
                z0 = z
            if X.search(line):
                x = float(X.findall(line)[0])
                y = float(Y.findall(line)[0])
                #e = float(E.findall(line)[0])
                gcode_object[layer_counter][move_counter+1][0].append(line_counter)
                gcode_object[layer_counter][move_counter+1][1].append(x)
                gcode_object[layer_counter][move_counter+1][2].append(y)
                #gcode_object[layer_counter][move_counter+1][3].append(e)
        if M.match(line):
            move_counter += 1
            gcode_object[layer_counter].append([[],[],[],[]])

    return gcode_object, gcode
