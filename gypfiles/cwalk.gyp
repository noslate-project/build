{
  'targets': [
    {
      'target_name': 'libcwalk',
      'type': 'static_library',
      'variables': {
        'cwalk_dir': '../../vendor/cwalk',
      },
      'direct_dependent_settings': {
        'include_dirs': [
          '<(cwalk_dir)/include'
        ]
      },
      'include_dirs': [
        '<(cwalk_dir)/include'
      ],
      'sources': [
        '<(cwalk_dir)/src/cwalk.c'
      ]
    }
  ]
}
