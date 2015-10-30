'''
Created on Oct 24, 2015

@author: ionut
'''

import json

def gps_to_json(positions):
    data = []
    for p in positions:
        aux = p.copy()
        aux['time'] = int(aux['time'].strftime('%s'))
        data.append(aux)
    return json.dumps(data)

def convert_projection(x, y, src_proj='+init=EPSG:4326', dst_proj='+init=EPSG:31700'):
    x = float(x)
    y = float(y)
    import pyproj
    x1, y1 = pyproj.transform(pyproj.Proj(src_proj), pyproj.Proj(dst_proj), x, y)
    return x1, y1

if __name__ == '__main__':
    x = 25.0
    y = 46.0
    x1, y1 = convert_projection(x, y)
    print('input [%.5f, %.5f], output [%.5f, %.5f]' % (x, y, x1, y1))