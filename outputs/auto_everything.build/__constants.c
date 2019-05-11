
#include "nuitka/prelude.h"
#include "structseq.h"

// Sentinel PyObject to be used for all our call iterator endings. It will
// become a PyCObject pointing to NULL. It's address is unique, and that's
// enough for us to use it as sentinel value.
PyObject *_sentinel_value = NULL;

PyObject *Nuitka_dunder_compiled_value = NULL;

PyObject *const_int_0;
PyObject *const_str_dot;
PyObject *const_int_pos_1;
PyObject *const_int_pos_6;
PyObject *const_str_empty;
PyObject *const_dict_empty;
PyObject *const_str_chr_47;
PyObject *const_bytes_empty;
PyObject *const_str_newline;
PyObject *const_str_plain_e;
PyObject *const_str_plain_f;
PyObject *const_str_plain_p;
PyObject *const_str_plain_r;
PyObject *const_str_plain_t;
PyObject *const_str_plain_w;
PyObject *const_tuple_empty;
PyObject *const_str_plain_IO;
PyObject *const_str_plain_os;
PyObject *const_str_plain_rb;
PyObject *const_str_plain_end;
PyObject *const_str_plain_get;
PyObject *const_str_plain_key;
PyObject *const_str_plain_num;
PyObject *const_str_plain_run;
PyObject *const_str_plain_sum;
PyObject *const_str_plain_None;
PyObject *const_str_plain_dict;
PyObject *const_str_plain_exit;
PyObject *const_str_plain_file;
PyObject *const_str_plain_join;
PyObject *const_str_plain_keys;
PyObject *const_str_plain_name;
PyObject *const_str_plain_open;
PyObject *const_str_plain_path;
PyObject *const_str_plain_read;
PyObject *const_str_plain_self;
PyObject *const_str_plain_send;
PyObject *const_str_plain_text;
PyObject *const_str_plain_time;
PyObject *const_str_plain_type;
PyObject *const_str_plain_wait;
PyObject *const_str_plain_False;
PyObject *const_str_plain_bytes;
PyObject *const_str_plain_close;
PyObject *const_str_plain_debug;
PyObject *const_str_plain_level;
PyObject *const_str_plain_print;
PyObject *const_str_plain_range;
PyObject *const_str_plain_sleep;
PyObject *const_str_plain_split;
PyObject *const_str_plain_strip;
PyObject *const_str_plain_throw;
PyObject *const_str_plain_tuple;
PyObject *const_str_plain_types;
PyObject *const_str_plain_write;
PyObject *const_str_plain_Python;
PyObject *const_str_plain_append;
PyObject *const_str_plain_exists;
PyObject *const_str_plain_format;
PyObject *const_str_plain_locals;
PyObject *const_str_plain_origin;
PyObject *const_str_plain_remove;
PyObject *const_tuple_none_tuple;
PyObject *const_str_plain___all__;
PyObject *const_str_plain___cmp__;
PyObject *const_str_plain___doc__;
PyObject *const_str_plain_abspath;
PyObject *const_str_plain_compile;
PyObject *const_str_plain_dirname;
PyObject *const_str_plain_globals;
PyObject *const_str_plain_inspect;
PyObject *const_str_plain_timeout;
PyObject *const_tuple_false_tuple;
PyObject *const_str_plain_Terminal;
PyObject *const_str_plain___dict__;
PyObject *const_str_plain___exit__;
PyObject *const_str_plain___file__;
PyObject *const_str_plain___init__;
PyObject *const_str_plain___iter__;
PyObject *const_str_plain___main__;
PyObject *const_str_plain___name__;
PyObject *const_str_plain___path__;
PyObject *const_str_plain___spec__;
PyObject *const_str_plain_fromlist;
PyObject *const_str_plain_getmtime;
PyObject *const_str_angle_metaclass;
PyObject *const_str_plain___class__;
PyObject *const_str_plain___debug__;
PyObject *const_str_plain___enter__;
PyObject *const_str_plain_bytearray;
PyObject *const_str_plain_file_path;
PyObject *const_str_plain_metaclass;
PyObject *const_str_plain___cached__;
PyObject *const_str_plain___import__;
PyObject *const_str_plain___loader__;
PyObject *const_str_plain___module__;
PyObject *const_str_plain___getitem__;
PyObject *const_str_plain___package__;
PyObject *const_str_plain___prepare__;
PyObject *const_str_plain_classmethod;
PyObject *const_str_plain_working_dir;
PyObject *const_tuple_int_pos_1_tuple;
PyObject *const_str_plain___builtins__;
PyObject *const_str_plain___compiled__;
PyObject *const_str_plain___internal__;
PyObject *const_str_plain___qualname__;
PyObject *const_str_plain_has_location;
PyObject *const_str_plain_staticmethod;
PyObject *const_str_plain___metaclass__;
PyObject *const_str_plain__initializing;
PyObject *const_slice_int_pos_1_none_none;
PyObject *const_slice_none_int_pos_6_none;
PyObject *const_tuple_str_plain_self_tuple;
PyObject *const_tuple_str_plain___class___tuple;
PyObject *const_str_plain_submodule_search_locations;
PyObject *const_str_digest_25731c733fd74e8333aa29126ce85686;
PyObject *const_str_digest_45e4dde2057b0bf276d6a84f4c917d27;
PyObject *const_str_digest_75fd71b1edada749c2ef7ac810062295;
PyObject *const_str_digest_9816e8d1552296af90d250823c964059;
PyObject *const_str_digest_adc474dd61fbd736d69c1bac5d9712e0;
PyObject *const_str_digest_b08fb10093cd2e07b291c2941013d5a6;
PyObject *const_str_digest_b50a17fc9d65354c4fea46012b82ea0b;
PyObject *const_tuple_str_digest_b50a17fc9d65354c4fea46012b82ea0b_tuple;
PyObject *const_tuple_anon_function_anon_builtin_function_or_method_tuple;

