import mapping_osm
from decimal import Decimal as d

def test_gps_to_decimal_degrees_n_d_m_s():
    pb = mapping_osm.PicBase()

    deg = {'ref': 'N', 'pos': [[14, 1], [27, 1], [5866, 100]]}
    answer = d('14.4663')

    deg_decimal = d(pb.convert_gps_to_decimal_degrees(deg))
    print(deg_decimal.quantize(d('0.0001')), type(deg_decimal))
    print(answer.quantize(d('0.0001')), type(answer))

    assert deg_decimal.quantize(d('0.0001')) == answer.quantize(d('0.0001'))

def test_gps_to_decimal_degrees_s_d_m_s():
    pb = mapping_osm.PicBase()

    deg = {'ref': 'S', 'pos': [[14, 1], [27, 1], [5866, 100]]}
    answer = d('-14.4663')

    deg_decimal = d(pb.convert_gps_to_decimal_degrees(deg))
    print(deg_decimal.quantize(d('0.0001')), type(deg_decimal))
    print(answer.quantize(d('0.0001')), type(answer))

    assert deg_decimal.quantize(d('0.0001')) == answer.quantize(d('0.0001'))

def test_gps_to_decimal_degrees_e_d_m_s():
    pb = mapping_osm.PicBase()

    deg = {'ref': 'E', 'pos': [[14, 1], [27, 1], [5866, 100]]}
    answer = d('+14.4663')

    deg_decimal = d(pb.convert_gps_to_decimal_degrees(deg))
    print(deg_decimal.quantize(d('0.0001')), type(deg_decimal))
    print(answer.quantize(d('0.0001')), type(answer))

    assert deg_decimal.quantize(d('0.0001')) == answer.quantize(d('0.0001'))

def test_gps_to_decimal_degrees_w_d_m_s():
    pb = mapping_osm.PicBase()

    deg = {'ref': 'W', 'pos': [[14, 1], [27, 1], [5866, 100]]}
    answer = d('-14.4663')

    deg_decimal = d(pb.convert_gps_to_decimal_degrees(deg))
    print(deg_decimal.quantize(d('0.0001')), type(deg_decimal))
    print(answer.quantize(d('0.0001')), type(answer))

    assert deg_decimal.quantize(d('0.0001')) == answer.quantize(d('0.0001'))

def test_gps_to_decimal_degrees_n_d_m():
    pb = mapping_osm.PicBase()

    deg = {'ref': 'N', 'pos': [[14, 1], [2733, 100], [0, 1]]}
    answer = d('14.4555')

    deg_decimal = d(pb.convert_gps_to_decimal_degrees(deg))
    print(deg_decimal.quantize(d('0.0001')), type(deg_decimal))
    print(answer.quantize(d('0.0001')), type(answer))

    assert deg_decimal.quantize(d('0.0001')) == answer.quantize(d('0.0001'))

def test_gps_to_decimal_degrees_n_d():
    pb = mapping_osm.PicBase()

    deg = {'ref': 'N', 'pos': [[142733, 10000], [0, 100], [0, 1]]}
    answer = d('14.2733')

    deg_decimal = d(pb.convert_gps_to_decimal_degrees(deg))
    print(deg_decimal.quantize(d('0.0001')), type(deg_decimal))
    print(answer.quantize(d('0.0001')), type(answer))

    assert deg_decimal.quantize(d('0.0001')) == answer.quantize(d('0.0001'))



if __name__ == '__main__':
    test_gps_to_decimal_degrees_e_d_m_s()
