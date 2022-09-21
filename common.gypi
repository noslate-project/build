{
  'variables': {
    'component%': 'static_library',
    'uv_library%': 'static_library',
    'clang%': 0,
    'llvm_version%': '0.0',

    'conditions': [[
      "OS=='mac'", {
        'clang%': 1
      }
    ]],

    # Redirect Node.js obj_dir
    'conditions': [
      ['OS=="mac"', {
        'obj_dir': '<(PRODUCT_DIR)/obj.target',
        'v8_base': '<(PRODUCT_DIR)/libv8_snapshot.a',
      }, {
        'obj_dir': '<(PRODUCT_DIR)/obj/node',
        'v8_base': '<(PRODUCT_DIR)/obj/node/tools/v8_gypfiles/libv8_snapshot.a',
      }],
    ],
  },
  'target_defaults': {
    'cflags': [ '-pthread' ],
    'ldflags': [ '-pthread' ],

    'conditions': [
      [
        "OS=='mac'", {
          'defines': ['_DARWIN_USE_64_BIT_INODE=1'],
          'xcode_settings': {
            'ALWAYS_SEARCH_USER_PATHS': 'NO',
            'GCC_CW_ASM_SYNTAX': 'NO',                # No -fasm-blocks
            'GCC_DYNAMIC_NO_PIC': 'NO',               # No -mdynamic-no-pic
                                                      # (Equivalent to -fPIC)
            'GCC_ENABLE_CPP_EXCEPTIONS': 'NO',        # -fno-exceptions
            'GCC_ENABLE_CPP_RTTI': 'NO',              # -fno-rtti
            'GCC_ENABLE_PASCAL_STRINGS': 'NO',        # No -mpascal-strings
            'PREBINDING': 'NO',                       # No -Wl,-prebind
            'MACOSX_DEPLOYMENT_TARGET': '10.13',      # -mmacosx-version-min=10.13
            'USE_HEADERMAP': 'NO',
            'OTHER_CFLAGS': [
              '-fno-strict-aliasing',
            ],
            'WARNING_CFLAGS': [
              '-Wall',
              '-Wendif-labels',
              '-W',
              '-Wno-unused-parameter',
            ],
          },
        }
      ],
      [
        'clang==1', {
          'xcode_settings': {
            'GCC_VERSION': 'com.apple.compilers.llvm.clang.1_0',
            'CLANG_CXX_LANGUAGE_STANDARD': 'gnu++1y',  # -std=gnu++1y
            'CLANG_CXX_LIBRARY': 'libc++',
          }
        }
      ]
    ],
    'target_conditions': [
      ['_type!="executable" and OS=="linux"', {
          'cflags': [ '-fPIC' ],
          'ldflags': [ '-fPIC' ]
        },
      ],
    ],

    'default_configuration': 'Release',
    "configurations": {
      "Release": {
        "variables": {
          "v8_enable_handle_zapping": 0
        },
        "cflags": [ "-O3" ]
      },
      "Debug": {
        "variables": {
          "v8_enable_handle_zapping": 1
        },
        "defines": [ "DEBUG", "_DEBUG", "V8_ENABLE_CHECKS" ],
        "cflags": [ "-g", "-O0" ],
        'conditions': [
          [
            'clang==1', {
              'cflags': [ '-fno-limit-debug-info' ],
              'ldflags': [ '-fno-limit-debug-info' ]
            }
          ]
        ],
      }
    }
  },
}
