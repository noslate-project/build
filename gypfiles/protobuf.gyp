# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

{
  'variables': {
    'protobuf_source_dir': '../../vendor/protobuf',
  },
  'conditions': [
    ['OS!="win"', {
      'variables': {
        'config_h_dir':
          './protobuf',  # crafted for gcc/linux.
      },
    }, {  # else, OS=="win"
      'variables': {
        'config_h_dir':
          'vsprojects',  # crafted for msvc.
      },
      'target_defaults': {
        'msvs_disabled_warnings': [
          4018,  # signed/unsigned mismatch in comparison
          4244,  # implicit conversion, possible loss of data
          4355,  # 'this' used in base member initializer list
        ],
        'defines!': [
          'WIN32_LEAN_AND_MEAN',  # Protobuf defines this itself.
        ],
      },
    }]
  ],

  'target_defaults': {
    # Putting these explicitly here so not to depend on `common.gypi`.
    # `common.gypi` need to be more general because it is used to build userland native addons.
    # Refs: https://github.com/nodejs/node-gyp/issues/1118
    'cflags': [ '-w' ],
    'xcode_settings': {
      'WARNING_CFLAGS': [
        '-w',
      ],
    },

    'conditions': [
      ['OS == "linux" and llvm_version != "0.0"', {
        'libraries': ['-latomic'],
      }],
    ],
  },
  'targets': [
    # The "lite" lib is about 1/7th the size of the heavy lib,
    # but it doesn't support some of the more exotic features of
    # protobufs, like reflection.  To generate C++ code that can link
    # against the lite version of the library, add the option line:
    #
    #   option optimize_for = LITE_RUNTIME;
    #
    # to your .proto file.
    {
      'target_name': 'protobuf_lite',
      'type': 'static_library',
      'toolsets': ['host', 'target'],

      'sources': [
        '<(protobuf_source_dir)/src/google/protobuf/stubs/atomicops.h',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/atomicops_internals_arm_gcc.h',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/atomicops_internals_atomicword_compat.h',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/atomicops_internals_macosx.h',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/atomicops_internals_mips_gcc.h',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/atomicops_internals_x86_gcc.cc',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/atomicops_internals_x86_gcc.h',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/atomicops_internals_x86_msvc.cc',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/atomicops_internals_x86_msvc.h',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/common.h',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/once.h',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/platform_macros.h',
        '<(protobuf_source_dir)/src/google/protobuf/extension_set.h',
        '<(protobuf_source_dir)/src/google/protobuf/generated_message_util.h',
        '<(protobuf_source_dir)/src/google/protobuf/message_lite.h',
        '<(protobuf_source_dir)/src/google/protobuf/repeated_field.h',
        '<(protobuf_source_dir)/src/google/protobuf/unknown_field_set.cc',
        '<(protobuf_source_dir)/src/google/protobuf/unknown_field_set.h',
        '<(protobuf_source_dir)/src/google/protobuf/wire_format_lite.h',
        '<(protobuf_source_dir)/src/google/protobuf/wire_format_lite_inl.h',
        '<(protobuf_source_dir)/src/google/protobuf/io/coded_stream.h',
        '<(protobuf_source_dir)/src/google/protobuf/io/zero_copy_stream.h',
        '<(protobuf_source_dir)/src/google/protobuf/io/zero_copy_stream_impl_lite.h',

        '<(protobuf_source_dir)/src/google/protobuf/stubs/common.cc',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/once.cc',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/hash.h',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/map-util.h',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/stl_util-inl.h',
        '<(protobuf_source_dir)/src/google/protobuf/extension_set.cc',
        '<(protobuf_source_dir)/src/google/protobuf/generated_message_util.cc',
        '<(protobuf_source_dir)/src/google/protobuf/message_lite.cc',
        '<(protobuf_source_dir)/src/google/protobuf/repeated_field.cc',
        '<(protobuf_source_dir)/src/google/protobuf/wire_format_lite.cc',
        '<(protobuf_source_dir)/src/google/protobuf/io/coded_stream.cc',
        '<(protobuf_source_dir)/src/google/protobuf/io/coded_stream_inl.h',
        '<(protobuf_source_dir)/src/google/protobuf/io/zero_copy_stream.cc',
        '<(protobuf_source_dir)/src/google/protobuf/io/zero_copy_stream_impl_lite.cc',
        '<(config_h_dir)/config.h',
      ],
      'include_dirs': [
        '<(config_h_dir)',
        '<(protobuf_source_dir)/src',
      ],
      # This macro must be defined to suppress the use of dynamic_cast<>,
      # which requires RTTI.
      'defines': [
        'GOOGLE_PROTOBUF_NO_RTTI',
        'GOOGLE_PROTOBUF_NO_STATIC_INITIALIZER',
      ],

      'direct_dependent_settings': {
        'include_dirs': [
          '<(config_h_dir)',
          '<(protobuf_source_dir)/src',
        ],
        'defines': [
          'GOOGLE_PROTOBUF_NO_RTTI',
          'GOOGLE_PROTOBUF_NO_STATIC_INITIALIZER',
        ],
      },
    },
    # This is the full, heavy protobuf lib that's needed for c++ .proto's
    # that don't specify the LITE_RUNTIME option.  The protocol
    # compiler itself (protoc) falls into that category.
    #
    # DO NOT LINK AGAINST THIS TARGET IN CHROME CODE  --agl
    {
      'target_name': 'protobuf_full_do_not_use',
      'type': 'static_library',
      'toolsets': ['host','target'],
      'sources': [
        '<(protobuf_source_dir)/src/google/protobuf/descriptor.h',
        '<(protobuf_source_dir)/src/google/protobuf/descriptor.pb.h',
        '<(protobuf_source_dir)/src/google/protobuf/descriptor_database.h',
        '<(protobuf_source_dir)/src/google/protobuf/dynamic_message.h',
        '<(protobuf_source_dir)/src/google/protobuf/generated_message_reflection.h',
        '<(protobuf_source_dir)/src/google/protobuf/message.h',
        '<(protobuf_source_dir)/src/google/protobuf/reflection_ops.h',
        '<(protobuf_source_dir)/src/google/protobuf/service.h',
        '<(protobuf_source_dir)/src/google/protobuf/text_format.h',
        '<(protobuf_source_dir)/src/google/protobuf/wire_format.h',
        '<(protobuf_source_dir)/src/google/protobuf/io/gzip_stream.h',
        '<(protobuf_source_dir)/src/google/protobuf/io/printer.h',
        '<(protobuf_source_dir)/src/google/protobuf/io/tokenizer.h',
        '<(protobuf_source_dir)/src/google/protobuf/io/zero_copy_stream_impl.h',

        '<(protobuf_source_dir)/src/google/protobuf/stubs/stringprintf.cc',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/stringprintf.h',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/strutil.cc',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/strutil.h',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/substitute.cc',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/substitute.h',
        '<(protobuf_source_dir)/src/google/protobuf/stubs/structurally_valid.cc',
        '<(protobuf_source_dir)/src/google/protobuf/descriptor.cc',
        '<(protobuf_source_dir)/src/google/protobuf/descriptor.pb.cc',
        '<(protobuf_source_dir)/src/google/protobuf/descriptor_database.cc',
        '<(protobuf_source_dir)/src/google/protobuf/dynamic_message.cc',
        '<(protobuf_source_dir)/src/google/protobuf/extension_set_heavy.cc',
        '<(protobuf_source_dir)/src/google/protobuf/generated_message_reflection.cc',
        '<(protobuf_source_dir)/src/google/protobuf/message.cc',
        '<(protobuf_source_dir)/src/google/protobuf/reflection_ops.cc',
        '<(protobuf_source_dir)/src/google/protobuf/service.cc',
        '<(protobuf_source_dir)/src/google/protobuf/text_format.cc',
        '<(protobuf_source_dir)/src/google/protobuf/wire_format.cc',
        # This file pulls in zlib, but it's not actually used by protoc, so
        # instead of compiling zlib for the host, let's just exclude this.
        # '<(protobuf_source_dir)/src/<(protobuf_source_dir)/src/google/protobuf/io/gzip_stream.cc',
        '<(protobuf_source_dir)/src/google/protobuf/io/printer.cc',
        '<(protobuf_source_dir)/src/google/protobuf/io/strtod.cc',
        '<(protobuf_source_dir)/src/google/protobuf/io/tokenizer.cc',
        '<(protobuf_source_dir)/src/google/protobuf/io/zero_copy_stream_impl.cc',
      ],
      'include_dirs': [
        '<(config_h_dir)',
        '<(protobuf_source_dir)/src',
      ],
      'dependencies': [
        'protobuf_lite',
      ],
      'export_dependent_settings': [
        'protobuf_lite',
      ],
    },
    {
      'target_name': 'protoc',
      'conditions': [
        ['OS!="ios"', {
          'type': 'executable',
          'toolsets': ['host'],
          'sources': [
            '<(protobuf_source_dir)/src/google/protobuf/compiler/code_generator.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/command_line_interface.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/importer.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/parser.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/code_generator.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/command_line_interface.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/importer.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/parser.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/plugin.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/plugin.pb.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/subprocess.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/subprocess.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/zip_writer.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/zip_writer.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_enum.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_enum.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_enum_field.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_enum_field.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_extension.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_extension.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_field.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_field.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_file.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_file.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_generator.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_helpers.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_helpers.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_message.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_message.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_message_field.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_message_field.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_primitive_field.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_primitive_field.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_service.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_service.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_string_field.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/cpp/cpp_string_field.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_context.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_context.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_doc_comment.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_doc_comment.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_enum.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_enum.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_enum_field.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_enum_field.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_extension.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_extension.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_field.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_field.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_file.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_file.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_generator.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_generator_factory.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_helpers.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_helpers.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_lazy_message_field.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_lazy_message_field.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_message.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_message.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_message_field.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_message_field.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_name_resolver.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_primitive_field.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_primitive_field.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_service.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_service.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_shared_code_generator.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_string_field.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/java/java_string_field.h',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/python/python_generator.cc',
            '<(protobuf_source_dir)/src/google/protobuf/compiler/main.cc',
          ],
          'dependencies': [
            'protobuf_full_do_not_use',
          ],
          'include_dirs': [
            '<(config_h_dir)',
            '<(protobuf_source_dir)/src',
          ],
#        }, {  # else, OS=="ios"
#          'type': 'none',
#          'variables': {
#            'ninja_output_dir': 'ninja-protoc',
#            # Gyp to rerun
#            're_run_targets': [
#              'third_party/protobuf/protobuf.gyp',
#            ],
#          },
#          'includes': ['../../build/ios/mac_build.gypi'],
#          'actions': [
#            {
#              'action_name': 'compile protoc',
#              'inputs': [],
#              'outputs': [],
#              'action': [
#                '<@(ninja_cmd)',
#                'protoc',
#              ],
#              'message': 'Generating the C++ protocol buffers compiler',
#            },
#            {
#              'action_name': 'copy protoc',
#              'inputs': [
#                '<(ninja_product_dir)/protoc',
#              ],
#              'outputs': [
#                '<(PRODUCT_DIR)/protoc',
#              ],
#              'action': [
#                'cp',
#                '<(ninja_product_dir)/protoc',
#                '<(PRODUCT_DIR)/protoc',
#              ],
#            },
#          ],
        }],
      ],
    },
    {
      # Generate the python module needed by all protoc-generated Python code.
      'target_name': 'py_proto',
      'type': 'none',
      'copies': [
        {
          'destination': '<(PRODUCT_DIR)/pyproto/google/',
          'files': [
            # google/ module gets an empty __init__.py.
            '__init__.py',
          ],
        },
        {
          'destination': '<(PRODUCT_DIR)/pyproto/google/protobuf',
          'files': [
            'python/google/protobuf/__init__.py',
            'python/google/protobuf/descriptor.py',
            'python/google/protobuf/message.py',
            'python/google/protobuf/reflection.py',
            'python/google/protobuf/service.py',
            'python/google/protobuf/service_reflection.py',
            'python/google/protobuf/text_format.py',

            # TODO(ncarter): protoc's python generator treats descriptor.proto
            # specially, but it's not possible to trigger the special treatment
            # unless you run protoc from ./<(protobuf_source_dir)/src/src (the treatment is based
            # on the path to the .proto file matching a constant exactly).
            # I'm not sure how to convince gyp to execute a rule from a
            # different directory.  Until this is resolved, use a copy of
            # descriptor_pb2.py that I manually generated.
            'descriptor_pb2.py',
          ],
        },
        {
          'destination': '<(PRODUCT_DIR)/pyproto/google/protobuf/internal',
          'files': [
            'python/google/protobuf/internal/__init__.py',
            'python/google/protobuf/internal/api_implementation.py',
            'python/google/protobuf/internal/containers.py',
            'python/google/protobuf/internal/cpp_message.py',
            'python/google/protobuf/internal/decoder.py',
            'python/google/protobuf/internal/encoder.py',
            'python/google/protobuf/internal/generator_test.py',
            'python/google/protobuf/internal/message_listener.py',
            'python/google/protobuf/internal/python_message.py',
            'python/google/protobuf/internal/type_checkers.py',
            'python/google/protobuf/internal/wire_format.py',
          ],
        },
      ],
     },
  ],
}
