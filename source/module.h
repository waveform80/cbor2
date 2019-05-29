#include <Python.h>
#if PY_MAJOR_VERSION < 3
#  error "_cbor2 doesn't support the Python 2.x API"
#elif PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION < 3
#  error "_cbor2 requires Python 3.3 or newer"
#elif PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION < 4
// Python 3.3 doesn't define PY_BIG_ENDIAN and PY_LITTLE_ENDIAN, but does
// include the WORDS_BIGENDIAN define
#  ifdef WORDS_BIGENDIAN
#    define PY_BIG_ENDIAN 1
#    define PY_LITTLE_ENDIAN 0
#  else
#    define PY_BIG_ENDIAN 0
#    define PY_LITTLE_ENDIAN 1
#  endif
#endif

// structure of the lead-byte for all CBOR records
typedef
    union {
        struct {
            unsigned int subtype: 5;
            unsigned int major: 3;
        };
        char byte;
    } LeadByte;

// structure for construction of typed array tag-numbers; see reference at
// https://datatracker.ietf.org/doc/draft-ietf-cbor-array-tags/?include_text=1
// for full explanation of type codes
typedef
    union {
        struct {
            unsigned int ll: 2;     // length code
            unsigned int e: 1;      // 0=big endian, 1=little endian
            unsigned int s: 1;      // 0=unsigned/float, 1=signed int
            unsigned int f: 1;      // 0=int type, 1=float type
            unsigned int head: 3;   // set to 2 (0b010)
        };
        char byte;
    } TypedArrayTag;

// break_marker singleton
extern PyObject _break_marker_obj;
#define break_marker (&_break_marker_obj)
#define CBOR2_RETURN_BREAK return Py_INCREF(break_marker), break_marker

// undefined singleton
extern PyObject _undefined_obj;
#define undefined (&_undefined_obj)
#define CBOR2_RETURN_UNDEFINED return Py_INCREF(undefined), undefined

// CBORSimpleValue namedtuple type
extern PyTypeObject CBORSimpleValueType;

// Various interned strings
extern PyObject *_CBOR2_empty_bytes;
extern PyObject *_CBOR2_empty_str;
extern PyObject *_CBOR2_str_array;
extern PyObject *_CBOR2_str_as_string;
extern PyObject *_CBOR2_str_as_tuple;
extern PyObject *_CBOR2_str_bit_length;
extern PyObject *_CBOR2_str_bytes;
extern PyObject *_CBOR2_str_byteswap;
extern PyObject *_CBOR2_str_BytesIO;
extern PyObject *_CBOR2_str_canonical_encoders;
extern PyObject *_CBOR2_str_compile;
extern PyObject *_CBOR2_str_copy;
extern PyObject *_CBOR2_str_datestr_re;
extern PyObject *_CBOR2_str_Decimal;
extern PyObject *_CBOR2_str_default_encoders;
extern PyObject *_CBOR2_str_denominator;
extern PyObject *_CBOR2_str_Fraction;
extern PyObject *_CBOR2_str_fromtimestamp;
extern PyObject *_CBOR2_str_FrozenDict;
extern PyObject *_CBOR2_str_geturl;
extern PyObject *_CBOR2_str_getvalue;
extern PyObject *_CBOR2_str_groups;
extern PyObject *_CBOR2_str_ip_address;
extern PyObject *_CBOR2_str_ip_network;
extern PyObject *_CBOR2_str_is_infinite;
extern PyObject *_CBOR2_str_is_nan;
extern PyObject *_CBOR2_str_isoformat;
extern PyObject *_CBOR2_str_join;
extern PyObject *_CBOR2_str_match;
extern PyObject *_CBOR2_str_network_address;
extern PyObject *_CBOR2_str_numerator;
extern PyObject *_CBOR2_str_obj;
extern PyObject *_CBOR2_str_packed;
extern PyObject *_CBOR2_str_Parser;
extern PyObject *_CBOR2_str_parsestr;
extern PyObject *_CBOR2_str_pattern;
extern PyObject *_CBOR2_str_prefixlen;
extern PyObject *_CBOR2_str_read;
extern PyObject *_CBOR2_str_s;
extern PyObject *_CBOR2_str_standard_b64decode;
extern PyObject *_CBOR2_str_timestamp;
extern PyObject *_CBOR2_str_timezone;
extern PyObject *_CBOR2_str_update;
extern PyObject *_CBOR2_str_urlsafe_b64decode;
extern PyObject *_CBOR2_str_urlsplit;
extern PyObject *_CBOR2_str_utc;
extern PyObject *_CBOR2_str_utc_suffix;
extern PyObject *_CBOR2_str_UUID;
extern PyObject *_CBOR2_str_write;

// Exception classes
extern PyObject *_CBOR2_CBORError;
extern PyObject *_CBOR2_CBOREncodeError;
extern PyObject *_CBOR2_CBORDecodeError;

// Global references (initialized by functions declared below)
extern PyObject *_CBOR2_timezone;
extern PyObject *_CBOR2_timezone_utc;
extern PyObject *_CBOR2_BytesIO;
extern PyObject *_CBOR2_Decimal;
extern PyObject *_CBOR2_Fraction;
extern PyObject *_CBOR2_FrozenDict;
extern PyObject *_CBOR2_UUID;
extern PyObject *_CBOR2_Parser;
extern PyObject *_CBOR2_re_compile;
extern PyObject *_CBOR2_datestr_re;
extern PyObject *_CBOR2_ip_address;
extern PyObject *_CBOR2_ip_network;
extern PyObject *_CBOR2_urlsplit;
extern PyObject *_CBOR2_standard_b64decode;
extern PyObject *_CBOR2_urlsafe_b64decode;
extern PyObject *_CBOR2_array;

// Initializers for the cached references above
int _CBOR2_init_timezone_utc(void); // also handles timezone
int _CBOR2_init_BytesIO(void);
int _CBOR2_init_Decimal(void);
int _CBOR2_init_Fraction(void);
int _CBOR2_init_FrozenDict(void);
int _CBOR2_init_UUID(void);
int _CBOR2_init_Parser(void);
int _CBOR2_init_re_compile(void); // also handles datestr_re
int _CBOR2_init_ip_address(void);
int _CBOR2_init_urlsplit(void); // also handles {standard,urlsafe}_b64decode
int _CBOR2_init_array(void);

int init_default_encoders(void);
int init_canonical_encoders(void);

// Encoder registries
extern PyObject *_CBOR2_default_encoders;
extern PyObject *_CBOR2_canonical_encoders;
