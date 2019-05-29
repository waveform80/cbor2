import sys
import struct
import platform
from setuptools import setup, Extension

cpython = platform.python_implementation() == 'CPython'
windows = sys.platform.startswith('win')
min_win_version = windows and sys.version_info >= (3, 5)
min_unix_version = not windows and sys.version_info >= (3, 3)

if cpython and (min_unix_version or min_win_version):
    def struct_type(size, signed):
        size //= 8
        codes = 'BHILQ'
        if signed:
            codes = codes.lower()
        for code in codes:
            if struct.calcsize(code) == size:
                return "'" + str(code) + "'"
        raise ValueError('unable to find typecode for %s %d bits' %
                         (('unsigned', 'signed')[signed], size))

    _cbor2 = Extension(
        '_cbor2',
        # math.h routines are built-in to MSVCRT
        libraries=['m'] if not windows else [],
        define_macros=[
            ('PY_TYPE_UINT8', "'B'"),
            ('PY_TYPE_UINT16', struct_type(16, False)),
            ('PY_TYPE_UINT32', struct_type(32, False)),
            ('PY_TYPE_UINT64', struct_type(64, False)),
            ('PY_TYPE_SINT8', "'b'"),
            ('PY_TYPE_SINT16', struct_type(16, True)),
            ('PY_TYPE_SINT32', struct_type(32, True)),
            ('PY_TYPE_SINT64', struct_type(64, True)),
            ('PY_TYPE_FLOAT32', "'f'"),
            ('PY_TYPE_FLOAT64', "'d'"),
        ],
        sources=[
            'source/module.c',
            'source/encoder.c',
            'source/decoder.c',
            'source/tags.c',
            'source/halffloat.c',
        ]
    )
    kwargs = {'ext_modules': [_cbor2]}
else:
    kwargs = {}


setup(
    use_scm_version={
        'version_scheme': 'post-release',
        'local_scheme': 'dirty-tag'
    },
    setup_requires=[
        'setuptools >= 36.2.7',
        'setuptools_scm >= 1.7.0'
    ],
    **kwargs
)
