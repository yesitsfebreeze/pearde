---
commit: 1351865eb0e787cf819456aaa201c18eacf74406
spec-digests: {"spec01.md":"2479dab0760eb1ee3210a39dcca765a933930783eab9a65349f845d99f0d9370"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/memory-runs-once-in-the-daemon-and-attached-instances-never-hit-the-writer-lock/specs/spec01.md: exit 0

Command SHA-256: 447804458130255f3755cebf1e55438764d1bcfaffb96f0961859086c500250f

```text
   Compiling proc-macro2 v1.0.107
   Compiling quote v1.0.47
   Compiling unicode-ident v1.0.24
   Compiling libc v0.2.189
   Compiling serde_core v1.0.229
   Compiling find-msvc-tools v0.1.9
   Compiling shlex v2.0.1
   Compiling cfg-if v1.0.4
   Compiling memchr v2.8.3
   Compiling smallvec v1.15.2
   Compiling pin-project-lite v0.2.17
   Compiling pkg-config v0.3.33
   Compiling parking_lot_core v0.9.12
   Compiling itoa v1.0.18
   Compiling bytes v1.12.1
   Compiling scopeguard v1.2.0
   Compiling once_cell v1.21.4
   Compiling serde v1.0.229
   Compiling lock_api v0.4.14
   Compiling log v0.4.33
   Compiling futures-core v0.3.33
   Compiling crossbeam-utils v0.8.22
   Compiling stable_deref_trait v1.2.1
   Compiling tracing-core v0.1.36
   Compiling futures-sink v0.3.33
   Compiling zmij v1.0.23
   Compiling futures-channel v0.3.33
   Compiling aho-corasick v1.1.4
   Compiling dunce v1.0.5
   Compiling serde_json v1.0.151
   Compiling regex-syntax v0.8.11
   Compiling fs_extra v1.3.0
   Compiling crossbeam-epoch v0.9.20
   Compiling regex-automata v0.4.16
   Compiling bitflags v2.13.1
   Compiling typenum v1.20.1
   Compiling slab v0.4.12
   Compiling futures-io v0.3.33
   Compiling crossbeam-deque v0.8.7
   Compiling futures-task v0.3.33
   Compiling hybrid-array v0.4.13
   Compiling http v1.4.2
   Compiling rand_core v0.10.1
   Compiling getrandom v0.4.3
   Compiling syn v2.0.119
   Compiling syn v3.0.3
   Compiling serde_derive v1.0.229
   Compiling jobserver v0.1.35
   Compiling cc v1.4.0
   Compiling errno v0.3.14
   Compiling synstructure v0.13.2
   Compiling signal-hook-registry v1.4.8
   Compiling mio v1.2.2
   Compiling socket2 v0.6.5
   Compiling tokio-macros v2.7.1
   Compiling zerofrom-derive v0.1.7
   Compiling parking_lot v0.12.5
   Compiling yoke-derive v0.8.2
   Compiling tokio v1.53.1
   Compiling zerofrom v0.1.8
   Compiling tracing-attributes v0.1.31
   Compiling tracing v0.1.44
   Compiling zerovec-derive v0.11.3
   Compiling cmake v0.1.58
   Compiling displaydoc v0.2.6
   Compiling aws-lc-sys v0.43.0
   Compiling futures-macro v0.3.33
   Compiling futures-util v0.3.33
   Compiling http-body v1.1.0
   Compiling bstr v1.13.0
   Compiling thiserror v2.0.19
   Compiling litemap v0.8.2
   Compiling percent-encoding v2.3.2
   Compiling writeable v0.6.3
   Compiling aws-lc-rs v1.17.3
   Compiling same-file v1.0.6
   Compiling walkdir v2.5.0
   Compiling thiserror-impl v2.0.19
   Compiling crypto-common v0.2.2
   Compiling block-buffer v0.12.1
   Compiling zeroize v1.9.0
   Compiling utf8_iter v1.0.4
   Compiling icu_normalizer_data v2.2.0
   Compiling tower-service v0.3.3
   Compiling icu_properties_data v2.2.0
   Compiling const-oid v0.10.2
   Compiling httparse v1.10.1
   Compiling digest v0.11.3
   Compiling yoke v0.8.3
   Compiling globset v0.4.19
   Compiling fsevent-sys v4.1.0
   Compiling cpufeatures v0.3.0
   Compiling chacha20 v0.10.1
   Compiling notify-types v2.1.0
   Compiling try-lock v0.2.5
   Compiling notify v8.2.0
   Compiling want v0.3.1
   Compiling rand v0.10.2
   Compiling sha2 v0.11.0
   Compiling ignore v0.4.31
   Compiling rustls-pki-types v1.15.1
   Compiling form_urlencoded v1.2.2
   Compiling async-trait v0.1.91
   Compiling sync_wrapper v1.0.2
   Compiling rustls v0.23.42
   Compiling httpdate v1.0.3
   Compiling tower-layer v0.3.3
   Compiling untrusted v0.9.0
   Compiling atomic-waker v1.1.2
   Compiling ipnet v2.12.0
   Compiling base64 v0.22.1
   Compiling subtle v2.6.1
   Compiling rand_core v0.6.4
   Compiling siphasher v1.0.3
   Compiling core-foundation-sys v0.8.7
   Compiling rand v0.8.7
   Compiling phf_shared v0.11.3
   Compiling http-body-util v0.1.4
   Compiling security-framework-sys v2.17.0
   Compiling phf_generator v0.11.3
   Compiling core-foundation v0.10.1
   Compiling phf_macros v0.11.3
   Compiling tokio-util v0.7.19
   Compiling security-framework v3.7.0
   Compiling regex v1.13.1
   Compiling phf v0.11.3
   Compiling audit v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/hotreload/audit)
   Compiling zstd-sys v2.0.16+zstd.1.5.7
   Compiling winnow v1.0.4
   Compiling option-ext v0.2.0
   Compiling dirs-sys v0.5.0
   Compiling toml_parser v1.1.2+spec-1.1.0
   Compiling hotreload v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/hotreload)
   Compiling serde_spanned v1.1.1
   Compiling toml_datetime v1.1.1+spec-1.1.0
   Compiling toml_writer v1.1.2+spec-1.1.0
   Compiling toml v1.1.3+spec-1.1.0
   Compiling dirs v6.0.0
   Compiling zstd-safe v7.2.4
   Compiling virtue v0.0.18
   Compiling bincode_derive v2.0.1
   Compiling tower v0.5.3
   Compiling bincode v1.3.3
   Compiling crossbeam-queue v0.3.13
   Compiling heed-traits v0.20.0
   Compiling byteorder v1.5.0
   Compiling unty v0.0.4
   Compiling heed-types v0.20.1
   Compiling bincode v2.0.1
   Compiling synchronoise v1.0.1
   Compiling page_size v0.6.0
   Compiling memmap2 v0.9.11
   Compiling rayon-core v1.13.0
   Compiling either v1.17.0
   Compiling rustix v1.1.4
   Compiling hyper v1.11.0
   Compiling hyper-util v0.1.20
   Compiling autocfg v1.5.1
   Compiling num-traits v0.2.19
   Compiling futures-executor v0.3.33
   Compiling utf8parse v0.2.2
   Compiling anstyle-parse v1.0.0
   Compiling futures v0.3.33
   Compiling memory_transport_macros v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/transport/macros)
   Compiling anstyle-query v1.1.5
   Compiling typeid v1.0.3
   Compiling colorchoice v1.0.5
   Compiling anstyle v1.0.14
   Compiling is_terminal_polyfill v1.70.2
   Compiling anstream v1.0.0
   Compiling zerovec v0.11.6
   Compiling zerotrie v0.2.4
   Compiling doxygen-rs v0.4.2
   Compiling lmdb-master-sys v0.2.6
   Compiling util v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/util)
   Compiling rayon v1.12.0
   Compiling memory_transport v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/transport)
   Compiling terminal_size v0.4.4
   Compiling mlua-sys v0.12.0
   Compiling heck v0.5.0
   Compiling erased-serde v0.4.10
   Compiling clap_lex v1.1.0
   Compiling mime v0.3.17
   Compiling strsim v0.11.1
   Compiling ryu v1.0.23
   Compiling axum-core v0.5.6
   Compiling clap_builder v4.6.2
   Compiling serde_urlencoded v0.7.1
   Compiling clap_derive v4.6.4
   Compiling ordered-float v2.10.1
   Compiling tinystr v0.8.3
   Compiling potential_utf v0.1.5
   Compiling icu_collections v2.2.0
   Compiling icu_locale_core v2.2.0
   Compiling serde_path_to_error v0.1.20
   Compiling matchit v0.8.4
   Compiling serde-value v0.7.0
   Compiling axum v0.8.9
   Compiling clap v4.6.4
   Compiling icu_provider v2.2.0
   Compiling icu_properties v2.2.0
   Compiling icu_normalizer v2.2.0
   Compiling idna_adapter v1.2.2
   Compiling mlua_derive v0.12.1
   Compiling idna v1.1.0
   Compiling memory_cartridge v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/cartridge)
   Compiling url v2.5.8
   Compiling fastrand v2.5.0
   Compiling tower-http v0.6.11
   Compiling rustc-hash v2.1.3
   Compiling tempfile v3.27.0
   Compiling base v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/base)
   Compiling ingest_config v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/ingest/config)
   Compiling math v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/math)
   Compiling test_support v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/.cartridge/tests/support)
   Compiling heed v0.20.5
   Compiling mlua v0.12.1
   Compiling zstd v0.13.3
   Compiling store_core v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store/core)
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
   Compiling ingest v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/ingest)
   Compiling tick v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/tick)
   Compiling bootstrap v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/bootstrap)
   Compiling retrieval v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/retrieval)
   Compiling tick_loop v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/tick/loop)
   Compiling store v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store)
   Compiling health v0.1.0 (/Users/feb/dev/cartridge/memory.ctg/src/health)
   Compiling rpc v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/rpc)
   Compiling commands v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/commands)
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.00.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.01.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.02.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.03.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.04.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.05.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.06.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.07.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.08.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.09.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.10.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.11.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.12.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.13.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.14.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b.memory_cartridge.82273c2396491d52-cgu.15.rcgu.o unable to open object file: No such file or directory
    Finished `test` profile [unoptimized + debuginfo] target(s) in 23.01s
     Running unittests src/lib.rs (target/memory-one-writer-verify/debug/deps/memory_cartridge-4972f1dcc8b9b65b)

running 1 test
test engine_tests::a_second_local_service_is_refused_and_the_attached_one_never_asks_for_the_writer ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 20 filtered out; finished in 0.18s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/memory-runs-once-in-the-daemon-and-attached-instances-never-hit-the-writer-lock/specs/spec01.md: exit 0

Command SHA-256: 30633b06cf5b1008cbf969b7fbfd68bb18fa99f31143b73a46f0e3baabf52c23

```text

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/memory-runs-once-in-the-daemon-and-attached-instances-never-hit-the-writer-lock/specs/spec01.md: exit 0

Command SHA-256: f097a00cc402a884ae035c25a131f492506dfba08df77ba67952f46942596b3a

```text

```
