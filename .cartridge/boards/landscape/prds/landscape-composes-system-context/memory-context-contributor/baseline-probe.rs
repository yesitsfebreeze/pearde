use serde_json::json;
#[test]
fn current_graph_cannot_find_memory_only_evidence() {
 let memos=vec![("@fixture/note/release.md".to_owned(),json!({"kind":"memo","description":"release checklist","name":"release","body":"not indexed"}))];
 let tools=vec![("tool.release".to_owned(),json!({"name":"release","description":"release status"}))];
 let (graph, counts)=landscape::surface::compose(&[], &tools, &memos, "");
 let hits=graph.search("release",&counts);
 assert_eq!(hits.len(),2);
 assert!(graph.search("Cedar-secret-fact",&counts).is_empty());
 assert!(graph.nodes().all(|node|node.kind!="memory"));
 println!("Existing surface finds {} memo/tool candidates; memory-only phrase has 0 hits; graph has no memory contributor or availability row",hits.len());
}
