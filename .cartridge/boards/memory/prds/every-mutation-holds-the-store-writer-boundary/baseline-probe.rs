
#[test]
fn baseline_with_graph_refuses_an_existing_writer_before_loading_or_mutating() {
	let dir = tempfile::tempdir().unwrap();
	let cfg = config::Config { data_dir:dir.path().to_string_lossy().into_owned(), ..Default::default() };
	let _owner = store::lock::acquire(&cfg.data_dir, "fixture owner").unwrap();
	let mut called = false;
	crate::with_graph(&cfg, |_| { called = true; });
	assert!(!called, "with_graph entered mutation while another writer held this store");
}
