from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'geometric_key', 'geometric_key2', 'normalize_values'
]


# class GeometricKey(object):

#     __instance = None

#     def __new__(cls, precision='3f', tolerance=1e-9, sanitize=True):
#         if GeometricKey.__instance is None:
#             GeometricKey.__instance = object.__new__(cls)
#             GeometricKey.__instance.precision = precision
#             GeometricKey.__instance.tolerance = tolerance
#             GeometricKey.__instance.sanitize = sanitize

#         return GeometricKey.__instance

#     def __call__(self, xyz):
#         return geometric_key(xyz, self.precision, self.tolerance, self.sanitize)

#     @staticmethod
#     def set_precision(precision):
#         GeometricKey.__instance.precision = precision


def geometric_key(xyz, precision='3f', tolerance=1e-9, sanitize=True):
    """Convert XYZ coordinates to a string that can be used as a dict key.

    Parameters:
        xyz (sequence of float): The XYZ coordinates.
        precision (str): Optional.
            A formatting option that specifies the precision of the
            individual numbers in the string.
            Supported values are any float precision, or decimal integer (``'d'``).
            Default is ``'3f'``.
        tolerance (float): Optional.
            A tolerance for values that should be considered zero.
            Default is ``1e-9``.
        sanitize (bool): Optional.
            Flag that indicates whether or not the input should be cleaned up
            using the tolerance value.
            Default is ``True``.

    Returns:
        str: the string representation of the given coordinates.

    Example:

        .. code-block:: python

            from math import pi
            from compas.utilities import geometric_key

            print(geometric_key([pi, pi / 2.0, 2.0 * pi], '3f'))

            # 3.142,3.142,3.142

    """
    x, y, z = xyz
    if precision == 'd':
        return '{0},{1},{2}'.format(int(x), int(y), int(z))
    if sanitize:
        tolerance = tolerance ** 2
        if x ** 2 < tolerance:
            x = 0.0
        if y ** 2 < tolerance:
            y = 0.0
        if z ** 2 < tolerance:
            z = 0.0
    return '{0:.{3}},{1:.{3}},{2:.{3}}'.format(x, y, z, precision)


def geometric_key2(xy, precision='3f', tolerance=1e-9, sanitize=True):
    """Convert XY coordinates to a string that can be used as a dict key."""
    x, y = xy
    if precision == 'd':
        return '{0},{1}'.format(int(x), int(y))
    if sanitize:
        tolerance = tolerance ** 2

        if x ** 2 < tolerance:
            x = 0.0
        if y ** 2 < tolerance:
            y = 0.0
    return '{0:.{2}},{1:.{2}}'.format(x, y, precision)


def normalize_values(values, new_min=0.0, new_max=1.0):
    """Normalize a list of numbers to the range between new_min and new_max."""
    old_max = max(l)
    old_min = min(l)
    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    return [(((value - old_min) * new_range) / old_range) + new_min for value in values]


def remap_values(values, target_min=0.0, target_max=1.0, original_min=None, original_max=None):
    """
    Maps a list of numbers from one domain to another.
    If you do not specify a target domain 0.0-1.0 will be used.

    Parameters
    ----------
    val : list of int, list of long, list of float
        The value to remap
    original_min : int, long, float
        The minimun value of the original domain
    original_max : int, long, float
        The maximum value of the original domain
    target_min : int, long, float
        The minimun value of the target domain. Default 0.0
    target_max : int, long, float
        The maximum value of the target domain. Default 1.0

    Returns
    -------
    list
        The remaped list of values

    """
    if isinstance(values, list):

        if original_min is None:
            original_min = min(values)
        if original_max is None:
            original_max = max(values)

        original_range = original_max - original_min
        target_range = target_max - target_min
        ratio = target_range / original_range

        return [target_min + ((value - original_min) * ratio) for value in values]
    else:
        raise TypeError('Parameter val should be of type: list of int, list of float, list of long')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from math import pi

    gkey1 = GeometricKey(precision='1f')
    gkey2 = GeometricKey(precision='2f')
    gkey3 = GeometricKey(precision='3f')

    GeometricKey.set_precision('3f')

    # print(geometric_key([pi, pi, pi], '3f'))
    # print(geometric_key([-0.00001, +0.00001, 0.00001], '3f', tolerance=1e-3))

    # print(geometric_key((1.1102230246251565e-16, -1.1102230246251565e-16, -1.7320508075688774), '3f', tolerance=1e-9))
    # print(geometric_key((-1.1102230246251565e-16, -1.1102230246251565e-16, -1.7320508075688774), '3f', tolerance=1e-9))

    print(gkey1([pi, pi, pi]))
    print(gkey2([-0.00001, +0.00001, 0.00001]))

    print(gkey3((1.1102230246251565e-16, -1.1102230246251565e-16, -1.7320508075688774)))
    print(gkey1((-1.1102230246251565e-16, -1.1102230246251565e-16, -1.7320508075688774)))
