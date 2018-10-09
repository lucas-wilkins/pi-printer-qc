from typing import List, Tuple

import re


flt = "[-+]?[0-9]*\.?[0-9]+"

class DynamicPosition:
    """ This class keeps track of the positions of the head, so that we always know the XYZE coordinates,
    even if they are not specidied in a particular G statement."""


    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.e = None

        self.last_x = 0.0
        self.last_y = 0.0

    def reset(self):
        self.x = None
        self.y = None
        self.z = None
        self.e = None

    def set_value(self, name, value):
        if name == "X":
            self.x = value
            self.last_x = value
        elif name == "Y":
            self.y = value
            self.last_y = value
        elif name == "Z":
            self.z = value
        elif name == "E":
            self.e = value
        else:
            pass

    @property
    def is_extruding(self):
        """ We use this property to determine whether movements of the head are printed or not"""
        if self.z is None:
            if self.e is not None and self.e > 0:
                return True
        return False

    def new_arrays(self):
        """Helper function"""
        return [self.last_x], [self.last_y]

    def append_to_lists(self, x_data, y_data):
        """ Adds a point to the list, fills in x and y if it was not specified"""
        if self.x is not None or self.y is not None:
            if self.x is not None:
                x_data.append(self.x)
            else:
                x_data.append(x_data[-1])

            if self.y is not None:
                y_data.append(self.y)
            else:
                y_data.append(y_data[-1])



class Printer:
    """ Model of the printers output. """
    def __init__(self):

        self.x_data = []
        self.y_data = []
        self.layer_ids = []

    def parse_code(self, filename):

        dynamic_position = DynamicPosition()
        current_layer = 0

        current_x, current_y = dynamic_position.new_arrays()
        self.layer_ids = [current_layer]


        fid = open(filename, 'r')
        for line in fid:
            # Absolute movement with G1
            # G1 [AXIS][POSITION]
            # Extruder, is E
            m = re.match(r"\s*G[01].*", line)
            if m is not None:

                dynamic_position.reset()

                stripped = line.strip()
                tokens = re.split(r"\s+", stripped)
                for token in tokens[1:]:
                    dynamic_position.set_value(token[0], float(token[1:]))

                if dynamic_position.is_extruding:
                    dynamic_position.append_to_lists(current_x, current_y)
                else:
                    if len(current_x) > 1:
                        self.x_data.append(current_x)
                        self.y_data.append(current_y)
                        self.layer_ids.append(current_layer)

                    current_x, current_y = dynamic_position.new_arrays()

            # Layer specifying comments
            m = re.match(";LAYER:.*", line)
            if m is not None:
                current_layer = int(line[7:])

            # Other Comments
            if line.startswith(";"):
                pass

        self.x_data.append(current_x)
        self.y_data.append(current_y)


    def show_work(self):
        """ Plot using matplotlib"""
        import matplotlib.pyplot as plt

        for x,y,layer in zip(self.x_data, self.y_data, self.layer_ids):
            s = (layer%5)*0.2
            color = [s, 1-s, 0.2]
            plt.plot(x,y, color=color)
        plt.show()

    @property
    def max_layer(self):
        """ Largest layer index (number of layers - 1)"""
        return max(self.layer_ids)

    def layers(self) -> List[List[Tuple[List[float], List[float]]]]:
        all = [[] for i in range(self.max_layer+1)]

        for x, y, layer in zip(self.x_data, self.y_data, self.layer_ids):
            all[layer].append((x, y))

        return all


if __name__ == "__main__":

    printer = Printer()
    printer.parse_code("test_data/CFDMP_test.gcode")

    layers = printer.layers()

    print("Found %i layers"%(printer.max_layer+1))

    print("%i sections"%len(printer.x_data))
    print("%i layer_ids"%len(printer.layer_ids))

    #from util import layer_length
    #for layer in layers:
    #    print(layer_length(layer))

    import matplotlib.pyplot as plt
    d1, d2 = 5, 4
    for i in range(d1):
        for j in range(d2):
            ind = d1 * j + i
            plt.subplot(d1, d2, ind+1)
            try:
                for x, y in layers[ind]:
                    plt.plot(x,y,color='k')
                    plt.xlim([70,170])
                    plt.ylim([75,125])
            except:
                pass


    plt.show()





