{
  'variables': {},
  'targets': [
    {
      'target_name': 'noslate',
      'type': 'none',
      'dependencies': [
        '<(noslate_noslated_dir)/noslated.gyp:noslated',
        '<(noslate_aworker_dir)/aworker.gyp:aworker',
        '<(noslate_node_dir)/node.gyp:node',
      ]
    }
  ]
}
