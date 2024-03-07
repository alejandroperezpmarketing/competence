import json
import os
import random
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import webbrowser

import folium
import pyproj

import lab_4

import utilities


class Vector():

    # Constructor
    def __init__(self, geometry='point'):

        # Attributes

        if geometry.upper() not in ['POINT', 'LINE', 'POLYLINE', 'POLYGON']:
            self._geometry = None
        else:
            self._geometry = geometry
        
        self._source = None
        self._format = None
        self._epsg = None
        self._coordinates = []
        self._attributes = []
        self._bbox = None

        self._screen = {
            'transform': None,
            'coordinates': []
        }


    def __repr__(self):

        report = {
            'geometry': self._geometry,
            'source': self._source,
            'format': self._format,
            'epsg': self._epsg,
            'coordinates': len(self._coordinates),
            'attributes': len(self._attributes),
            'bbox': self._bbox,
            'transform': self._screen['transform']
        }

        return json.dumps(report, indent=4)


    # Properties

    def _set_epsg(self, code):

        self._epsg = code

    def _get_epsg(self):

        return self._epsg

    epsg = property(fget=_get_epsg, fset=_set_epsg)


    def _get_fields(self):


        fields = list(self._attributes[0].keys())

        return fields

    fields = property(fget=_get_fields)
    


    def _get_attributes(self):

        return self._attributes

    attributes = property(fget=_get_attributes)
    
    def _get_coordinates(self):

        return self._coordinates

    coordinates = property(fget=_get_coordinates)




    
    # Protected methods


    def _read_point_xy_csv(self, header, data, id_field, xy_field, separator, xy):

        # Inits
        
        id_index = None
        xy_index = None

        for field_index, field_name in enumerate(header):

            if field_name == id_field:
                id_index = field_index
            elif field_name == xy_field:
                xy_index = field_index

        if id_index is None or xy_index is None:
            # Bad parameters passed by user
            return


        # Data processing

        for count, record in enumerate(data):

            # Init
            
            attributes = {}

            # Split records in separate field values

            field_values = record.strip().split(separator)

            # Assign special fields: ID, X, Y

            record_id = field_values[id_index]

            if xy is True:
                x, y = list(map(float, field_values[xy_index].split(',')))
            elif xy is False:
                y, x = list(map(float, field_values[xy_index].split(',')))

            # Assign other fields ~ regular attributes
            
            for field_index, field_value in enumerate(field_values):

                # Do not process id_field, xy_field
                if field_index == id_index or field_index == xy_index:
                    continue

                attributes[header[field_index]] = field_value

            # Store in memory

            self._coordinates.append([x,y])
            self._attributes.append(attributes)
        

        # Other instance attributes
        
        self._format = 'CSV'
        self._source = 'file'
            
        
        


    # User methods


    def random_points(self, number_of_points, x_min, y_min, x_max, y_max, filename=False):

        # NOTE: this method overwrites previous contents !!!

        delta_x = x_max - x_min
        delta_y = y_max - y_min
            
        coordinates = []
        attributes = []
        
        for point_number in range(number_of_points):
            
            x_random = x_min + random.random() * delta_x
            y_random = y_min + random.random() * delta_y

            coordinates.append([x_random, y_random])
            
            attributes.append({'id': point_number})

        self._geometry = 'point'
        self._source = 'random' # file, digit, random
        self._format = 'list'
        self._coordinates = coordinates
        self._attributes = attributes

        if filename is True:

            tkinter.Tk().withdraw()
            filename = tkinter.filedialog.asksaveasfilename(
                title='Select output CSV file',
                filetypes=[('CSV files', '*.csv *.CSV')]
            )

            if filename == '':
                return

            with open(filename, 'wt') as csv_file:

                csv_file.write('id,x,y\n')

                for count, point in enumerate(coordinates):
                    
                    x, y = point
                    csv_file.write(f'{count},{x},{y}\n')





    def read_csv(self, id_field, x_field, y_field, separator=',', xy=True):

        root = tkinter.Tk().withdraw()
        filename = tkinter.filedialog.askopenfilename(
            title='Select CSV file',
            filetypes=[('CSV Files', '*.csv *.CSV')]
        )

        if not filename:
            return

        # Read file contents (context manager)
        # 'rt' = read, text
        
        with open(filename, 'rt', encoding='utf-8-sig') as csv_file:
            data = csv_file.readlines()


        # Header

        header = data[0].strip().split(separator)

        # Check fields exist

        if id_field not in header:
            tkinter.messagebox.showerror(
                'PROG', f'Field name not found [{id_field}]'
            )
            return
        
        if x_field not in header:
            tkinter.messagebox.showerror(
                'PROG', f'Field name not found [{x_field}]'
            )
            return        
        
        if y_field not in header:
            tkinter.messagebox.showerror(
                'PROG', f'Field name not found [{y_field}]'
            )
            return        
            
        if x_field == y_field:
            if self._geometry == 'point':
                self._read_point_xy_csv(header, data[1:], id_field, x_field, separator, xy)
        else:
            if self._geometry == 'point':
                self._read_point_csv()

        

    def bounding_box(self):

        # Assume XY !

        if len(self._coordinates) == 0:
            # Message box??
            return

        if self._geometry == 'point':

            # Init

            x_min, y_min = self._coordinates[0]
            x_max, y_max = self._coordinates[0]

            for point in self._coordinates:

                x, y = point

                if x < x_min:
                    x_min = x
                elif x > x_max:
                    x_max = x

                if y < y_min:
                    y_min = y
                elif y > y_max:
                    y_max = y

            self._bbox = [x_min, y_min, x_max, y_max]

        elif self._geometry == 'polyline':

            x_min, y_min = self._coordinates[0][0]
            x_max, y_max = self._coordinates[0][0]

            for polyline in self._coordinates:
                for point in polyline:

                    x, y = point

                    if x < x_min:
                        x_min = x
                    elif x > x_max:
                        x_max = x

                    if y < y_min:
                        y_min = y
                    elif y > y_max:
                        y_max = y

            self._bbox = [x_min, y_min, x_max, y_max]

        elif self._geometry == 'polygon':

            x_min, y_min = self._coordinates[0][0][0]
            x_max, y_max = self._coordinates[0][0][0]

            for polygon in self._coordinates:
                for part in polygon:
                    for point in part:

                        x, y = point

                        if x < x_min:
                            x_min = x
                        elif x > x_max:
                            x_max = x

                        if y < y_min:
                            y_min = y
                        elif y > y_max:
                            y_max = y

            self._bbox = [x_min, y_min, x_max, y_max]



    def describe_geojson(self):

        root = tkinter.Tk().withdraw()
        filename = tkinter.filedialog.askopenfilename(
            title='Select GeoJSON file',
            filetypes=[('GeoJSON Files', '*.geojson *.json')]
        )

        if not filename:
            return

        report = lab_4._describe_geojson(filename)

        return report

        
    def read_geojson(self, geometry='point'):

        if geometry.lower() not in ['point', 'polyline', 'polygon']:
            return

        tkinter.Tk().withdraw()
        filename = tkinter.filedialog.askopenfilename(
            title='Select GeoJSON file',
            filetypes=[('GeoJSON Files', '*.geojson *.json')]
        )

        if not filename:
            return

        coordinates, attributes = lab_4._read_geojson(filename, geometry)

        #print(coordinates)

        self._coordinates = coordinates
        self._attributes = attributes

        self._source = 'file'
        self._format = 'GeoJSON'
        self._epsg = 4326

        self._geometry = geometry.lower()



    # 08/11/2023
    
    def add_field(self, field_name, field_value=None):

        if field_name == 'id':
            return

        if len(self._coordinates) == 0:
            return

        if field_name in self.fields:

            # Overwrite or not overwrite ?
            # Warning
            pass

        for record in self._attributes:
            record[field_name] = field_value

        

        
            
            
    # 10/11/2023

    def set_field_value(self, record_number, field_name, field_value):

        if field_name == 'id':
            return

