use serde_json::{json,Value};
use landscape::census::{capture,Kind,Runtime,Root,Limits};
#[tokio::main(flavor="current_thread")]
async fn main(){
 let fixture=std::path::PathBuf::from(std::env::args().nth(1).unwrap());
 let declarations:Vec<Value>=serde_json::from_slice(&std::fs::read(fixture.join("declarations.json")).unwrap()).unwrap();
 let scope=fixture.join(".cartridge/boards");let root=scope.join("root");
 let census=capture(&[Root{alias:"root".into(),kind:Kind::Board,runtime:Runtime::SourceOnly,scope,directory:root.clone()}],Limits{deadline_ms:2000,..Default::default()},|_,dir|std::future::ready(declarations.iter().find(|r|r["root"].as_str()==dir.to_str()).unwrap().clone())).await;
 let entries=vec![json!({"id":"root","state":"SourceOnly","dir":root,"provide":[]})];
 let memos=vec![("@root/same".into(),json!({"kind":"prd","name":"same","description":"ROOTAMBER"}))];
 let (graph,_)=landscape::surface::compose(&entries,&[],&memos,"");
 println!("{}",json!({"census":census,"supplied_entries":entries.len(),"supplied_records":memos.len(),"root_hits":graph.search("ROOTAMBER",&Default::default()),"base_hits":graph.search("BASEBERYL",&Default::default()),"plugin_hits":graph.search("PLUGINCOBALT",&Default::default())}));
}
