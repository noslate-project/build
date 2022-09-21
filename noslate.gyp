{
  'variables': {},
  'targets': [
    {
      'target_name': 'noslate',
      'type': 'none',
      'dependencies': [
        '<(noslate_alice_dir)/alice.gyp:alice',
        '<(noslate_aworker_dir)/aworker.gyp:aworker',
        '<(noslate_node_dir)/node.gyp:node',
      ]
    }
  ]
}