##        if len(self._coordinates) == 0:
        if len(self._attributes) == 0:
            return

        try:
            self._attributes[record_number][field_name] = field_value
        except:
            return


    def _project_points(self, projection):

        projected_points = []

        for coordinates in self._coordinates:

            x, y = coordinates

            x_projected, y_projected = projection.transform(x, y)

            projected_points.append([x_projected, y_projected])

        return projected_points


    def _project_polyline(projection):
        pass


    def _project_polygon(projection):
        pass
        
    def project(self, target_epsg):

        if self._epsg is None:
            tkinter.Tk().withdraw()
            tkinter.messagebox.showerror('PROG', 'Unkonwn source EPSG code')
            return

        if self._epsg == target_epsg:
            return

        # Source and target CRS
        
        try:
            source_crs = pyproj.CRS.from_epsg(self._epsg)
        except:
            tkinter.Tk().withdraw()
            tkinter.messagebox.showerror('PROG', 'Unkonwn source EPSG code')
            return            

        try:
            target_crs = pyproj.CRS.from_epsg(target_epsg)
        except:
            tkinter.Tk().withdraw()
            tkinter.messagebox.showerror('PROG', 'Unkonwn target EPSG code')
            return

        # Transformer

        projection = pyproj.Transformer.from_crs(
            source_crs, target_crs, always_xy=True
        )

        # Transformation

        if self._geometry == 'point':
            projected = self._project_points(projection)
        elif self._geometry == 'polyline':
            pass
        elif self._geometry == 'polygon':
            pass

        self._coordinates = projected
        self._epsg = target_epsg


    def _create_osm_point_layer(self, coordinates, attributes, colour, size):

        # Folium !!!!!!

        osm_layer = folium.FeatureGroup(name='osm')

        if colour is None:
            colour = 'blue'

        if size is None:
            size = 4


        for count, geometry in enumerate(coordinates):

            longitude, latitude = geometry

            # Attributes

            osm_popup_text = ''

            for field, value in attributes[count].items():

                osm_popup_text += field.upper() + ': '
                osm_popup_text += str(value) + '<br>'

            osm_popup = folium.Popup(osm_popup_text, max_width=500)

            osm_marker = folium.CircleMarker(
                location=[latitude, longitude],
                popup=osm_popup,
                radius=size,
                color=colour,
                fill=True,
                fill_color=colour,
                fill_opacity=0.4
            )

            osm_layer.add_child(osm_marker)

        return osm_layer

            

    def _show_osm_map(self, layers):
        
        osm_map = folium.Map()

        for layer in layers:
            osm_map.add_child(layer)


        osm_map.fit_bounds(
            osm_map.get_bounds()
        )


        filename = 'osm.html'
        
        osm_map.save(filename)

        webbrowser.open(
            os.path.abspath(filename)
        )

        
            
        
    def osm(self, colour=None, size=None):

        if len(self._coordinates) == 0:
            return

        if self._epsg == 4326 or self._epsg == 4258:
            transform = None
        elif self._epsg is None:
            return
        else:
            pass

        if self._geometry == 'point':
            
            if transform is None:

                coordinates_4326 = self._coordinates

            else:

                coordinates_4326 = None


            osm_layer = self._create_osm_point_layer(
                coordinates_4326, self._attributes, colour, size
            )

        elif self._geometry == 'polyline':
            pass
        elif self._geometry == 'polygon':
            pass

        self._show_osm_map([osm_layer])

        # [osm_layer] = list of Folium layers
        
            
    def read_vlc_opendatasoft(self, dataset_id, version=2.1, valid_attributes=None):