static void _createGlobalConstants( void )
{
    NUITKA_MAY_BE_UNUSED PyObject *exception_type, *exception_value;
    NUITKA_MAY_BE_UNUSED PyTracebackObject *exception_tb;

#ifdef _MSC_VER
    // Prevent unused warnings in case of simple programs, the attribute
    // NUITKA_MAY_BE_UNUSED doesn't work for MSVC.
    (void *)exception_type; (void *)exception_value; (void *)exception_tb;
#endif

    const_int_0 = PyLong_FromUnsignedLong( 0ul );
    const_str_dot = UNSTREAM_STRING_ASCII( &constant_bin[ 94 ], 1, 0 );
    const_int_pos_1 = PyLong_FromUnsignedLong( 1ul );
    const_int_pos_6 = PyLong_FromUnsignedLong( 6ul );
    const_str_empty = UNSTREAM_STRING_ASCII( &constant_bin[ 0 ], 0, 0 );
    const_dict_empty = _PyDict_NewPresized( 0 );
    assert( PyDict_Size( const_dict_empty ) == 0 );
    const_str_chr_47 = UNSTREAM_STRING_ASCII( &constant_bin[ 30 ], 1, 0 );
    const_bytes_empty = UNSTREAM_BYTES( &constant_bin[ 0 ], 0 );
    const_str_newline = UNSTREAM_STRING_ASCII( &constant_bin[ 169 ], 1, 0 );
    const_str_plain_e = UNSTREAM_STRING_ASCII( &constant_bin[ 20 ], 1, 1 );
    const_str_plain_f = UNSTREAM_STRING_ASCII( &constant_bin[ 182 ], 1, 1 );
    const_str_plain_p = UNSTREAM_STRING_ASCII( &constant_bin[ 95 ], 1, 1 );
    const_str_plain_r = UNSTREAM_STRING_ASCII( &constant_bin[ 23 ], 1, 1 );
    const_str_plain_t = UNSTREAM_STRING_ASCII( &constant_bin[ 17 ], 1, 1 );
    const_str_plain_w = UNSTREAM_STRING_ASCII( &constant_bin[ 199 ], 1, 1 );
    const_tuple_empty = PyTuple_New( 0 );
    const_str_plain_IO = UNSTREAM_STRING_ASCII( &constant_bin[ 714 ], 2, 1 );
    const_str_plain_os = UNSTREAM_STRING_ASCII( &constant_bin[ 3251 ], 2, 1 );
    const_str_plain_rb = UNSTREAM_STRING_ASCII( &constant_bin[ 16330 ], 2, 1 );
    const_str_plain_end = UNSTREAM_STRING_ASCII( &constant_bin[ 1708 ], 3, 1 );
    const_str_plain_get = UNSTREAM_STRING_ASCII( &constant_bin[ 142 ], 3, 1 );
    const_str_plain_key = UNSTREAM_STRING_ASCII( &constant_bin[ 16332 ], 3, 1 );
    const_str_plain_num = UNSTREAM_STRING_ASCII( &constant_bin[ 1741 ], 3, 1 );
    const_str_plain_run = UNSTREAM_STRING_ASCII( &constant_bin[ 217 ], 3, 1 );
    const_str_plain_sum = UNSTREAM_STRING_ASCII( &constant_bin[ 16335 ], 3, 1 );
    const_str_plain_None = UNSTREAM_STRING_ASCII( &constant_bin[ 16338 ], 4, 1 );
    const_str_plain_dict = UNSTREAM_STRING_ASCII( &constant_bin[ 349 ], 4, 1 );
    const_str_plain_exit = UNSTREAM_STRING_ASCII( &constant_bin[ 8426 ], 4, 1 );
    const_str_plain_file = UNSTREAM_STRING_ASCII( &constant_bin[ 499 ], 4, 1 );
    const_str_plain_join = UNSTREAM_STRING_ASCII( &constant_bin[ 16342 ], 4, 1 );
    const_str_plain_keys = UNSTREAM_STRING_ASCII( &constant_bin[ 16332 ], 4, 1 );
    const_str_plain_name = UNSTREAM_STRING_ASCII( &constant_bin[ 338 ], 4, 1 );
    const_str_plain_open = UNSTREAM_STRING_ASCII( &constant_bin[ 474 ], 4, 1 );
    const_str_plain_path = UNSTREAM_STRING_ASCII( &constant_bin[ 159 ], 4, 1 );
    const_str_plain_read = UNSTREAM_STRING_ASCII( &constant_bin[ 1711 ], 4, 1 );
    const_str_plain_self = UNSTREAM_STRING_ASCII( &constant_bin[ 5602 ], 4, 1 );
    const_str_plain_send = UNSTREAM_STRING_ASCII( &constant_bin[ 16346 ], 4, 1 );
    const_str_plain_text = UNSTREAM_STRING_ASCII( &constant_bin[ 122 ], 4, 1 );
    const_str_plain_time = UNSTREAM_STRING_ASCII( &constant_bin[ 2644 ], 4, 1 );
    const_str_plain_type = UNSTREAM_STRING_ASCII( &constant_bin[ 457 ], 4, 1 );
    const_str_plain_wait = UNSTREAM_STRING_ASCII( &constant_bin[ 2069 ], 4, 1 );
    const_str_plain_False = UNSTREAM_STRING_ASCII( &constant_bin[ 7736 ], 5, 1 );
    const_str_plain_bytes = UNSTREAM_STRING_ASCII( &constant_bin[ 10099 ], 5, 1 );
    const_str_plain_close = UNSTREAM_STRING_ASCII( &constant_bin[ 16350 ], 5, 1 );
    const_str_plain_debug = UNSTREAM_STRING_ASCII( &constant_bin[ 1036 ], 5, 1 );
    const_str_plain_level = UNSTREAM_STRING_ASCII( &constant_bin[ 16355 ], 5, 1 );
    const_str_plain_print = UNSTREAM_STRING_ASCII( &constant_bin[ 3297 ], 5, 1 );
    const_str_plain_range = UNSTREAM_STRING_ASCII( &constant_bin[ 16360 ], 5, 1 );
    const_str_plain_sleep = UNSTREAM_STRING_ASCII( &constant_bin[ 16365 ], 5, 1 );
    const_str_plain_split = UNSTREAM_STRING_ASCII( &constant_bin[ 2854 ], 5, 1 );
    const_str_plain_strip = UNSTREAM_STRING_ASCII( &constant_bin[ 16370 ], 5, 1 );
    const_str_plain_throw = UNSTREAM_STRING_ASCII( &constant_bin[ 16375 ], 5, 1 );
    const_str_plain_tuple = UNSTREAM_STRING_ASCII( &constant_bin[ 16380 ], 5, 1 );
    const_str_plain_types = UNSTREAM_STRING_ASCII( &constant_bin[ 16385 ], 5, 1 );
    const_str_plain_write = UNSTREAM_STRING_ASCII( &constant_bin[ 717 ], 5, 1 );
    const_str_plain_Python = UNSTREAM_STRING_ASCII( &constant_bin[ 241 ], 6, 1 );
    const_str_plain_append = UNSTREAM_STRING_ASCII( &constant_bin[ 1705 ], 6, 1 );
    const_str_plain_exists = UNSTREAM_STRING_ASCII( &constant_bin[ 3665 ], 6, 1 );
    const_str_plain_format = UNSTREAM_STRING_ASCII( &constant_bin[ 4836 ], 6, 1 );
    const_str_plain_locals = UNSTREAM_STRING_ASCII( &constant_bin[ 263 ], 6, 1 );
    const_str_plain_origin = UNSTREAM_STRING_ASCII( &constant_bin[ 5721 ], 6, 1 );
    const_str_plain_remove = UNSTREAM_STRING_ASCII( &constant_bin[ 10025 ], 6, 1 );
    const_tuple_none_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_none_tuple, 0, Py_None ); Py_INCREF( Py_None );
    const_str_plain___all__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16390 ], 7, 1 );
    const_str_plain___cmp__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16397 ], 7, 1 );
    const_str_plain___doc__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16404 ], 7, 1 );
    const_str_plain_abspath = UNSTREAM_STRING_ASCII( &constant_bin[ 16411 ], 7, 1 );
    const_str_plain_compile = UNSTREAM_STRING_ASCII( &constant_bin[ 16418 ], 7, 1 );
    const_str_plain_dirname = UNSTREAM_STRING_ASCII( &constant_bin[ 16425 ], 7, 1 );
    const_str_plain_globals = UNSTREAM_STRING_ASCII( &constant_bin[ 16432 ], 7, 1 );
    const_str_plain_inspect = UNSTREAM_STRING_ASCII( &constant_bin[ 16439 ], 7, 1 );
    const_str_plain_timeout = UNSTREAM_STRING_ASCII( &constant_bin[ 8161 ], 7, 1 );
    const_tuple_false_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_false_tuple, 0, Py_False ); Py_INCREF( Py_False );
    const_str_plain_Terminal = UNSTREAM_STRING_ASCII( &constant_bin[ 112 ], 8, 1 );
    const_str_plain___dict__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16446 ], 8, 1 );
    const_str_plain___exit__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16454 ], 8, 1 );
    const_str_plain___file__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16462 ], 8, 1 );
    const_str_plain___init__ = UNSTREAM_STRING_ASCII( &constant_bin[ 86 ], 8, 1 );
    const_str_plain___iter__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16470 ], 8, 1 );
    const_str_plain___main__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16478 ], 8, 1 );
    const_str_plain___name__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16486 ], 8, 1 );
    const_str_plain___path__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16494 ], 8, 1 );
    const_str_plain___spec__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16502 ], 8, 1 );
    const_str_plain_fromlist = UNSTREAM_STRING_ASCII( &constant_bin[ 16510 ], 8, 1 );
    const_str_plain_getmtime = UNSTREAM_STRING_ASCII( &constant_bin[ 16518 ], 8, 1 );
    const_str_angle_metaclass = UNSTREAM_STRING_ASCII( &constant_bin[ 16526 ], 11, 0 );
    const_str_plain___class__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16537 ], 9, 1 );
    const_str_plain___debug__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16546 ], 9, 1 );
    const_str_plain___enter__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16555 ], 9, 1 );
    const_str_plain_bytearray = UNSTREAM_STRING_ASCII( &constant_bin[ 16564 ], 9, 1 );
    const_str_plain_file_path = UNSTREAM_STRING_ASCII( &constant_bin[ 499 ], 9, 1 );
    const_str_plain_metaclass = UNSTREAM_STRING_ASCII( &constant_bin[ 16527 ], 9, 1 );
    const_str_plain___cached__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16573 ], 10, 1 );
    const_str_plain___import__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16583 ], 10, 1 );
    const_str_plain___loader__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16593 ], 10, 1 );
    const_str_plain___module__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16603 ], 10, 1 );
    const_str_plain___getitem__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16613 ], 11, 1 );
    const_str_plain___package__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16624 ], 11, 1 );
    const_str_plain___prepare__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16635 ], 11, 1 );
    const_str_plain_classmethod = UNSTREAM_STRING_ASCII( &constant_bin[ 16646 ], 11, 1 );
    const_str_plain_working_dir = UNSTREAM_STRING_ASCII( &constant_bin[ 3452 ], 11, 1 );
    const_tuple_int_pos_1_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_int_pos_1_tuple, 0, const_int_pos_1 ); Py_INCREF( const_int_pos_1 );
    const_str_plain___builtins__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16657 ], 12, 1 );
    const_str_plain___compiled__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16669 ], 12, 1 );
    const_str_plain___internal__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16681 ], 12, 1 );
    const_str_plain___qualname__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16693 ], 12, 1 );
    const_str_plain_has_location = UNSTREAM_STRING_ASCII( &constant_bin[ 16705 ], 12, 1 );
    const_str_plain_staticmethod = UNSTREAM_STRING_ASCII( &constant_bin[ 16717 ], 12, 1 );
    const_str_plain___metaclass__ = UNSTREAM_STRING_ASCII( &constant_bin[ 16729 ], 13, 1 );
    const_str_plain__initializing = UNSTREAM_STRING_ASCII( &constant_bin[ 16742 ], 13, 1 );
    const_slice_int_pos_1_none_none = PySlice_New( const_int_pos_1, Py_None, Py_None );
    const_slice_none_int_pos_6_none = PySlice_New( Py_None, const_int_pos_6, Py_None );
    const_tuple_str_plain_self_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_self_tuple, 0, const_str_plain_self ); Py_INCREF( const_str_plain_self );
    const_tuple_str_plain___class___tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain___class___tuple, 0, const_str_plain___class__ ); Py_INCREF( const_str_plain___class__ );
    const_str_plain_submodule_search_locations = UNSTREAM_STRING_ASCII( &constant_bin[ 16755 ], 26, 1 );
    const_str_digest_25731c733fd74e8333aa29126ce85686 = UNSTREAM_STRING_ASCII( &constant_bin[ 5555 ], 2, 0 );
    const_str_digest_45e4dde2057b0bf276d6a84f4c917d27 = UNSTREAM_STRING_ASCII( &constant_bin[ 16781 ], 7, 0 );
    const_str_digest_75fd71b1edada749c2ef7ac810062295 = UNSTREAM_STRING_ASCII( &constant_bin[ 16788 ], 46, 0 );
    const_str_digest_9816e8d1552296af90d250823c964059 = UNSTREAM_STRING_ASCII( &constant_bin[ 16834 ], 46, 0 );
    const_str_digest_adc474dd61fbd736d69c1bac5d9712e0 = UNSTREAM_STRING_ASCII( &constant_bin[ 16880 ], 47, 0 );
    const_str_digest_b08fb10093cd2e07b291c2941013d5a6 = UNSTREAM_STRING_ASCII( &constant_bin[ 3261 ], 20, 0 );
    const_str_digest_b50a17fc9d65354c4fea46012b82ea0b = UNSTREAM_STRING_ASCII( &constant_bin[ 16927 ], 22, 0 );
    const_tuple_str_digest_b50a17fc9d65354c4fea46012b82ea0b_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_digest_b50a17fc9d65354c4fea46012b82ea0b_tuple, 0, const_str_digest_b50a17fc9d65354c4fea46012b82ea0b ); Py_INCREF( const_str_digest_b50a17fc9d65354c4fea46012b82ea0b );
    const_tuple_anon_function_anon_builtin_function_or_method_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_anon_function_anon_builtin_function_or_method_tuple, 0, (PyObject *)&PyFunction_Type ); Py_INCREF( (PyObject *)&PyFunction_Type );
    PyTuple_SET_ITEM( const_tuple_anon_function_anon_builtin_function_or_method_tuple, 1, (PyObject *)&PyCFunction_Type ); Py_INCREF( (PyObject *)&PyCFunction_Type );

