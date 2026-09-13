use cartridge::{lua::Host,runtime::Runtime};
use serde_json::{json,Value};
use std::{path::PathBuf,time::Duration};
fn provider(version:u64,fail:bool)->String{format!(r#"return {{inject={{"router","pty"}},provide={{"counter"}},apply=function(ctx) ctx:provide("counter",function() return {{version={version},router=ctx.router(),pty=ctx.pty()}} end) {failure} end}}"#,failure=if fail{"error('candidate rejected')"}else{""})}
fn main(){tokio::runtime::Builder::new_multi_thread().worker_threads(2).enable_all().build().unwrap().block_on(async{
 let root=PathBuf::from(std::env::args().nth(1).unwrap());let mut rows=vec![];
 for depth in 0..=1{
  let dir=root.join(format!("depth-{depth}"));std::fs::create_dir_all(&dir).unwrap();
  let write=|name:&str,text:&str|std::fs::write(dir.join(name),text).unwrap();
  write("p.lua",&provider(1,false));
  write("shared.lua",r#"return {provide={"router","pty"},apply=function(ctx) ctx:send("shared","applied");ctx:provide("router",function() return "one-router" end);ctx:provide("pty",function() return "one-pty" end) end}"#);
  write("reader.lua",r#"return {inject={"counter"},provide={"front"},apply=function(ctx) local counter=ctx.counter;ctx:provide("front",function() return counter() end) end}"#);
  write("outer.lua",r#"return {provide={"front","child"},apply=function(ctx) local p=ctx:cartridge("p.lua");local c=ctx:cartridge("reader.lua");ctx:provide("front",function() return ctx:peek("front")() end);ctx:provide("child",function() return p:uid() end) end}"#);
  // A distinct inner read key avoids the public adapter resolving itself.
  if depth==1{write("reader.lua",r#"return {inject={"counter"},provide={"inner-front"},apply=function(ctx) local counter=ctx.counter;ctx:provide("inner-front",function() return counter() end) end}"#);write("outer.lua",r#"return {provide={"front","child"},apply=function(ctx) local p=ctx:cartridge("p.lua");local c=ctx:cartridge("reader.lua");ctx:provide("front",function() return ctx:peek("inner-front")() end);ctx:provide("child",function() return p:uid() end) end}"#);}
  write("init.lua",if depth==0{r#"return {{id="s",path="shared.lua"},{id="p",path="p.lua"},{id="c",path="reader.lua"}}"#}else{r#"return {{id="s",path="shared.lua"},{id="o",path="outer.lua"}}"#});
  let host=Host::new(Runtime::new(),&dir,&dir);let mut events=host.outbox();host.reconcile().await.unwrap();
  let initial=tokio::time::timeout(Duration::from_secs(5),async{loop{if let Ok(v)=host.call("front",Value::Null).await{break v;}tokio::task::yield_now().await;}}).await.unwrap();
  let old=if depth==0{host.fiber_of("p").unwrap().uid()}else{host.call("child",Value::Null).await.unwrap().as_u64().unwrap()};
  let dependent=host.fiber_of(if depth==0{"c"}else{"o"}).unwrap().uid();let shared=host.fiber_of("s").unwrap().uid();
  write("p.lua",&provider(2,false));let returned=host.replace_node(old).await;let actual=if depth==0{host.fiber_of("p").unwrap().uid()}else{*returned.as_ref().unwrap()};
  let after=host.call("front",Value::Null).await.unwrap();
  write("p.lua",&provider(3,true));let refused=host.replace_node(actual).await;let retained=host.call("front",Value::Null).await.unwrap();
  let mut applications=0;while let Ok(e)=events.try_recv(){if e["event"]=="shared"{applications+=1;}}
  rows.push(json!({"depth":depth,"initial":initial,"old_uid":old,"returned":format!("{returned:?}"),"actual_uid":actual,"after":after,"failed_candidate_reply":format!("{refused:?}"),"retained":retained,"dependent_unchanged":host.fiber_of(if depth==0{"c"}else{"o"}).unwrap().uid()==dependent,"shared_unchanged":host.fiber_of("s").unwrap().uid()==shared,"shared_applications":applications,"counter_visible_at_root":host.call("counter",Value::Null).await.is_ok()}));
  for id in if depth==0{vec!["c","p","s"]}else{vec!["o","s"]}{host.fiber_of(id).unwrap().dispose().await;}
 }
 println!("{}",serde_json::to_string_pretty(&rows).unwrap());
});}