##        print('read_vlc_opendatasoft()')



        # Get dataset from opendatasoft server

        dataset = utilities.get_vlc_opendatasoft_dataset(
            dataset_id, version=version
        )

        if dataset is None:
            # Warning
            return

        # Extract information from GeoJSON dictionary

        coordinates = []
        attributes = []

        for feature in dataset['features']:

            # Check geometry types match!!

            if feature['geometry']['type'].lower() != self._geometry:
                continue

            coordinates.append(feature['geometry']['coordinates'])


            # Discuss attributes

            if valid_attributes is None:

                attributes.append(feature['properties'])

            else:

                feature_attribute_names = list(feature['properties'].keys())

##                print(feature_attribute_names)

                feature_attributes = {}

                for attribute_name in valid_attributes:

                    if attribute_name in feature_attribute_names:

                        attribute_value = feature['properties'][attribute_name]

                        feature_attributes[attribute_name] = attribute_value

                
                attributes.append(feature_attributes)    


        # Update instance information
        
        self._coordinates = coordinates
        self._attributes = attributes

        self._source = 'online'
        self._format = 'GeoJSON'
        self._epsg = 4326


        


        

        
        

        
    

        



class Screen():

    def __init__(self, rows=600, columns=800, background='black'):

        self._columns = columns
        self._rows = rows
        
        self._root = tkinter.Tk()

        self._root.title('PROG')
        self._root.resizable(False, False)

        self._canvas = tkinter.Canvas(
            self._root, width=self._columns, height=self._rows, bg=background,
            borderwidth = 0, highlightthickness = 0
        )

        self._canvas.pack()


        # System bindings

        self._root.bind('<F1>', self._help)
