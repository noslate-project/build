{
  'variables': {
    'v8_enable_i18n_support%': 1,
    'ada_dir': '../../vendor/ada',
    'ada_sources': [
      '<(ada_dir)/include/ada.h',
      '<(ada_dir)/include/ada/ada_version.h',
      '<(ada_dir)/include/ada/character_sets.h',
      '<(ada_dir)/include/ada/character_sets-inl.h',
      '<(ada_dir)/include/ada/checkers.h',
      '<(ada_dir)/include/ada/checkers-inl.h',
      '<(ada_dir)/include/ada/common_defs.h',
      '<(ada_dir)/include/ada/encoding_type.h',
      '<(ada_dir)/include/ada/expected.h',
      '<(ada_dir)/include/ada/helpers.h',
      '<(ada_dir)/include/ada/implementation.h',
      '<(ada_dir)/include/ada/log.h',
      '<(ada_dir)/include/ada/parser.h',
      '<(ada_dir)/include/ada/scheme.h',
      '<(ada_dir)/include/ada/scheme-inl.h',
      '<(ada_dir)/include/ada/serializers.h',
      '<(ada_dir)/include/ada/state.h',
      '<(ada_dir)/include/ada/unicode.h',
      '<(ada_dir)/include/ada/url.h',
      '<(ada_dir)/include/ada/url-inl.h',
      '<(ada_dir)/src/ada.cpp',
      '<(ada_dir)/src/checkers.cpp',
      '<(ada_dir)/src/helpers.cpp',
      '<(ada_dir)/src/implementation.cpp',
      '<(ada_dir)/src/parser.cpp',
      '<(ada_dir)/src/serializers.cpp',
      '<(ada_dir)/src/unicode.cpp',
      '<(ada_dir)/src/url-getters.cpp',
      '<(ada_dir)/src/url-setters.cpp',
      '<(ada_dir)/src/url.cpp',
    ],
    'ada_singleheader': [
      '<(ada_dir)/singleheader/ada.cpp',
      '<(ada_dir)/singleheader/ada.h',
    ]
  },
  'targets': [
    {
      'target_name': 'ada_singleheader',
      'type': 'none',
      'sources': [ '<@(ada_sources)' ],
      'actions': [
        {
          'action_name': 'singleheader',
          'inputs': [
            '<(ada_dir)/singleheader/amalgamate.py',
            '<@(_sources)',
          ],
          'outputs': [
            '<@(ada_singleheader)',
          ],
          'action': ['<(python)', '<(ada_dir)/singleheader/amalgamate.py'],
        }
      ]
    },
    {
      'target_name': 'ada',
      'type': 'static_library',
      'include_dirs': ['<(ada_dir)/singleheader'],
      'direct_dependent_settings': {
        'include_dirs': ['<(ada_dir)/singleheader'],
      },
      'sources': [ '<@(ada_singleheader)' ],
      'conditions': [
        ['v8_enable_i18n_support==0', {
          'defines': ['ADA_HAS_ICU=0'],
        }],
        ['v8_enable_i18n_support==1', {
          'dependencies': [
            '<(icu_gyp_path):icui18n',
            '<(icu_gyp_path):icuuc',
          ],
        }],
        ['OS=="win" and v8_enable_i18n_support==1', {
          'dependencies': [
            '<(icu_gyp_path):icudata',
          ],
        }],
      ]
    },
  ]
}
