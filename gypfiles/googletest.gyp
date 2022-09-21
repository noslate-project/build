{
  'variables': {
    'googletest_dir': '../../vendor/googletest',
    'gtest_dir': '<(googletest_dir)/googletest',
  },
  'targets': [
    {
      'target_name': 'gtest',
      'type': 'static_library',
      'sources': [
        '<(gtest_dir)/src/gtest_main.cc',
        '<(gtest_dir)/src/gtest-all.cc',
      ],
      'include_dirs': [
        '<(gtest_dir)/include',
        '<(gtest_dir)/',
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(gtest_dir)/include',
        ],
      }
    },
    {
      'target_name': 'gtest_prod',
      'type': 'none',
      'sources': [
        '<(gtest_dir)/include/gtest_prod.h'
      ],
      'include_dirs': [
        '<(gtest_dir)/include',
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(gtest_dir)/include',
        ],
      }
    }
  ]
}