##        self._root.bind('<F2>', self._state_of_the_app)

        self._root.bind('<F9>', self._start_digit)
        self._root.bind('<F10>', self._stop_digit)
        self._root.bind('<F11>', self._digit_repr)
        self._root.bind('<F12>', self._digit_out)
        
##        self._root.bind('<Shift-F5>', self._image_epsg)
        self._root.bind('<Shift-F6>', self._points_epsg)
##        self._root.bind('<Shift-F7>', self._polylines_epsg)
##        self._root.bind('<Shift-F8>', self._polygons_epsg)

        self._root.bind('<Control-F6>', self._points_repr)
        self._root.bind('<Control-F7>', self._polylines_repr)
##        self._root.bind('<Control-F8>', self._polygons_repr)
##        self._root.bind('<Control-F9>', self._digit_repr)

        self._root.bind('<Shift-F9>', self.zoom_extent)


        # Datasets

        self._digit = Vector(geometry='point')
        
        self._points = Vector(geometry='point')
        self._polylines = Vector(geometry='polyline')
        self._polygons = Vector(geometry='polygon')
        
        self._image = Raster()




    # Protected methods

    def _help(self, event):
        
        help_text = 'F1: Help\n\n'
        
        help_text += 'F5: Read image\n'
        help_text += 'F6: Read points\n'
        help_text += 'F7: Read polylines\n'
        help_text += 'F8: Read polygons\n\n'

        help_text += 'F9: Start digitising points\n'
        help_text += 'F10: Stop digitising points\n'
        help_text += 'F11: Digit coordinates and attributes\n'

        help_text += 'Shift-F5: Image EPSG code\n'
        help_text += 'Shift-F6: Points EPSG code\n'
        help_text += 'Shift-F7: Polylines EPSG code\n'
        help_text += 'Shift-F8: Polygons EPSG code\n\n'
        
        help_text += 'Control-F2: Clear screen\n\n'

        help_text += 'Control-F5: Print image properties\n'
        help_text += 'Control-F6: Print points properties\n'
        help_text += 'Control-F7: Print polylines properties\n'
        help_text += 'Control-F8: Print polygons properties\n'


        print(help_text)



    def _start_digit(self, event):
        
        self._root.bind('<Button-1>', self._get_point)
        self.cursor('tcross')


    def _stop_digit(self, event):
        
        self._root.unbind('<Button-1>')
        self.cursor()


    def _get_point(self, event):

        if self._digit._source is None:
            self._digit._source = 'digit'

        point = [event.x, event.y]
        count = len(self._digit._coordinates)
        self._digit._coordinates.append(point)
        self._digit._attributes.append({'id': count})
        
        self.draw_point(point)


    def _image_epsg(self, event):

        epsg = tkinter.simpledialog.askinteger(
            title='PROG', prompt='Image EPSG code'
        )

        if epsg is None:
            return

##        if utilities._check_epsg(epsg) is False:
##            return
        
        self._image.epsg = epsg

    
    def _points_epsg(self, event):

        epsg = tkinter.simpledialog.askinteger(
            title='PROG', prompt='Points EPSG code'
        )

        if epsg is None:
            return

##        if utilities._check_epsg(epsg) is False:
##            return
        
        self._points.epsg = epsg


    def _polylines_epsg(self, event):

        epsg = tkinter.simpledialog.askinteger(
            title='PROG', prompt='Polylines EPSG code'
        )

        if epsg is None:
            return

##        if utilities._check_epsg(epsg) is False:
##            return
        
        self._polylines.epsg = epsg


    def _polygons_epsg(self, event):

        epsg = tkinter.simpledialog.askinteger(
            title='PROG', prompt='Polygons EPSG code'
        )

        if epsg is None:
            return

