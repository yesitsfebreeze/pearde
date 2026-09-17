---
commit: ea3c16ea888bef0c946842749d1e333e355440aa
spec-digests: {"spec01.md":"1e767ed8db9278a8e625933fbc28cdbcbcb3048af78b54d5ab454f5455d5b404"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/live/prds/voice-runs-headless-on-the-microphone/specs/spec01.md: exit 0

Command SHA-256: 315b09bf1857bcb2429d2b56549108fc7d2105108f29364ab7fd4584fd9d6150

```text
   Compiling libc v0.2.189
   Compiling proc-macro2 v1.0.107
   Compiling quote v1.0.47
   Compiling shlex v2.0.1
   Compiling find-msvc-tools v0.1.12
   Compiling unicode-ident v1.0.24
   Compiling cfg-if v1.0.4
   Compiling objc2 v0.6.4
   Compiling objc2-encode v4.1.0
   Compiling bitflags v2.13.2
   Compiling zeroize v1.9.0
   Compiling pkg-config v0.3.34
   Compiling serde_core v1.0.229
   Compiling cc v1.4.6
   Compiling typenum v1.20.1
   Compiling untrusted v0.9.0
   Compiling rustls-pki-types v1.15.1
   Compiling autocfg v1.5.1
   Compiling rand_core v0.10.1
   Compiling ring v0.17.14
   Compiling bytes v1.12.1
   Compiling num-traits v0.2.19
   Compiling rustls v0.23.45
   Compiling getrandom v0.4.3
   Compiling hybrid-array v0.4.15
   Compiling typeid v1.0.3
   Compiling vcpkg v0.2.15
   Compiling itoa v1.0.18
   Compiling crypto-common v0.2.2
   Compiling block-buffer v0.12.1
   Compiling pin-project-lite v0.2.17
   Compiling subtle v2.6.1
   Compiling smallvec v1.16.1
   Compiling serde v1.0.229
   Compiling thiserror v2.0.20
   Compiling once_cell v1.21.4
   Compiling const-oid v0.10.2
   Compiling parking_lot_core v0.9.12
   Compiling httparse v1.10.1
   Compiling digest v0.11.3
   Compiling dispatch2 v0.3.1
   Compiling block2 v0.6.2
   Compiling objc2-foundation v0.3.2
   Compiling syn v3.0.5
   Compiling getrandom v0.2.17
   Compiling objc2-core-foundation v0.3.2
   Compiling objc2-core-audio-types v0.3.2
   Compiling thiserror-impl v2.0.20
   Compiling tokio-macros v2.7.2
   Compiling serde_derive v1.0.229
   Compiling socket2 v0.6.5
   Compiling mio v1.2.3
   Compiling cpufeatures v0.3.1
   Compiling libsqlite3-sys v0.35.0
   Compiling objc2-core-audio v0.3.2
   Compiling chacha20 v0.10.2
   Compiling mlua-sys v0.12.0
   Compiling memchr v2.8.3
   Compiling foldhash v0.1.5
   Compiling erased-serde v0.4.10
   Compiling zmij v1.0.23
   Compiling scopeguard v1.2.0
   Compiling rand v0.10.2
   Compiling lock_api v0.4.14
   Compiling hashbrown v0.15.5
   Compiling objc2-audio-toolbox v0.3.2
   Compiling ordered-float v2.10.1
   Compiling tokio v1.53.1
   Compiling sha1 v0.11.0
   Compiling futures-macro v0.3.34
   Compiling syn v2.0.119
   Compiling http v1.5.0
   Compiling webpki-roots v1.0.9
   Compiling log v0.4.34
   Compiling serde_json v1.0.151
   Compiling slab v0.4.12
   Compiling cpal v0.18.2
   Compiling data-encoding v2.11.1
   Compiling futures-sink v0.3.34
   Compiling futures-task v0.3.34
   Compiling futures-core v0.3.34
   Compiling futures-util v0.3.34
   Compiling webpki-roots v0.26.11
   Compiling mlua_derive v0.12.1
   Compiling coreaudio-rs v0.14.2
   Compiling parking_lot v0.12.5
   Compiling hashlink v0.10.0
   Compiling bstr v1.13.1
   Compiling fallible-streaming-iterator v0.1.9
   Compiling either v1.18.0
   Compiling live v0.1.0 (/Users/feb/dev/cartridge/live.ctg)
   Compiling rustc-hash v2.1.3
   Compiling dasp_sample v0.11.0
   Compiling fallible-iterator v0.3.0
   Compiling mach2 v0.6.0
   Compiling base64 v0.22.1
   Compiling serde-value v0.7.0
   Compiling mlua v0.12.1
   Compiling rustls-webpki v0.103.15
   Compiling tungstenite v0.30.0
   Compiling tokio-rustls v0.26.5
   Compiling tokio-tungstenite v0.30.0
   Compiling rusqlite v0.37.0
    Finished `test` profile [unoptimized + debuginfo] target(s) in 4.01s
     Running unittests src/lib.rs (target/voice-headless-verify/debug/deps/live-06f13a9329221032)

running 18 tests
test audio::tests::an_unchanged_rate_copies ... ok
test audio::tests::halving_the_rate_averages_neighbours ... ok
test service::tests::a_transcript_names_each_speaker_once ... ok
test service::tests::a_spoken_line_is_capped_rather_than_read_out_whole ... ok
test audio::tests::the_speaker_holds_the_gate_while_it_has_audio ... ok
test service::tests::the_voice_session_is_told_what_the_record_says ... ok
test socket::tests::a_delta_that_is_not_base64_is_no_audio_rather_than_a_panic ... ok
test socket::tests::audio_decodes_back_to_the_samples_it_carried ... ok
test service::tests::a_conversation_opens_once_and_is_found_again ... ok
test service::tests::an_answer_with_no_voice_session_is_recorded_rather_than_refused ... ok
test service::tests::a_note_comes_back_in_the_state ... ok
test service::tests::spoken_words_are_the_prompt_of_the_delegation_that_follows_them ... ok
test audio::tests::a_voice_puts_its_devices_down_before_stopping_returns ... ok
test audio::tests::a_refused_microphone_is_the_error_the_caller_sees ... ok
test service::tests::a_device_that_will_not_open_is_a_readable_voice_error_in_the_state ... ok
test service::tests::a_key_the_fixture_does_not_know_never_opens_a_session ... ok
test socket::tests::the_environment_key_wins ... ok
test service::tests::voice_runs_a_session_on_the_wire_and_puts_both_devices_down_before_it_returns ... ok

test result: ok. 18 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.78s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/live/prds/voice-runs-headless-on-the-microphone/specs/spec01.md: exit 0

Command SHA-256: 80a40415a74cffac13d114991e4034e73a7de16ac4cfb3c6d4fe35d4895290d3

```text
audio granted; grant.exec == what src spawns == ['tmux']

```
