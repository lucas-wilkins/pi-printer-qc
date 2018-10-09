import re

def get_image_positions(gcode_filename, x_name="U", y_name="Y"):
    fid = open(gcode_filename)
    positions = []
    for line in fid:
        if re.match(r"\s*G[01].*", line) is not None:
            tokens = re.split(r"\s+", line)
            u = None
            y = None
            for token in tokens:
                if token.startswith(x_name):
                    u = float(token[1:])
                elif token.startswith(y_name):
                    y = float(token[1:])

            if u is not None and y is not None:
                positions.append((u,y))

    print("Found positions for %i photos"%len(positions))
    return positions

def get_grid_size(gcode_filename, x_name="U", y_name="Y"):
    positions = get_image_positions(gcode_filename, x_name, y_name)

    ys_from_x = {}
    xs_from_y = {}

    def add_value(dic, key, val):
        if key in dic:
            dic[key].append(val)
        else:
            dic[key] = [val]


    for x, y in positions:
        add_value(ys_from_x, x, y)
        add_value(xs_from_y, y, x)

    # Check for consistency
    nx = len(ys_from_x)
    ny = len(xs_from_y)

    for val in xs_from_y.values():
        if len(val) != nx:
            raise ValueError("GCode does not define a square grid of points")

    for val in ys_from_x.values():
        if len(val) != ny:
            raise ValueError("GCode does not define a square grid of points")


    width = max(ys_from_x.keys()) - min(ys_from_x.keys())
    height = max(xs_from_y.keys()) - min(xs_from_y.keys())

    width, height = nx*width/(nx-1), ny*height/(ny-1)

    x_offset_mm = min(ys_from_x.keys()) - (0.5*width/nx)
    y_offset_mm = min(xs_from_y.keys()) - (0.5*width/ny)

    print("Grid is %i photos by %i photos, and %gmm by %gmm" % (nx, ny, width, height))

    return nx, ny, x_offset_mm, y_offset_mm, width, height