##        if utilities._check_epsg(epsg) is False:
##            return
        
        self._polygons.epsg = epsg
        

    def _digit_repr(self, event):
        print(self._digit)


    def _points_repr(self, event):
        print(self._points)


    def _polylines_repr(self, event):
        print(self._polylines)


    def _polygons_repr(self, event):
        print(self._polygons)


    def _digit_out(self, event):

        for count, point in enumerate(self._digit._coordinates):

            attributes = self._digit._attributes[count]
            
            print(point, attributes)

        
    def _draw_single_point(self, point, size, colour, tag):
        """Draws a single point on the Screen() canvas"""

        x, y = point

        x_min = x - size
        y_min = y - size
        x_max = x + size
        y_max = y + size

        self._canvas.create_rectangle(
            x_min, y_min, x_max, y_max,
            fill=colour, tag=tag
        )


    def _draw_single_polyline(self, polyline, thickness, colour, tag):
        """Draws a single point on the Screen() canvas"""

        self._canvas.create_line(
            polyline, fill=colour, width=thickness, tag=tag
        )


    def _draw_single_polygon(self, polygon, size, color, tag):
        """Draws a single point on the Screen() canvas"""

        # TODO



    # Properties

    def _get_digit(self):
        return self._digit

    digit = property(fget=_get_digit)


    def _get_points(self):
        return self._points

    points = property(fget=_get_points)


    def _get_polylines(self):
        return self._polylines

    polylines = property(fget=_get_polylines)


    def _get_polygons(self):
        return self._polygons

    polygons = property(fget=_get_polygons)


    def _get_image(self):
        return self._image

    image = property(fget=_get_image)




        

    
    # User Screen() methods
    
    def loop(self):
        self._root.mainloop()


    def keyboard_bind(self, event, function):
        self._root.bind(event, function)


    def mouse_bind(self, event, function):
        self._canvas.bind(event, function)


    def cursor(self, shape='left_ptr'):
        self._canvas.config(cursor=shape)


    def delete(self, tag):
        self._canvas.delete(tag)


    def clear(self):
        self._canvas.delete('all')

        self._digit.reset()
        
        self._points.reset()
        self._polylines.reset()
        self._polygons.reset()
        
        #self._image.reset()



    # User graphical methods
    
    
    def add_vector(self, vector):

        if type(vector).__name__ != 'Vector':
            return
        
        if vector.geometry == 'point':
            self._points = vector

    
    def draw_point(self, point, size=3, colour='white', tag='point'):
        """Draws a single point on the Screen() canvas"""

        self._draw_single_point(point, size, colour, tag)


    def draw_polyline(self, polyline, thickness=2, colour='white', tag='polyline'):
        """Draws a single polyline on the Screen() canvas"""

        self._draw_single_polyline(polyline, thickness, colour, tag)
        
    def draw_polygon(self, point, size=3, colour='white', tag='polygon', trans=None):
        """Draws a single polyline on the Screen() canvas"""

        # TODO


    def draw_text(self, point, message, colour='white', tag='text'):
        self._canvas.create_text(
            *point, text=message, anchor='sw', fill=colour, tag=tag
        )

    
    def draw_vector(self, geometry='point', screen=False):

        if geometry == 'point':
            
            if self._points is None:
                return

            # TODO


            


    # [22-24/11/2023]


    def _zoom_extent(self, k_0=0.95):

        if len(self._points.coordinates) == 0 and \
           len(self._polylines.coordinates) == 0 and \
           len(self._polygons.coordinates) == 0:
            # Warning ?
            return

        # Source bounding box

        bounding_boxes = []

        if self._points._bbox is None:
            self._points.bounding_box()

        if self._points._bbox is not None:
            bounding_boxes.append(self._points._bbox)


        if self._polylines._bbox is None:
            self._polylines.bounding_box()

        if self._polylines._bbox is not None:
            bounding_boxes.append(self._polylines._bbox)
        

        if self._polygons._bbox is None:
            self._polygons.bounding_box()

        if self._polygons._bbox is not None:
            bounding_boxes.append(self._polygons._bbox)        


        # World extent

        if len(bounding_boxes) == 1:
            
            xw_min, yw_min, xw_max, yw_max = bounding_boxes[0]

        else:

            # xw_min, yw_min, xw_max, yw_max = utilities.merge_bounding_boxes(bounding_boxes)
            pass


        # Screen extent

        xs_min, ys_min, xs_max, ys_max = [0, 0, self._columns, self._rows]

        
        delta_xw = xw_max - xw_min
        delta_yw = yw_max - yw_min
        
        delta_xs = xs_max - xs_min
        delta_ys = ys_max - ys_min

        # Scale factor

        k_1 = delta_xs / delta_xw
        k_2 = delta_ys / delta_yw

        k = min(k_1, k_2) * k_0

        # Translation world space

        tx_world = 0.5 * (xw_min + xw_max)
        ty_world = 0.5 * (yw_min + yw_max)

        # Scale to screen space
        
        tx_world *= k
        ty_world *= k

        # Translation in screen space

        tx_screen = 0.5 * (xs_min + xs_max)
        ty_screen = 0.5 * (ys_min + ys_max)

        # Global translation

        tx = - tx_world + tx_screen
        ty = - ty_world - ty_screen


        # Update Screen() instance

        self._points._screen['transform'] = [k, tx, ty]
        self._polylines._screen['transform'] = [k, tx, ty]
        self._polygons._screen['transform'] = [k, tx, ty]

        
    def zoom_extent(self, event):

        self._zoom_extent()

        

    def _transform_polyline(self, polyline):

        # Get transform parameters
        k, tx, ty = self._polylines._screen['transform']

        transformed_polyline = []

        for point in polyline:

            x, y = point

            x_screen = k * x + tx
            y_screen = -(k * y + ty)

            transformed_polyline.append([x_screen, y_screen])

        return transformed_polyline

        
    def draw_vector_polylines(self):

        """
        Draw polylines on the screen with this sequence:

        1. Using the world file
        2. Using zoom extent
        3. Raw coordinates
        """

        if len(self._polylines.coordinates) == 0:
            # Warning ??
            return

        if self._image._photoimage is not None:
            print('World file')
        elif self._polylines._screen['transform'] is not None:
            #print('Zoom extent')

            for polyline in self._polylines.coordinates:

                # 1. Transform polyline from world to screen coordinates

                transformed_polyline = self._transform_polyline(polyline)
                
                
                # 2. Draw screen coordinates

                self.draw_polyline(transformed_polyline)

                
        else:
            print('Raw coordinates')

        

    def draw_image(self):

        global image

        image = self._image._photoimage # Tkinter image format

        if image is None:
            # Warning
            return

        self._canvas.create_image(0, 0, image=image, anchor='nw')

        

        
    def _screen_to_world(self):
        """Transforms digit points in screen coordinates to world coordinates"""

        if self._image._world_file is None:
            return

        a, d, b, e, c, f = self._image._world_file

        coordinates = []
        attributes = []

        for count, point in enumerate(self._digit.coordinates):

            x, y = point
            
            affine = [a, b, c, d, e, f]

            x_world, y_world = utilities.screen_to_world(x, y, affine)

            #print(x, y, x_world, y_world)

            coordinates.append([x_world, y_world])

            attributes.append({'id': count})

            
        self._points._coordinates = coordinates

        self._points._attributes = attributes

        
            

            
        
        
        







    