#if _NUITKA_EXE
    /* Set the "sys.executable" path to the original CPython executable. */
    PySys_SetObject(
        (char *)"executable",
        None
    );

#ifndef _NUITKA_STANDALONE
    /* Set the "sys.prefix" path to the original one. */
    PySys_SetObject(
        (char *)"prefix",
        None
    );

    /* Set the "sys.prefix" path to the original one. */
    PySys_SetObject(
        (char *)"exec_prefix",
        None
    );


#if PYTHON_VERSION >= 300
    /* Set the "sys.base_prefix" path to the original one. */
    PySys_SetObject(
        (char *)"base_prefix",
        None
    );

    /* Set the "sys.exec_base_prefix" path to the original one. */
    PySys_SetObject(
        (char *)"base_exec_prefix",
        None
    );

#endif
#endif
#endif

    static PyTypeObject Nuitka_VersionInfoType;

    // Same fields as "sys.version_info" except no serial number.
    static PyStructSequence_Field Nuitka_VersionInfoFields[] = {
        {(char *)"major", (char *)"Major release number"},
        {(char *)"minor", (char *)"Minor release number"},
        {(char *)"micro", (char *)"Micro release number"},
        {(char *)"releaselevel", (char *)"'alpha', 'beta', 'candidate', or 'release'"},
        {0}
    };

    static PyStructSequence_Desc Nuitka_VersionInfoDesc = {
        (char *)"__nuitka_version__",                                    /* name */
        (char *)"__compiled__\n\nVersion information as a named tuple.", /* doc */
        Nuitka_VersionInfoFields,                                        /* fields */
        4
    };

    PyStructSequence_InitType(&Nuitka_VersionInfoType, &Nuitka_VersionInfoDesc);

    Nuitka_dunder_compiled_value = PyStructSequence_New(&Nuitka_VersionInfoType);
    assert(Nuitka_dunder_compiled_value != NULL);

    PyStructSequence_SET_ITEM(Nuitka_dunder_compiled_value, 0, PyInt_FromLong(0));
    PyStructSequence_SET_ITEM(Nuitka_dunder_compiled_value, 1, PyInt_FromLong(6));
    PyStructSequence_SET_ITEM(Nuitka_dunder_compiled_value, 2, PyInt_FromLong(3));

#if PYTHON_VERSION < 300
    PyStructSequence_SET_ITEM(Nuitka_dunder_compiled_value, 3, PyString_FromString("release"));
#else
    PyStructSequence_SET_ITEM(Nuitka_dunder_compiled_value, 3, PyUnicode_FromString("release"));
#endif
    // Prevent users from creating the Nuitka version type object.
    Nuitka_VersionInfoType.tp_init = NULL;
    Nuitka_VersionInfoType.tp_new = NULL;


}

// In debug mode we can check that the constants were not tampered with in any
// given moment. We typically do it at program exit, but we can add extra calls
// for sanity.
#ifndef __NUITKA_NO_ASSERT__
void checkGlobalConstants( void )
{

}
#endif

void createGlobalConstants( void )
{
    if ( _sentinel_value == NULL )
    {
#if PYTHON_VERSION < 300
        _sentinel_value = PyCObject_FromVoidPtr( NULL, NULL );
#else
        // The NULL value is not allowed for a capsule, so use something else.
        _sentinel_value = PyCapsule_New( (void *)27, "sentinel", NULL );
#endif
        assert( _sentinel_value );

        _createGlobalConstants();
    }
}
