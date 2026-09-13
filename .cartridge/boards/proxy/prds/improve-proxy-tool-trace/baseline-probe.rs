#[tokio::test]
async fn baseline_tool_trace_probe() {
 let wire=Wire::Responses;
 let (service,fake)=fixture(vec![response(wire,&["cartridge__memo","client_tool"]),response(wire,&["client_tool"])],"allow");
 let value=service.request(wire,request(wire)).await.unwrap();
 let calls=fake.calls.lock().unwrap();
 assert_eq!(calls.iter().filter(|(key,args)|key=="tool.memo" && args["op"]=="call").count(),1);
 assert_eq!(calls.iter().filter(|(key,args)|key=="policy" && args["tool"]=="memo").count(),1);
 assert!(value.get("cartridge_trace").is_none());
 assert!(calls.iter().any(|(key,args)|key=="memo" && args["op"]=="observe"));
 let failure=match serde_json::from_value::<Config>(json!({"tool_trace":true})) { Ok(_)=>panic!("baseline unexpectedly supports traces"),Err(error)=>error.to_string() };
 assert!(failure.contains("unknown field `tool_trace`"));
 println!("One private dispatch and policy check completed in a mixed batch; caller tool retained; no trace identity returned. Existing memo observations are present. Opt-in configuration rejected: {failure}");
}