class Raster():

    def __init__(self):

        self._filename = None
        self._epsg = None
        self._photoimage = None
        self._world_file = None


    
    def __repr__(self):

        report = {
            'filename': self._filename,
            'epsg': self._epsg,
            'world': self._world_file
        }

        return json.dumps(report, indent=4)


    # Properties

    # Protected methods

    # User methods

    def _read_world_file(self):

        # Filename, extension

        image_filename, image_extension = os.path.splitext(self._filename)

        # World filename

        world_extension = image_extension[1] + image_extension[-1]+ 'w'

        world_filename = image_filename + '.' + world_extension


        try:
            
            with open(world_filename, 'rt') as world_file:
                records = world_file.readlines()

            # Convert to float

            world_file_parameters = list(map(float, records))

            # Check there are 6 parameters

            if len(world_file_parameters) == 6:

                self._world_file = world_file_parameters
            
        except:
            
            pass
            

        

        


    def read_image(self):

        tkinter.Tk().withdraw()
        filename = tkinter.filedialog.askopenfilename(
            title='Select input image file',
            filetypes=[('PNG files', '*.png'), ('GIF files', '*.gif')]
        )

        if not filename:
            return

        self._filename = filename

        self._photoimage = tkinter.PhotoImage(file=filename)


        # Read world file

        self._read_world_file()

        # Read projection file

        

        

        


    

        


        
        
        
            

        
        
                

        






        
