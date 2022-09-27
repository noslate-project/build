{
  'targets': [
    {
      'target_name': 'libcurl',
      'type': 'static_library',
      'variables': {
        'curl_dir': '../../vendor/curl',
      },
      'direct_dependent_settings': {
        'include_dirs': [
          '<(curl_dir)/include'
        ],
      },
      'dependencies': [
        '<(noslate_brotli_gyp):brotli',
        '<(noslate_cares_gyp):cares',
        '<(noslate_nghttp2_gyp):nghttp2',
        # Version not supported by curl
        # '<(noslate_ngtcp2_gyp):nghttp3',
        # '<(noslate_ngtcp2_gyp):ngtcp2',
        '<(noslate_openssl_gyp):openssl',
        '<(noslate_zlib_gyp):zlib',
      ],
      'defines': [
        'BUILDING_LIBCURL=1',
        'CURL_STATICLIB=1',
        # features
        'USE_ARES=1',
        'USE_NGHTTP2=1',
        # Version not supported by curl
        # 'USE_NGHTTP3=1',
        # 'USE_NGTCP2_CRYPTO_OPENSSL=1',
        # 'USE_NGTCP2=1',
        'USE_OPENSSL=1',

        'HAVE_CONFIG_H=1',
      ],
      'conditions': [
        ['OS == "linux"', {
          'defines': [
            'HAVE_LINUX_TCP_H=1',
            'HAVE_MSG_NOSIGNAL=1',
          ],
        }],
      ],
      'include_dirs': [
        './curl',
        '<(curl_dir)/include',
        '<(curl_dir)/lib',
      ],
      'sources': [
        '<(curl_dir)/lib/vauth/cleartext.c',
        '<(curl_dir)/lib/vauth/cram.c',
        '<(curl_dir)/lib/vauth/digest.c',
        '<(curl_dir)/lib/vauth/digest.h',
        '<(curl_dir)/lib/vauth/digest_sspi.c',
        '<(curl_dir)/lib/vauth/gsasl.c',
        '<(curl_dir)/lib/vauth/krb5_gssapi.c',
        '<(curl_dir)/lib/vauth/krb5_sspi.c',
        '<(curl_dir)/lib/vauth/ntlm.c',
        '<(curl_dir)/lib/vauth/ntlm.h',
        '<(curl_dir)/lib/vauth/ntlm_sspi.c',
        '<(curl_dir)/lib/vauth/oauth2.c',
        '<(curl_dir)/lib/vauth/spnego_gssapi.c',
        '<(curl_dir)/lib/vauth/spnego_sspi.c',
        '<(curl_dir)/lib/vauth/vauth.c',
        '<(curl_dir)/lib/vauth/vauth.h',
        '<(curl_dir)/lib/vquic/ngtcp2.c',
        '<(curl_dir)/lib/vquic/ngtcp2.h',
        '<(curl_dir)/lib/vquic/quiche.c',
        '<(curl_dir)/lib/vquic/quiche.h',
        '<(curl_dir)/lib/vquic/vquic.c',
        '<(curl_dir)/lib/vquic/vquic.h',
        '<(curl_dir)/lib/vssh/libssh.c',
        '<(curl_dir)/lib/vssh/libssh2.c',
        '<(curl_dir)/lib/vssh/ssh.h',
        '<(curl_dir)/lib/vssh/wolfssh.c',
        '<(curl_dir)/lib/vssh/wolfssh.h',
        '<(curl_dir)/lib/vtls/bearssl.c',
        '<(curl_dir)/lib/vtls/bearssl.h',
        '<(curl_dir)/lib/vtls/gskit.c',
        '<(curl_dir)/lib/vtls/gskit.h',
        '<(curl_dir)/lib/vtls/gtls.c',
        '<(curl_dir)/lib/vtls/gtls.h',
        '<(curl_dir)/lib/vtls/keylog.c',
        '<(curl_dir)/lib/vtls/keylog.h',
        '<(curl_dir)/lib/vtls/mbedtls.c',
        '<(curl_dir)/lib/vtls/mbedtls.h',
        '<(curl_dir)/lib/vtls/mbedtls_threadlock.c',
        '<(curl_dir)/lib/vtls/mbedtls_threadlock.h',
        '<(curl_dir)/lib/vtls/mesalink.c',
        '<(curl_dir)/lib/vtls/mesalink.h',
        '<(curl_dir)/lib/vtls/nss.c',
        '<(curl_dir)/lib/vtls/nssg.h',
        '<(curl_dir)/lib/vtls/openssl.c',
        '<(curl_dir)/lib/vtls/openssl.h',
        '<(curl_dir)/lib/vtls/rustls.c',
        '<(curl_dir)/lib/vtls/rustls.h',
        '<(curl_dir)/lib/vtls/schannel.c',
        '<(curl_dir)/lib/vtls/schannel.h',
        '<(curl_dir)/lib/vtls/schannel_verify.c',
        '<(curl_dir)/lib/vtls/sectransp.c',
        '<(curl_dir)/lib/vtls/sectransp.h',
        '<(curl_dir)/lib/vtls/vtls.c',
        '<(curl_dir)/lib/vtls/vtls.h',
        '<(curl_dir)/lib/vtls/wolfssl.c',
        '<(curl_dir)/lib/vtls/wolfssl.h',
        '<(curl_dir)/lib/altsvc.c',
        '<(curl_dir)/lib/altsvc.h',
        '<(curl_dir)/lib/amigaos.c',
        '<(curl_dir)/lib/amigaos.h',
        '<(curl_dir)/lib/arpa_telnet.h',
        '<(curl_dir)/lib/asyn-ares.c',
        '<(curl_dir)/lib/asyn-thread.c',
        '<(curl_dir)/lib/asyn.h',
        '<(curl_dir)/lib/base64.c',
        '<(curl_dir)/lib/bufref.c',
        '<(curl_dir)/lib/bufref.h',
        '<(curl_dir)/lib/c-hyper.c',
        '<(curl_dir)/lib/c-hyper.h',
        '<(curl_dir)/lib/config-amigaos.h',
        '<(curl_dir)/lib/config-dos.h',
        '<(curl_dir)/lib/config-mac.h',
        '<(curl_dir)/lib/config-os400.h',
        '<(curl_dir)/lib/config-plan9.h',
        '<(curl_dir)/lib/config-riscos.h',
        '<(curl_dir)/lib/config-tpf.h',
        '<(curl_dir)/lib/config-vxworks.h',
        '<(curl_dir)/lib/config-win32.h',
        '<(curl_dir)/lib/config-win32ce.h',
        '<(curl_dir)/lib/conncache.c',
        '<(curl_dir)/lib/conncache.h',
        '<(curl_dir)/lib/connect.c',
        '<(curl_dir)/lib/connect.h',
        '<(curl_dir)/lib/content_encoding.c',
        '<(curl_dir)/lib/content_encoding.h',
        '<(curl_dir)/lib/cookie.c',
        '<(curl_dir)/lib/cookie.h',
        '<(curl_dir)/lib/curl_addrinfo.c',
        '<(curl_dir)/lib/curl_addrinfo.h',
        '<(curl_dir)/lib/curl_base64.h',
        '<(curl_dir)/lib/curl_config.h',
        '<(curl_dir)/lib/curl_ctype.c',
        '<(curl_dir)/lib/curl_ctype.h',
        '<(curl_dir)/lib/curl_des.c',
        '<(curl_dir)/lib/curl_des.h',
        '<(curl_dir)/lib/curl_endian.c',
        '<(curl_dir)/lib/curl_endian.h',
        '<(curl_dir)/lib/curl_fnmatch.c',
        '<(curl_dir)/lib/curl_fnmatch.h',
        '<(curl_dir)/lib/curl_get_line.c',
        '<(curl_dir)/lib/curl_get_line.h',
        '<(curl_dir)/lib/curl_gethostname.c',
        '<(curl_dir)/lib/curl_gethostname.h',
        '<(curl_dir)/lib/curl_gssapi.c',
        '<(curl_dir)/lib/curl_gssapi.h',
        '<(curl_dir)/lib/curl_hmac.h',
        '<(curl_dir)/lib/curl_krb5.h',
        '<(curl_dir)/lib/curl_ldap.h',
        '<(curl_dir)/lib/curl_md4.h',
        '<(curl_dir)/lib/curl_md5.h',
        '<(curl_dir)/lib/curl_memory.h',
        '<(curl_dir)/lib/curl_memrchr.c',
        '<(curl_dir)/lib/curl_memrchr.h',
        '<(curl_dir)/lib/curl_multibyte.c',
        '<(curl_dir)/lib/curl_multibyte.h',
        '<(curl_dir)/lib/curl_ntlm_core.c',
        '<(curl_dir)/lib/curl_ntlm_core.h',
        '<(curl_dir)/lib/curl_ntlm_wb.c',
        '<(curl_dir)/lib/curl_ntlm_wb.h',
        '<(curl_dir)/lib/curl_path.c',
        '<(curl_dir)/lib/curl_path.h',
        '<(curl_dir)/lib/curl_printf.h',
        '<(curl_dir)/lib/curl_range.c',
        '<(curl_dir)/lib/curl_range.h',
        '<(curl_dir)/lib/curl_rtmp.c',
        '<(curl_dir)/lib/curl_rtmp.h',
        '<(curl_dir)/lib/curl_sasl.c',
        '<(curl_dir)/lib/curl_sasl.h',
        '<(curl_dir)/lib/curl_setup.h',
        '<(curl_dir)/lib/curl_setup_once.h',
        '<(curl_dir)/lib/curl_sha256.h',
        '<(curl_dir)/lib/curl_sspi.c',
        '<(curl_dir)/lib/curl_sspi.h',
        '<(curl_dir)/lib/curl_threads.c',
        '<(curl_dir)/lib/curl_threads.h',
        '<(curl_dir)/lib/curlx.h',
        '<(curl_dir)/lib/dict.c',
        '<(curl_dir)/lib/dict.h',
        '<(curl_dir)/lib/doh.c',
        '<(curl_dir)/lib/doh.h',
        '<(curl_dir)/lib/dotdot.c',
        '<(curl_dir)/lib/dotdot.h',
        '<(curl_dir)/lib/dynbuf.c',
        '<(curl_dir)/lib/dynbuf.h',
        '<(curl_dir)/lib/easy.c',
        '<(curl_dir)/lib/easygetopt.c',
        '<(curl_dir)/lib/easyif.h',
        '<(curl_dir)/lib/easyoptions.c',
        '<(curl_dir)/lib/easyoptions.h',
        '<(curl_dir)/lib/escape.c',
        '<(curl_dir)/lib/escape.h',
        '<(curl_dir)/lib/file.c',
        '<(curl_dir)/lib/file.h',
        '<(curl_dir)/lib/fileinfo.c',
        '<(curl_dir)/lib/fileinfo.h',
        '<(curl_dir)/lib/formdata.c',
        '<(curl_dir)/lib/formdata.h',
        '<(curl_dir)/lib/ftp.c',
        '<(curl_dir)/lib/ftp.h',
        '<(curl_dir)/lib/ftplistparser.c',
        '<(curl_dir)/lib/ftplistparser.h',
        '<(curl_dir)/lib/getenv.c',
        '<(curl_dir)/lib/getinfo.c',
        '<(curl_dir)/lib/getinfo.h',
        '<(curl_dir)/lib/gopher.c',
        '<(curl_dir)/lib/gopher.h',
        '<(curl_dir)/lib/hash.c',
        '<(curl_dir)/lib/hash.h',
        '<(curl_dir)/lib/hmac.c',
        '<(curl_dir)/lib/hostasyn.c',
        '<(curl_dir)/lib/hostcheck.c',
        '<(curl_dir)/lib/hostcheck.h',
        '<(curl_dir)/lib/hostip.c',
        '<(curl_dir)/lib/hostip.h',
        '<(curl_dir)/lib/hostip4.c',
        '<(curl_dir)/lib/hostip6.c',
        '<(curl_dir)/lib/hostsyn.c',
        '<(curl_dir)/lib/hsts.c',
        '<(curl_dir)/lib/hsts.h',
        '<(curl_dir)/lib/http.c',
        '<(curl_dir)/lib/http.h',
        '<(curl_dir)/lib/http2.c',
        '<(curl_dir)/lib/http2.h',
        '<(curl_dir)/lib/http_aws_sigv4.c',
        '<(curl_dir)/lib/http_aws_sigv4.h',
        '<(curl_dir)/lib/http_chunks.c',
        '<(curl_dir)/lib/http_chunks.h',
        '<(curl_dir)/lib/http_digest.c',
        '<(curl_dir)/lib/http_digest.h',
        '<(curl_dir)/lib/http_negotiate.c',
        '<(curl_dir)/lib/http_negotiate.h',
        '<(curl_dir)/lib/http_ntlm.c',
        '<(curl_dir)/lib/http_ntlm.h',
        '<(curl_dir)/lib/http_proxy.c',
        '<(curl_dir)/lib/http_proxy.h',
        '<(curl_dir)/lib/idn_win32.c',
        '<(curl_dir)/lib/if2ip.c',
        '<(curl_dir)/lib/if2ip.h',
        '<(curl_dir)/lib/imap.c',
        '<(curl_dir)/lib/imap.h',
        '<(curl_dir)/lib/inet_ntop.c',
        '<(curl_dir)/lib/inet_ntop.h',
        '<(curl_dir)/lib/inet_pton.c',
        '<(curl_dir)/lib/inet_pton.h',
        '<(curl_dir)/lib/krb5.c',
        '<(curl_dir)/lib/ldap.c',
        '<(curl_dir)/lib/llist.c',
        '<(curl_dir)/lib/llist.h',
        '<(curl_dir)/lib/md4.c',
        '<(curl_dir)/lib/md5.c',
        '<(curl_dir)/lib/memdebug.c',
        '<(curl_dir)/lib/memdebug.h',
        '<(curl_dir)/lib/mime.c',
        '<(curl_dir)/lib/mime.h',
        '<(curl_dir)/lib/mprintf.c',
        '<(curl_dir)/lib/mqtt.c',
        '<(curl_dir)/lib/mqtt.h',
        '<(curl_dir)/lib/multi.c',
        '<(curl_dir)/lib/multihandle.h',
        '<(curl_dir)/lib/multiif.h',
        '<(curl_dir)/lib/netrc.c',
        '<(curl_dir)/lib/netrc.h',
        '<(curl_dir)/lib/non-ascii.c',
        '<(curl_dir)/lib/non-ascii.h',
        '<(curl_dir)/lib/nonblock.c',
        '<(curl_dir)/lib/nonblock.h',
        '<(curl_dir)/lib/nwlib.c',
        '<(curl_dir)/lib/nwos.c',
        '<(curl_dir)/lib/openldap.c',
        '<(curl_dir)/lib/parsedate.c',
        '<(curl_dir)/lib/parsedate.h',
        '<(curl_dir)/lib/pingpong.c',
        '<(curl_dir)/lib/pingpong.h',
        '<(curl_dir)/lib/pop3.c',
        '<(curl_dir)/lib/pop3.h',
        '<(curl_dir)/lib/progress.c',
        '<(curl_dir)/lib/progress.h',
        '<(curl_dir)/lib/psl.c',
        '<(curl_dir)/lib/psl.h',
        '<(curl_dir)/lib/quic.h',
        '<(curl_dir)/lib/rand.c',
        '<(curl_dir)/lib/rand.h',
        '<(curl_dir)/lib/rename.c',
        '<(curl_dir)/lib/rename.h',
        '<(curl_dir)/lib/rtsp.c',
        '<(curl_dir)/lib/rtsp.h',
        '<(curl_dir)/lib/select.c',
        '<(curl_dir)/lib/select.h',
        '<(curl_dir)/lib/sendf.c',
        '<(curl_dir)/lib/sendf.h',
        '<(curl_dir)/lib/setopt.c',
        '<(curl_dir)/lib/setopt.h',
        '<(curl_dir)/lib/setup-os400.h',
        '<(curl_dir)/lib/setup-vms.h',
        '<(curl_dir)/lib/setup-win32.h',
        '<(curl_dir)/lib/sha256.c',
        '<(curl_dir)/lib/share.c',
        '<(curl_dir)/lib/share.h',
        '<(curl_dir)/lib/sigpipe.h',
        '<(curl_dir)/lib/slist.c',
        '<(curl_dir)/lib/slist.h',
        '<(curl_dir)/lib/smb.c',
        '<(curl_dir)/lib/smb.h',
        '<(curl_dir)/lib/smtp.c',
        '<(curl_dir)/lib/smtp.h',
        '<(curl_dir)/lib/sockaddr.h',
        '<(curl_dir)/lib/socketpair.c',
        '<(curl_dir)/lib/socketpair.h',
        '<(curl_dir)/lib/socks.c',
        '<(curl_dir)/lib/socks.h',
        '<(curl_dir)/lib/socks_gssapi.c',
        '<(curl_dir)/lib/socks_sspi.c',
        '<(curl_dir)/lib/speedcheck.c',
        '<(curl_dir)/lib/speedcheck.h',
        '<(curl_dir)/lib/splay.c',
        '<(curl_dir)/lib/splay.h',
        '<(curl_dir)/lib/strcase.c',
        '<(curl_dir)/lib/strcase.h',
        '<(curl_dir)/lib/strdup.c',
        '<(curl_dir)/lib/strdup.h',
        '<(curl_dir)/lib/strerror.c',
        '<(curl_dir)/lib/strerror.h',
        '<(curl_dir)/lib/strtok.c',
        '<(curl_dir)/lib/strtok.h',
        '<(curl_dir)/lib/strtoofft.c',
        '<(curl_dir)/lib/strtoofft.h',
        '<(curl_dir)/lib/system_win32.c',
        '<(curl_dir)/lib/system_win32.h',
        '<(curl_dir)/lib/telnet.c',
        '<(curl_dir)/lib/telnet.h',
        '<(curl_dir)/lib/tftp.c',
        '<(curl_dir)/lib/tftp.h',
        '<(curl_dir)/lib/timeval.c',
        '<(curl_dir)/lib/timeval.h',
        '<(curl_dir)/lib/transfer.c',
        '<(curl_dir)/lib/transfer.h',
        '<(curl_dir)/lib/url.c',
        '<(curl_dir)/lib/url.h',
        '<(curl_dir)/lib/urlapi-int.h',
        '<(curl_dir)/lib/urlapi.c',
        '<(curl_dir)/lib/urldata.h',
        '<(curl_dir)/lib/version.c',
        '<(curl_dir)/lib/version_win32.c',
        '<(curl_dir)/lib/version_win32.h',
        '<(curl_dir)/lib/warnless.c',
        '<(curl_dir)/lib/warnless.h',
        '<(curl_dir)/lib/wildcard.c',
        '<(curl_dir)/lib/wildcard.h',
        '<(curl_dir)/lib/x509asn1.c',
        '<(curl_dir)/lib/x509asn1.h',
      ],
    }
  ]
}