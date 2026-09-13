---
commit: 09bfaaefdcbe2fb3705bece2fcc643c9a95da478
spec-digests: {"spec01.md":"86b14c10ac42f521dc2054c79268b8cc4bf7694bf87db0b7272f60ca42aca406"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/the-exit-flag-tests-race-each-other/specs/spec01.md: exit 0

Command SHA-256: da8d1c97c3ab894a30569244a26d9fd818dfce9af77b32d8b4fadbd5b806043c

```text
   Compiling proc-macro2 v1.0.107
   Compiling unicode-ident v1.0.24
   Compiling quote v1.0.47
   Compiling libc v0.2.189
   Compiling serde_core v1.0.229
   Compiling memchr v2.8.3
   Compiling shlex v2.0.1
   Compiling find-msvc-tools v0.1.9
   Compiling cfg-if v1.0.4
   Compiling pin-project-lite v0.2.17
   Compiling smallvec v1.15.2
   Compiling itoa v1.0.18
   Compiling bytes v1.12.1
   Compiling once_cell v1.21.4
   Compiling parking_lot_core v0.9.12
   Compiling scopeguard v1.2.0
   Compiling pkg-config v0.3.33
   Compiling lock_api v0.4.14
   Compiling log v0.4.33
   Compiling serde v1.0.229
   Compiling futures-core v0.3.33
   Compiling crossbeam-utils v0.8.22
   Compiling stable_deref_trait v1.2.1
   Compiling tracing-core v0.1.36
   Compiling futures-sink v0.3.33
   Compiling zmij v1.0.23
   Compiling futures-channel v0.3.33
   Compiling aho-corasick v1.1.4
   Compiling serde_json v1.0.151
   Compiling syn v2.0.119
   Compiling syn v3.0.3
   Compiling dunce v1.0.5
   Compiling regex-syntax v0.8.11
   Compiling fs_extra v1.3.0
   Compiling jobserver v0.1.35
   Compiling errno v0.3.14
   Compiling signal-hook-registry v1.4.8
   Compiling cc v1.4.0
   Compiling parking_lot v0.12.5
   Compiling socket2 v0.6.5
   Compiling mio v1.2.2
   Compiling crossbeam-epoch v0.9.20
   Compiling regex-automata v0.4.16
   Compiling typenum v1.20.1
   Compiling futures-task v0.3.33
   Compiling cmake v0.1.58
   Compiling bitflags v2.13.1
   Compiling slab v0.4.12
   Compiling crossbeam-deque v0.8.7
   Compiling futures-io v0.3.33
   Compiling http v1.4.2
   Compiling getrandom v0.4.3
   Compiling hybrid-array v0.4.13
   Compiling aws-lc-sys v0.43.0
   Compiling rand_core v0.10.1
   Compiling litemap v0.8.2
   Compiling aws-lc-rs v1.17.3
   Compiling percent-encoding v2.3.2
   Compiling http-body v1.1.0
   Compiling same-file v1.0.6
   Compiling thiserror v2.0.19
   Compiling synstructure v0.13.2
   Compiling writeable v0.6.3
   Compiling walkdir v2.5.0
   Compiling block-buffer v0.12.1
   Compiling serde_derive v1.0.229
   Compiling thiserror-impl v2.0.19
   Compiling crypto-common v0.2.2
   Compiling bstr v1.13.0
   Compiling utf8_iter v1.0.4
   Compiling zeroize v1.9.0
   Compiling tower-service v0.3.3
   Compiling httparse v1.10.1
   Compiling icu_properties_data v2.2.0
   Compiling const-oid v0.10.2
   Compiling icu_normalizer_data v2.2.0
   Compiling globset v0.4.19
   Compiling digest v0.11.3
   Compiling chacha20 v0.10.1
   Compiling notify-types v2.1.0
   Compiling tokio-macros v2.7.1
   Compiling zerofrom-derive v0.1.7
   Compiling yoke-derive v0.8.2
   Compiling tracing-attributes v0.1.31
   Compiling zerovec-derive v0.11.3
   Compiling tokio v1.53.1
   Compiling displaydoc v0.2.6
   Compiling futures-macro v0.3.33
   Compiling fsevent-sys v4.1.0
   Compiling cpufeatures v0.3.0
   Compiling try-lock v0.2.5
   Compiling notify v8.2.0
   Compiling sha2 v0.11.0
   Compiling zerofrom v0.1.8
   Compiling want v0.3.1
   Compiling rand v0.10.2
   Compiling tracing v0.1.44
   Compiling futures-util v0.3.33
   Compiling yoke v0.8.3
   Compiling ignore v0.4.31
   Compiling rustls-pki-types v1.15.1
   Compiling async-trait v0.1.91
   Compiling form_urlencoded v1.2.2
   Compiling sync_wrapper v1.0.2
   Compiling untrusted v0.9.0
   Compiling httpdate v1.0.3
   Compiling tower-layer v0.3.3
   Compiling atomic-waker v1.1.2
   Compiling rustls v0.23.42
   Compiling siphasher v1.0.3
   Compiling core-foundation-sys v0.8.7
   Compiling subtle v2.6.1
   Compiling base64 v0.22.1
   Compiling ipnet v2.12.0
   Compiling rand_core v0.6.4
   Compiling phf_shared v0.11.3
   Compiling rand v0.8.7
   Compiling http-body-util v0.1.4
   Compiling security-framework-sys v2.17.0
   Compiling core-foundation v0.10.1
   Compiling regex v1.13.1
   Compiling zstd-sys v2.0.16+zstd.1.5.7
   Compiling zerovec v0.11.6
   Compiling zerotrie v0.2.4
   Compiling phf_generator v0.11.3
   Compiling security-framework v3.7.0
   Compiling audit v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/hotreload/audit)
   Compiling phf_macros v0.11.3
   Compiling option-ext v0.2.0
   Compiling winnow v1.0.4
   Compiling toml_parser v1.1.2+spec-1.1.0
   Compiling hotreload v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/hotreload)
   Compiling phf v0.11.3
   Compiling tinystr v0.8.3
   Compiling potential_utf v0.1.5
   Compiling icu_locale_core v2.2.0
   Compiling icu_collections v2.2.0
   Compiling dirs-sys v0.5.0
   Compiling serde_spanned v1.1.1
   Compiling toml_datetime v1.1.1+spec-1.1.0
   Compiling doxygen-rs v0.4.2
   Compiling toml_writer v1.1.2+spec-1.1.0
   Compiling dirs v6.0.0
   Compiling zstd-safe v7.2.4
   Compiling virtue v0.0.18
   Compiling toml v1.1.3+spec-1.1.0
   Compiling hyper v1.11.0
   Compiling util v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/util)
   Compiling tower v0.5.3
   Compiling icu_provider v2.2.0
   Compiling tokio-util v0.7.19
   Compiling lmdb-master-sys v0.2.6
   Compiling bincode_derive v2.0.1
   Compiling icu_properties v2.2.0
   Compiling icu_normalizer v2.2.0
   Compiling hyper-util v0.1.20
   Compiling base v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/base)
   Compiling idna_adapter v1.2.2
   Compiling idna v1.1.0
   Compiling bincode v1.3.3
   Compiling url v2.5.8
   Compiling ingest_config v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/ingest/config)
   Compiling tower-http v0.6.11
   Compiling crossbeam-queue v0.3.13
   Compiling byteorder v1.5.0
   Compiling unty v0.0.4
   Compiling heed-traits v0.20.0
   Compiling bincode v2.0.1
   Compiling heed-types v0.20.1
   Compiling synchronoise v1.0.1
   Compiling page_size v0.6.0
   Compiling math v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/math)
   Compiling memmap2 v0.9.11
   Compiling rayon-core v1.13.0
   Compiling either v1.17.0
   Compiling rustix v1.1.4
   Compiling futures-executor v0.3.33
   Compiling utf8parse v0.2.2
   Compiling futures v0.3.33
   Compiling heed v0.20.5
   Compiling transport-macros v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/transport/macros)
   Compiling anstyle-parse v1.0.0
   Compiling colorchoice v1.0.5
   Compiling is_terminal_polyfill v1.70.2
   Compiling anstyle-query v1.1.5
   Compiling anstyle v1.0.14
   Compiling strsim v0.11.1
   Compiling ryu v1.0.23
   Compiling anstream v1.0.0
   Compiling clap_lex v1.1.0
   Compiling mime v0.3.17
   Compiling heck v0.5.0
   Compiling serde_urlencoded v0.7.1
   Compiling transport v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/transport)
   Compiling rayon v1.12.0
   Compiling clap_derive v4.6.4
   Compiling axum-core v0.5.6
   Compiling serde_path_to_error v0.1.20
   Compiling matchit v0.8.4
   Compiling fastrand v2.5.0
   Compiling terminal_size v0.4.4
   Compiling clap_builder v4.6.2
   Compiling axum v0.8.9
   Compiling tempfile v3.27.0
   Compiling clap v4.6.4
   Compiling zstd v0.13.3
   Compiling store_core v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store/core)
   Compiling test_support v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/.cartridge/tests/support)
   Compiling rustls-webpki v0.103.13
   Compiling tokio-rustls v0.26.4
   Compiling rustls-platform-verifier v0.7.0
   Compiling hyper-rustls v0.27.9
   Compiling reqwest v0.13.4
   Compiling llm v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/llm)
   Compiling config v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/config)
   Compiling graph v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/graph)
   Compiling gnn v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/gnn)
   Compiling identity v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/identity)
   Compiling hub v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/hub)
   Compiling retrieval-piece v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/retrieval/piece)
   Compiling tick v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/tick)
   Compiling ingest v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/ingest)
   Compiling bootstrap v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/bootstrap)
   Compiling retrieval v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/retrieval)
   Compiling tick_loop v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/tick/loop)
   Compiling store v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store)
   Compiling health v0.1.0 (/Users/feb/dev/cartridge/memory.ctg/src/health)
   Compiling rpc v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/rpc)
   Compiling commands v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/commands)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 27.11s
     Running ../../.cartridge/tests/unit/src/commands/tests/exit_status.rs (target/debug/deps/exit_status-fcf4e62f7ca39f0e)

running 1 test
test a_reported_failure_is_what_the_exit_status_reads ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Compiling serde_core v1.0.229
   Compiling crossbeam-utils v0.8.22
   Compiling syn v2.0.119
   Compiling serde_json v1.0.151
   Compiling smallvec v1.15.2
   Compiling regex-syntax v0.8.11
   Compiling rustix v1.1.4
   Compiling parking_lot_core v0.9.12
   Compiling parking_lot v0.12.5
   Compiling regex-automata v0.4.16
   Compiling crossbeam-epoch v0.9.20
   Compiling crossbeam-queue v0.3.13
   Compiling synchronoise v1.0.1
   Compiling crossbeam-deque v0.8.7
   Compiling globset v0.4.19
   Compiling ignore v0.4.31
   Compiling phf_macros v0.11.3
   Compiling tracing-attributes v0.1.31
   Compiling tokio-macros v2.7.1
   Compiling phf v0.11.3
   Compiling tokio v1.53.1
   Compiling tracing v0.1.44
   Compiling doxygen-rs v0.4.2
   Compiling bitflags v2.13.1
   Compiling serde v1.0.229
   Compiling lmdb-master-sys v0.2.6
   Compiling notify-types v2.1.0
   Compiling notify v8.2.0
   Compiling bincode v1.3.3
   Compiling bincode v2.0.1
   Compiling heed-types v0.20.1
   Compiling tempfile v3.27.0
   Compiling heed v0.20.5
   Compiling util v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/util)
   Compiling base v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/base)
   Compiling math v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/math)
   Compiling store_core v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store/core)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 6.50s
     Running unittests src/lib.rs (target/debug/deps/store_core-03cee6b718ef367c)

running 1 test
test lock::lock_tests::inherited_description_requires_the_bounded_retry ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 66 filtered out; finished in 0.00s

   Compiling commands v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/commands)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 6.71s
     Running unittests src/lib.rs (target/debug/deps/commands-0681a46a646d8621)

running 1 test
test commands_serve::watchdog_handover_tests::a_handover_with_no_listener_frees_the_store_and_returns ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 110 filtered out; finished in 0.00s


```
