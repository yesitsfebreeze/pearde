use super::*;
use std::collections::VecDeque;
use std::sync::Mutex;

struct Fake {
	calls: Mutex<Vec<(String, Value)>>,
	replies: Mutex<VecDeque<Value>>,
	decision: &'static str,
}

fn fixture(replies: Vec<Value>, decision: &'static str) -> (Service, Arc<Fake>) {
	let fake = Arc::new(Fake {
		calls: Mutex::new(vec![]),
		replies: Mutex::new(replies.into()),
		decision,
	});
	let f = fake.clone();
	let call: Call = Arc::new(move |key, args| {
		let f = f.clone();
		async move {
			f.calls.lock().unwrap().push((key.clone(), args.clone()));
			match (key.as_str(), args["op"].as_str()) {
				("sessions", Some("create")) => Ok(json!({"id":"proxy-session"})),
				("tool.memo", Some("describe")) => Ok(json!({"error":false,"content":json!({"name":"memo","description":"Read memos","input_schema":{"type":"object"},"cancellable":true}).to_string()})),
				("harness", Some("injection")) => Ok(json!({"system":"Live harness instructions", "tools":args["descriptors"].as_array().unwrap().iter().map(|d| json!({"type":"function","function":{"name":d["name"],"description":d["description"],"parameters":d["input_schema"]}})).collect::<Vec<_>>(),"max_bytes":200000})),
				("policy", _) => Ok(json!({"decision":f.decision})),
				("memory", Some("query")) => Ok(json!({"entities":[{"status":"active","text":"The code name is Cedar"},{"status":"superseded","text":"stale"}]})),
				("tool.memo", Some("call")) => Ok(json!({"content":"Memo result", "error":false})),
				("memo", Some("observe")) => Ok(json!({"id":"observation-id","saved":true})),
				("router", Some("request")) => f.replies.lock().unwrap().pop_front().ok_or_else(|| "unexpected model request".into()),
				_ => Err(format!("unexpected call {key} {args}")),
			}
		}.boxed()
	});
	let config = Config {
		record_usage: true,
		tools: vec!["tool.memo".into()],
		cwd: "/trusted/workspace".into(),
		..Config::default()
	};
	(Service::new(config, call), fake)
}

fn request(wire: Wire) -> Value {
	let mut body = json!({"model":"original-model","temperature":0.37,"metadata":{"caller":"kept"},"stream":true});
	match wire {
		Wire::Chat => {
			body["messages"] = json!([{"role":"system","content":"Caller instructions"},{"role":"user","content":[{"type":"text","text":"Read the memo"},{"type":"image_url","image_url":{"url":"data:image/png;base64,AA=="}}]}]);
			body["tools"] = json!([{"type":"function","function":{"name":"client_tool","parameters":{"type":"object"},"strict":true}}]);
		}
		Wire::Anthropic => {
			body["system"] = json!([{"type":"text","text":"Caller instructions","cache_control":{"type":"ephemeral"}}]);
			body["messages"] = json!([{"role":"user","content":"Read the memo"}]);
			body["tools"] = json!([{"name":"client_tool","input_schema":{"type":"object"}}]);
			body["max_tokens"] = json!(1000);
		}
		Wire::Responses => {
			body["instructions"] = json!("Caller instructions");
			body["input"] = json!("Read the memo");
			body["tools"] = json!([{"type":"function","name":"client_tool","parameters":{"type":"object"}},{"type":"web_search"}]);
			body["previous_response_id"] = json!("resp_previous");
			body["reasoning"] = json!({"effort":"high"});
		}
	}
	body
}

fn response(wire: Wire, names: &[&str]) -> Value {
	let calls: Vec<_> = names
		.iter()
		.enumerate()
		.map(|(i, n)| (format!("call-{i}"), *n))
		.collect();
	match wire {
		Wire::Chat => {
			json!({"id":"original-id","model":"selected-model","object":"chat.completion","choices":[{"index":0,"message":{"role":"assistant","content":"answer","tool_calls":calls.iter().map(|(id,name)| json!({"id":id,"type":"function","function":{"name":name,"arguments":"{\"op\":\"list\"}"}})).collect::<Vec<_>>()},"finish_reason":if calls.is_empty() {"stop"} else {"tool_calls"}}],"usage":{"prompt_tokens":20,"completion_tokens":5}})
		}
		Wire::Anthropic => {
			let mut content = vec![json!({"type":"text","text":"answer"})];
			content.extend(calls.iter().map(
				|(id, name)| json!({"type":"tool_use","id":id,"name":name,"input":{"op":"list"}}),
			));
			json!({"id":"original-id","type":"message","model":"selected-model","role":"assistant","content":content,"stop_reason":if calls.is_empty() {"end_turn"} else {"tool_use"},"stop_sequence":null,"usage":{"input_tokens":20,"output_tokens":5}})
		}
		Wire::Responses => {
			let mut output = vec![
				json!({"id":"reasoning-id","type":"reasoning","summary":[],"encrypted_content":"keep-me"}),
				json!({"id":"message-id","type":"message","role":"assistant","status":"completed","content":[{"type":"output_text","text":"answer","annotations":[]}]}),
			];
			output.extend(calls.iter().map(|(id,name)| json!({"id":format!("fc_{id}"),"type":"function_call","call_id":id,"name":name,"arguments":"{\"op\":\"list\"}","status":"completed"})));
			json!({"id":"original-id","model":"selected-model","status":"completed","output":output,"usage":{"input_tokens":20,"output_tokens":5}})
		}
	}
}

#[tokio::test]
async fn native_requests_are_injected_and_private_results_return_to_model() {
	for wire in [Wire::Chat, Wire::Anthropic, Wire::Responses] {
		let original = request(wire);
		let final_response = response(wire, &[]);
		let (service, fake) = fixture(
			vec![response(wire, &["cartridge__memo"]), final_response.clone()],
			"allow",
		);
		assert_eq!(
			service.request(wire, original.clone()).await.unwrap(),
			final_response
		);
		let seen = fake.calls.lock().unwrap();
		let outgoing: Vec<_> = seen
			.iter()
			.filter(|(k, _)| k == "router")
			.map(|(_, a)| &a["body"])
			.collect();
		assert_eq!(outgoing.len(), 2);
		for field in [
			"model",
			"temperature",
			"metadata",
			"reasoning",
			"previous_response_id",
		] {
			assert_eq!(outgoing[0][field], original[field], "{wire:?} {field}");
		}
		assert_eq!(outgoing[0]["stream"], false);
		assert_eq!(outgoing[0]["tools"][0], original["tools"][0]);
		assert!(outgoing[1].to_string().contains("Memo result"));
		for round in &outgoing {
			let text = round.to_string();
			assert_eq!(text.matches("Live harness instructions").count(), 1);
			assert!(text.contains("- The code name is Cedar"), "{wire:?} recall");
			assert!(!text.contains("stale"), "{wire:?} superseded hit");
		}
		let (_, query) = seen.iter().find(|(k, _)| k == "memory").unwrap();
		assert_eq!(query["text"], "Read the memo");
		let (_, executed) = seen
			.iter()
			.find(|(k, a)| k == "tool.memo" && a["op"] == "call")
			.unwrap();
		assert_eq!(executed["context"]["cwd"], "/trusted/workspace");
		assert_eq!(executed["input"], json!({"op":"list"}));
		if wire == Wire::Responses {
			assert!(outgoing[1].to_string().contains("keep-me"));
		}
	}
}

#[tokio::test]
async fn caller_tools_are_returned_and_mixed_batches_are_deferred_without_execution() {
	for wire in [Wire::Chat, Wire::Anthropic, Wire::Responses] {
		let final_response = response(wire, &["client_tool"]);
		let (service, fake) = fixture(
			vec![
				response(wire, &["cartridge__memo", "client_tool"]),
				final_response.clone(),
			],
			"allow",
		);
		assert_eq!(
			service.request(wire, request(wire)).await.unwrap(),
			final_response
		);
		let seen = fake.calls.lock().unwrap();
		let calls: Vec<_> = seen.iter().filter(|(_, a)| a["op"] == "call").collect();
		assert_eq!(calls.len(), 1);
		assert_eq!(calls[0].0, "tool.memo");
		let second = &seen.iter().filter(|(k, _)| k == "router").nth(1).unwrap().1["body"];
		assert!(
			!second.to_string().contains("call-1"),
			"deferred call left unresolved"
		);
	}
}

#[tokio::test]
async fn policy_denials_and_approval_requirements_never_execute() {
	for decision in ["deny", "ask"] {
		let (service, fake) = fixture(
			vec![
				response(Wire::Chat, &["cartridge__memo"]),
				response(Wire::Chat, &[]),
			],
			decision,
		);
		service
			.request(Wire::Chat, request(Wire::Chat))
			.await
			.unwrap();
		let seen = fake.calls.lock().unwrap();
		assert!(!seen.iter().any(|(_, a)| a["op"] == "call"));
		assert!(seen
			.iter()
			.filter(|(k, _)| k == "router")
			.nth(1)
			.unwrap()
			.1
			.to_string()
			.contains("error\\\":true"));
	}
}

#[tokio::test]
async fn an_ask_denial_names_the_operation_and_the_missing_channel() {
	let (service, fake) = fixture(
		vec![
			response(Wire::Chat, &["cartridge__memo"]),
			response(Wire::Chat, &[]),
		],
		"ask",
	);
	service
		.request(Wire::Chat, request(Wire::Chat))
		.await
		.unwrap();
	let seen = fake.calls.lock().unwrap();
	assert!(!seen.iter().any(|(_, a)| a["op"] == "call"));
	assert!(!seen
		.iter()
		.any(|(k, a)| k == "memo" && a["op"] == "observe"));
	let refusal = seen.iter().filter(|(k, _)| k == "router").nth(1).unwrap().1["body"].to_string();
	assert!(
		refusal.contains("approval required for memo list"),
		"{refusal}"
	);
	assert!(
		refusal.contains("this proxy has no interactive approval channel"),
		"{refusal}"
	);
}

#[tokio::test]
async fn granted_dispatches_land_in_the_observation_journal_with_caller_and_turn() {
	let (service, fake) = fixture(
		vec![
			response(Wire::Chat, &["cartridge__memo"]),
			response(Wire::Chat, &[]),
		],
		"allow",
	);
	service
		.request(Wire::Chat, request(Wire::Chat))
		.await
		.unwrap();
	let seen = fake.calls.lock().unwrap();
	let observations: Vec<_> = seen
		.iter()
		.filter(|(k, a)| k == "memo" && a["op"] == "observe")
		.collect();
	assert_eq!(observations.len(), 2, "{:?}", seen);
	let (used, outcome) = (&observations[0].1, &observations[1].1);
	assert_eq!(used["event"]["stage"], "used");
	assert_eq!(used["event"]["path"], "tool.memo");
	assert_eq!(used["event"]["usage"], "memo");
	assert_eq!(used["event"]["revision"].as_str().unwrap().len(), 64);
	assert_eq!(
		used["context"],
		json!({"session":"proxy-session","run":"proxy-0","call":"1"})
	);
	assert_eq!(used["cwd"], "/trusted/workspace");
	assert_eq!(outcome["event"]["stage"], "outcome");
	assert_eq!(outcome["event"]["outcome"], "success");
	assert_eq!(outcome["event"]["parent"], "observation-id");
	assert_eq!(
		outcome["context"],
		json!({"session":"proxy-session","run":"proxy-0","call":"1:outcome"})
	);
}

#[tokio::test]
async fn collision_budget_and_malformed_calls_fail_before_side_effects() {
	let (mut service, fake) = fixture(vec![], "allow");
	let mut body = request(Wire::Chat);
	body["tools"][0]["function"]["name"] = json!("cartridge__memo");
	assert!(service
		.request(Wire::Chat, body)
		.await
		.unwrap_err()
		.contains("collides"));
	assert!(!fake
		.calls
		.lock()
		.unwrap()
		.iter()
		.any(|(k, _)| k == "router"));
	service.config.max_bytes = 1;
	assert!(service
		.request(Wire::Chat, request(Wire::Chat))
		.await
		.unwrap_err()
		.contains("budget"));
	let mut malformed = response(Wire::Chat, &["cartridge__memo"]);
	malformed["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"] = json!("invalid");
	let (service, fake) = fixture(vec![malformed], "allow");
	assert!(service
		.request(Wire::Chat, request(Wire::Chat))
		.await
		.is_err());
	assert!(!fake
		.calls
		.lock()
		.unwrap()
		.iter()
		.any(|(_, a)| a["op"] == "call"));
}

#[test]
fn final_sse_preserves_ids_stop_reasons_and_native_response_items() {
	for wire in [Wire::Chat, Wire::Anthropic, Wire::Responses] {
		let response = response(wire, &["client_tool"]);
		let frames = wire::sse(&response, wire).unwrap();
		let events = router::protocol::Decoder::default()
			.push(frames.as_bytes())
			.unwrap();
		assert!(frames.contains("original-id"));
		assert!(frames.contains("client_tool"));
		assert!(!frames.contains("cartridge__memo"));
		assert!(!frames.contains("cartridge_usage"));
		if wire == Wire::Responses {
			assert_eq!(events.last().unwrap()["response"], response);
			assert!(frames.contains("keep-me"));
		}
	}
}

#[tokio::test]
async fn http_accepts_original_json_and_authenticates_before_dispatch() {
	for wire in [Wire::Chat, Wire::Anthropic, Wire::Responses] {
		for streaming in [false, true] {
			let final_response = response(wire, &[]);
			let (mut service, fake) = fixture(
				vec![response(wire, &["cartridge__memo"]), final_response.clone()],
				"allow",
			);
			let upstream = if streaming {
				Some(attach_stream_router(&mut service, wire, None, false).await)
			} else {
				None
			};
			let app = axum::Router::new()
				.fallback(forward)
				.with_state(Arc::new(Http {
					service: Arc::new(service),
					key: "test-only-key".into(),
				}));
			let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
			let url = format!(
				"http://{}/v1{}",
				listener.local_addr().unwrap(),
				wire.path()
			);
			let task = tokio::spawn(async move {
				axum::serve(listener, app).await.unwrap();
			});
			let client = reqwest::Client::new();
			let unauthorized = client.post(&url).json(&request(wire)).send().await.unwrap();
			assert_eq!(unauthorized.status(), 401);
			assert!(fake.calls.lock().unwrap().is_empty());
			let looped = client
				.post(&url)
				.bearer_auth("test-only-key")
				.header("x-cartridge-model-hop", "1")
				.json(&request(wire))
				.send()
				.await
				.unwrap();
			assert_eq!(looped.status(), 508);
			assert!(fake.calls.lock().unwrap().is_empty());
			let mut body = request(wire);
			body["stream"] = json!(streaming);
			let request = client.post(&url).json(&body);
			let request = if wire == Wire::Anthropic {
				request.header("x-api-key", "test-only-key")
			} else {
				request.bearer_auth("test-only-key")
			};
			let result = request.send().await.unwrap();
			assert_eq!(result.status(), 200);
			assert!(!result.headers().contains_key("x-cartridge-usage-id"));
			if streaming {
				assert_eq!(result.headers()["content-type"], "text/event-stream");
				let frames = result.text().await.unwrap();
				assert!(frames.contains("answer"));
				assert!(!frames.contains("cartridge__memo"));
			} else {
				assert_eq!(result.json::<Value>().await.unwrap(), final_response);
			}
			task.abort();
			let _ = task.await;
			if let Some(task) = upstream {
				task.abort();
				let _ = task.await;
			}
		}
	}
}

async fn attach_stream_router(
	service: &mut Service,
	wire: Wire,
	gate: Option<Arc<tokio::sync::Semaphore>>,
	truncate: bool,
) -> tokio::task::JoinHandle<()> {
	attach_stream_router_options(service, wire, gate, truncate, false).await
}

async fn attach_stream_router_options(
	service: &mut Service,
	wire: Wire,
	gate: Option<Arc<tokio::sync::Semaphore>>,
	truncate: bool,
	repeat_usage: bool,
) -> tokio::task::JoinHandle<()> {
	let call = service.call.clone();
	let requests = Arc::new(std::sync::atomic::AtomicUsize::new(0));
	let app = axum::Router::new().fallback(move |axum::Json(body): axum::Json<Value>| {
		let (call, gate, requests) = (call.clone(), gate.clone(), requests.clone());
		async move {
			assert_eq!(body["stream"], true);
			let number = requests.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
			let value = call("router".into(), json!({"op":"request","body":body}))
				.await
				.unwrap();
			let frames = wire::sse(&value, wire).unwrap();
            let snapshot = match wire {
                Wire::Chat => json!({"choices":[],"usage":value["usage"]}),
                Wire::Anthropic => json!({"type":"message_delta","delta":{"stop_reason":null,"stop_sequence":null},"usage":value["usage"]}),
                Wire::Responses => json!({"type":"response.in_progress","response":{"usage":value["usage"]}}),
            };
            let snapshot = router::protocol::sse(&snapshot,wire);
			let (tx, rx) =
				tokio::sync::mpsc::channel::<Result<axum::body::Bytes, std::io::Error>>(16);
			tokio::spawn(async move {
				for (frame_index,frame) in frames.split_inclusive("\n\n").enumerate() {
					let is_text = match wire {
						Wire::Chat => frame.contains("\"content\":\"answer\""),
						Wire::Anthropic => frame.contains("text_delta"),
						Wire::Responses => frame.contains("response.output_text.delta"),
					};
					for bytes in frame.as_bytes().chunks(7) {
						if tx
							.send(Ok(axum::body::Bytes::copy_from_slice(bytes)))
							.await
							.is_err()
						{
							return;
						}
					}
                    if repeat_usage && frame_index == 0 {
                        for _ in 0..2 {
                            for bytes in snapshot.as_bytes().chunks(7) {
                                if tx.send(Ok(axum::body::Bytes::copy_from_slice(bytes))).await.is_err() { return; }
                            }
                        }
                    }
					if is_text && number == 0 {
						if let Some(gate) = &gate {
							let _permit = gate.acquire().await.unwrap();
						}
						if truncate {
							return;
						}
					}
				}
			});
			let stream = futures::stream::unfold(rx, |mut rx| async {
				rx.recv().await.map(|frame| (frame, rx))
			});
			(
				[("content-type", "text/event-stream")],
				axum::body::Body::from_stream(stream),
			)
				.into_response()
		}
	});
	let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
	let base_url = format!("http://{}", listener.local_addr().unwrap());
	let base = service.call.clone();
	service.call = Arc::new(move |key, args| {
		let (base, base_url) = (base.clone(), base_url.clone());
		async move {
			if key == "router" && args["op"] == "session" {
				return Ok(json!({"key":"test-lease","base":base_url}));
			}
			if key == "router" && args["op"] == "release" {
				return Ok(json!(true));
			}
			base(key, args).await
		}
		.boxed()
	});
	tokio::spawn(async move {
		axum::serve(listener, app).await.unwrap();
	})
}

#[tokio::test]
async fn text_arrives_before_round_completion_and_private_tools_stay_hidden() {
	use axum::body::HttpBody;
	use futures::StreamExt;
	for wire in [Wire::Chat, Wire::Anthropic, Wire::Responses] {
		let (mut service, fake) = fixture(
			vec![
				response(wire, &["cartridge__memo", "client_tool"]),
				response(wire, &["client_tool"]),
			],
			"allow",
		);
		let gate = Arc::new(tokio::sync::Semaphore::new(0));
		let upstream = attach_stream_router(&mut service, wire, Some(gate.clone()), false).await;
		let service = Arc::new(service);
		let reply = streaming::response(service.clone(), wire, request(wire));
		assert!(!reply.body().is_end_stream());
		let mut chunks = reply.into_body().into_data_stream();
		let mut frames = String::new();
		tokio::time::timeout(std::time::Duration::from_secs(3), async {
			while !frames.contains("answer") {
				frames
					.push_str(std::str::from_utf8(&chunks.next().await.unwrap().unwrap()).unwrap());
			}
		})
		.await
		.expect("text must arrive while upstream completion is blocked");
		assert!(!fake
			.calls
			.lock()
			.unwrap()
			.iter()
			.any(|(_, a)| a["op"] == "call"));
		gate.add_permits(1);
		while let Some(chunk) = chunks.next().await {
			frames.push_str(std::str::from_utf8(&chunk.unwrap()).unwrap());
		}
		assert!(!frames.contains("cartridge__memo"));
		assert!(frames.contains("client_tool"));
		let events = router::protocol::Decoder::default()
			.push(frames.as_bytes())
			.unwrap();
		let done = events
			.iter()
			.filter(|e| {
				e["_done"] == true
					|| matches!(
						e["type"].as_str(),
						Some("message_stop" | "response.completed")
					)
			})
			.count();
		assert_eq!(done, 1, "{frames}");
		assert_eq!(
			fake.calls
				.lock()
				.unwrap()
				.iter()
				.filter(|(_, a)| a["op"] == "call")
				.count(),
			1
		);
		if wire == Wire::Responses {
			let final_response = &events.last().unwrap()["response"];
			assert_eq!(final_response["id"], events[0]["response"]["id"]);
			assert_eq!(
				final_response["output"][0]["content"][0]["text"],
				"answeranswer"
			);
			for (i, event) in events.iter().enumerate() {
				assert_eq!(event["sequence_number"], i);
			}
			fake.replies.lock().unwrap().push_back(response(wire, &[]));
			let mut next = request(wire);
			next["previous_response_id"] = final_response["id"].clone();
			service.request(wire, next).await.unwrap();
			assert_eq!(
				fake.calls
					.lock()
					.unwrap()
					.iter()
					.rfind(|(k, _)| k == "router")
					.unwrap()
					.1["body"]["previous_response_id"],
				"original-id"
			);
		}
		upstream.abort();
		let _ = upstream.await;
	}
}

#[tokio::test]
async fn interrupted_stream_reports_error_without_success_replay_or_tools() {
	use futures::StreamExt;
	for wire in [Wire::Chat, Wire::Anthropic, Wire::Responses] {
		let (mut service, fake) = fixture(vec![response(wire, &["cartridge__memo"])], "allow");
		let upstream = attach_stream_router(&mut service, wire, None, true).await;
		let mut chunks = streaming::response(Arc::new(service), wire, request(wire))
			.into_body()
			.into_data_stream();
		let mut frames = String::new();
		while let Some(chunk) = chunks.next().await {
			frames.push_str(std::str::from_utf8(&chunk.unwrap()).unwrap());
		}
		assert!(frames.contains("answer"));
		assert!(frames.contains("proxy_error"));
		assert!(
			!frames.contains("[DONE]")
				&& !frames.contains("response.completed")
				&& !frames.contains("message_stop")
		);
		let calls = fake.calls.lock().unwrap();
		assert_eq!(calls.iter().filter(|(k, _)| k == "router").count(), 1);
		assert!(!calls.iter().any(|(_, a)| a["op"] == "call"));
		upstream.abort();
	}
}

#[tokio::test]
async fn deadline_and_dropped_request_cancel_the_exact_active_tool() {
	for deadline in [true, false] {
		let (mut service, _) = fixture(vec![response(Wire::Chat, &["cartridge__memo"])], "allow");
		service.config.timeout_secs = 1;
		service.config.usage_accounting = true;
		let base = service.call.clone();
		let started = Arc::new(tokio::sync::Notify::new());
		let (tx, mut rx) = tokio::sync::mpsc::unbounded_channel();
		let active = Arc::new(Mutex::new(Value::Null));
		let (signal, saved) = (started.clone(), active.clone());
		service.call = Arc::new(move |key, args| {
			let (base, signal, saved, tx) =
				(base.clone(), signal.clone(), saved.clone(), tx.clone());
			async move {
				if key == "tool.memo" && args["op"] == "call" {
					*saved.lock().unwrap() = args["context"].clone();
					signal.notify_one();
					return std::future::pending().await;
				}
				if key == "tool.memo" && args["op"] == "cancel" {
					tx.send(args["context"].clone()).unwrap();
					return Ok(json!({"content":"cancelled","error":false}));
				}
				base(key, args).await
			}
			.boxed()
		});
		let task = tokio::spawn(async move {
			service
				.request_with_stream(Wire::Chat, request(Wire::Chat), None)
				.await
		});
		started.notified().await;
		if deadline {
			let failure = task.await.unwrap().unwrap_err();
			assert!(failure.message.contains("deadline"));
			let report = failure.usage.unwrap();
			assert_eq!(report["status"], "failed");
			assert_eq!(report["complete"], false);
			assert_eq!(report["totals"]["total_tokens"], 25);
			assert_eq!(report["rounds_completed"], 1);
		} else {
			task.abort();
			assert!(task.await.unwrap_err().is_cancelled());
		}
		let context = tokio::time::timeout(std::time::Duration::from_secs(2), rx.recv())
			.await
			.unwrap()
			.unwrap();
		assert_eq!(context, *active.lock().unwrap());
	}
}

#[tokio::test]
async fn exhausted_step_budget_prevents_unreportable_tool_side_effects() {
	let (mut service, fake) = fixture(vec![response(Wire::Chat, &["cartridge__memo"])], "allow");
	service.config.max_steps = 1;
	assert!(service
		.request(Wire::Chat, request(Wire::Chat))
		.await
		.unwrap_err()
		.contains("step budget"));
	assert!(!fake
		.calls
		.lock()
		.unwrap()
		.iter()
		.any(|(_, a)| a["op"] == "call"));
}

#[tokio::test]
async fn dropping_stream_body_cancels_active_tool_and_releases_router_lease() {
	use futures::StreamExt;
	let (mut service, _) = fixture(vec![response(Wire::Chat, &["cartridge__memo"])], "allow");
	service.config.usage_accounting = true;
	let upstream = attach_stream_router(&mut service, Wire::Chat, None, false).await;
	let base = service.call.clone();
	let started = Arc::new(tokio::sync::Notify::new());
	let (cancel_tx, mut cancel_rx) = tokio::sync::mpsc::unbounded_channel();
	let (release_tx, mut release_rx) = tokio::sync::mpsc::unbounded_channel();
	let saved = Arc::new(Mutex::new(Value::Null));
	let (signal, context) = (started.clone(), saved.clone());
	service.call = Arc::new(move |key, args| {
		let (base, signal, context, cancel_tx, release_tx) = (
			base.clone(),
			signal.clone(),
			context.clone(),
			cancel_tx.clone(),
			release_tx.clone(),
		);
		async move {
			if key == "tool.memo" && args["op"] == "call" {
				*context.lock().unwrap() = args["context"].clone();
				signal.notify_one();
				return std::future::pending().await;
			}
			if key == "tool.memo" && args["op"] == "cancel" {
				cancel_tx.send(args["context"].clone()).unwrap();
				return Ok(json!({"content":"cancelled","error":false}));
			}
			if key == "router" && args["op"] == "release" {
				release_tx.send(args["key"].clone()).unwrap();
			}
			base(key, args).await
		}
		.boxed()
	});
	let service = Arc::new(service);
	let response = streaming::response(service.clone(), Wire::Chat, request(Wire::Chat));
	let report_id = response.headers()["x-cartridge-usage-id"]
		.to_str()
		.unwrap()
		.to_owned();
	let mut chunks = response.into_body().into_data_stream();
	assert!(!chunks.next().await.unwrap().unwrap().is_empty());
	tokio::time::timeout(std::time::Duration::from_secs(3), started.notified())
		.await
		.unwrap();
	drop(chunks);
	let cancelled = tokio::time::timeout(std::time::Duration::from_secs(3), cancel_rx.recv())
		.await
		.unwrap()
		.unwrap();
	assert_eq!(cancelled, *saved.lock().unwrap());
	assert_eq!(
		tokio::time::timeout(std::time::Duration::from_secs(3), release_rx.recv())
			.await
			.unwrap()
			.unwrap(),
		"test-lease"
	);
	let report = service.usage_report(&report_id).unwrap();
	assert_eq!(report["status"], "cancelled");
	assert_eq!(report["complete"], false);
	assert_eq!(
		report["totals"],
		json!({"input_tokens":20,"output_tokens":5,"total_tokens":25})
	);
	assert_eq!(report["rounds_completed"], 1);
	upstream.abort();
	let _ = upstream.await;
}

fn counted_response(wire: Wire, names: &[&str], input: u64, output: u64) -> Value {
	let mut value = response(wire, names);
	let (i, o) = if wire == Wire::Chat {
		("prompt_tokens", "completion_tokens")
	} else {
		("input_tokens", "output_tokens")
	};
	value["usage"] = json!({i:input,o:output});
	value
}

async fn stream_reports(service: Arc<Service>, wire: Wire) -> (String, Vec<Value>) {
	use futures::StreamExt;
	let response = streaming::response(service, wire, request(wire));
	let id = response.headers()["x-cartridge-usage-id"]
		.to_str()
		.unwrap()
		.to_owned();
	let mut chunks = response.into_body().into_data_stream();
	let mut bytes = Vec::new();
	tokio::time::timeout(std::time::Duration::from_secs(5), async {
		while let Some(chunk) = chunks.next().await {
			bytes.extend_from_slice(&chunk.unwrap());
		}
	})
	.await
	.expect("stream accounting deadline");
	(
		id,
		router::protocol::Decoder::default().push(&bytes).unwrap(),
	)
}
fn extract_reports(events: &[Value]) -> Vec<Value> {
	events
		.iter()
		.filter_map(|event| {
			event
				.get("cartridge_usage")
				.or_else(|| event["response"].get("cartridge_usage"))
		})
		.cloned()
		.collect()
}

#[tokio::test]
async fn three_round_json_and_sse_accounting_match_without_duplicate_final_events() {
	for wire in [Wire::Chat, Wire::Anthropic, Wire::Responses] {
		let replies = vec![
			counted_response(wire, &["cartridge__memo"], 10, 1),
			counted_response(wire, &["cartridge__memo"], 20, 2),
			counted_response(wire, &[], 30, 3),
		];
		let (mut plain, _) = fixture(replies.clone(), "allow");
		plain.config.usage_accounting = true;
		let result = plain.request(wire, request(wire)).await.unwrap();
		let expected = result["cartridge_usage"].clone();
		assert_eq!(expected["complete"], true);
		assert_eq!(
			expected["totals"],
			json!({"input_tokens":60,"output_tokens":6,"total_tokens":66})
		);
		assert_eq!(
			expected["final_round"],
			json!({"index":3,"input_tokens":30,"output_tokens":3,"completed":true})
		);
		assert_eq!(expected["rounds_completed"], 3);
		assert_eq!(
			result["usage"], replies[2]["usage"],
			"legacy JSON usage stays final-round"
		);
		assert_eq!(
			plain
				.usage_report(expected["id"].as_str().unwrap())
				.unwrap(),
			expected
		);
		let (mut streamed, fake) = fixture(replies, "allow");
		streamed.config.usage_accounting = true;
		let upstream = attach_stream_router_options(&mut streamed, wire, None, false, true).await;
		let streamed = Arc::new(streamed);
		let (id, events) = stream_reports(streamed.clone(), wire).await;
		let reports = extract_reports(&events);
		assert_eq!(reports.len(), 1, "{events:?}");
		let mut actual = reports[0].clone();
		assert_eq!(actual["id"], id);
		assert_eq!(streamed.usage_report(&id).unwrap(), actual);
		actual["id"] = expected["id"].clone();
		assert_eq!(actual, expected);
		assert_eq!(
			events
				.iter()
				.filter(|e| e["_done"] == true
					|| e["type"] == "message_stop"
					|| e["type"] == "response.completed")
				.count(),
			1
		);
		assert_eq!(
			fake.calls
				.lock()
				.unwrap()
				.iter()
				.filter(|(_, a)| a["op"] == "call")
				.count(),
			2
		);
		upstream.abort();
		let _ = upstream.await;
	}
}

#[tokio::test]
async fn incomplete_streams_retain_observed_usage_and_never_claim_success() {
	for wire in [Wire::Chat, Wire::Anthropic, Wire::Responses] {
		let (mut service, fake) = fixture(
			vec![counted_response(wire, &["cartridge__memo"], 40, 7)],
			"allow",
		);
		service.config.usage_accounting = true;
		let upstream = attach_stream_router_options(&mut service, wire, None, true, true).await;
		let service = Arc::new(service);
		let (id, events) = stream_reports(service.clone(), wire).await;
		let reports = extract_reports(&events);
		assert_eq!(reports.len(), 1);
		assert_eq!(
			reports[0]["totals"],
			json!({"input_tokens":40,"output_tokens":7,"total_tokens":47})
		);
		assert_eq!(reports[0]["complete"], false);
		assert_eq!(reports[0]["rounds_completed"], 0);
		assert_eq!(reports[0]["status"], "failed");
		assert_eq!(service.usage_report(&id).unwrap(), reports[0]);
		assert!(!events.iter().any(|e| e["_done"] == true
			|| e["type"] == "message_stop"
			|| e["type"] == "response.completed"));
		assert!(!fake
			.calls
			.lock()
			.unwrap()
			.iter()
			.any(|(_, a)| a["op"] == "call"));
		upstream.abort();
		let _ = upstream.await;
	}
}

#[tokio::test]
async fn missing_invalid_zero_usage_and_json_errors_are_distinct() {
	for wire in [Wire::Chat, Wire::Anthropic, Wire::Responses] {
		for missing in [
			Value::Null,
			json!({"prompt_tokens":-1,"completion_tokens":"bad","input_tokens":-1,"output_tokens":"bad"}),
		] {
			let mut middle = response(wire, &["cartridge__memo"]);
			middle["usage"] = missing;
			let (mut service, _) = fixture(
				vec![
					counted_response(wire, &["cartridge__memo"], 10, 1),
					middle,
					counted_response(wire, &[], 30, 3),
				],
				"allow",
			);
			service.config.usage_accounting = true;
			let report =
				service.request(wire, request(wire)).await.unwrap()["cartridge_usage"].clone();
			assert_eq!(report["complete"], false);
			assert_eq!(
				report["totals"],
				json!({"input_tokens":40,"output_tokens":4,"total_tokens":44})
			);
			assert_eq!(report["input_reported_rounds"], 2);
		}
		let (mut service, _) = fixture(vec![counted_response(wire, &[], 0, 0)], "allow");
		service.config.usage_accounting = true;
		let value = service.request(wire, request(wire)).await.unwrap();
		assert_eq!(value["cartridge_usage"]["complete"], true);
		assert_eq!(value["cartridge_usage"]["totals"]["total_tokens"], 0);
		let (mut service, _) = fixture(
			vec![counted_response(wire, &["cartridge__memo"], 10, 1)],
			"allow",
		);
		service.config.usage_accounting = true;
		let failure = service
			.request_with_stream(wire, request(wire), None)
			.await
			.unwrap_err();
		let report = failure.usage.unwrap();
		assert_eq!(report["complete"], false);
		assert_eq!(
			report["totals"],
			json!({"input_tokens":10,"output_tokens":1,"total_tokens":11})
		);
		assert_eq!(report["rounds_started"], 2);
		assert_eq!(report["final_round"]["input_tokens"], Value::Null);
	}
}

#[test]
fn accounting_is_bounded_and_overflow_cannot_be_a_success() {
	let archive = Arc::new(usage::Archive::default());
	for n in 0..130 {
		let shared = usage::shared(format!("fixture-{n}"));
		let mut guard = usage::Guard::new(Some(shared.clone()), archive.clone());
		usage::lock(&shared).begin();
		usage::lock(&shared).observe(
			Wire::Chat,
			&json!({"prompt_tokens":1,"completion_tokens":0}),
		);
		usage::lock(&shared).complete_round();
		guard.finish("completed");
	}
	assert!(archive.get("fixture-0").is_err());
	assert!(archive.get("fixture-1").is_err());
	assert!(archive.get("fixture-2").is_ok());
	assert!(archive.get("unknown").is_err());
	let shared = usage::shared("overflow".into());
	let mut guard = usage::Guard::new(Some(shared.clone()), archive.clone());
	for input in [u64::MAX, 1] {
		usage::lock(&shared).begin();
		usage::lock(&shared).observe(
			Wire::Chat,
			&json!({"prompt_tokens":input,"completion_tokens":0}),
		);
		usage::lock(&shared).complete_round();
	}
	let result = guard.finish("completed").unwrap();
	assert_eq!(result["complete"], false);
	assert_eq!(result["totals"]["input_tokens"], Value::Null);
	assert!(result["incomplete_reasons"]
		.as_array()
		.unwrap()
		.contains(&json!("counter_overflow")));
}

#[tokio::test]
async fn enabled_http_reports_success_and_error_with_lookup_id() {
	for wire in [Wire::Chat, Wire::Anthropic, Wire::Responses] {
		for fail in [false, true] {
			let replies = if fail {
				vec![]
			} else {
				vec![counted_response(wire, &[], 8, 2)]
			};
			let (mut service, _) = fixture(replies, "allow");
			assert!(service
				.usage_report("anything")
				.unwrap_err()
				.contains("disabled"));
			service.config.usage_accounting = true;
			let service = Arc::new(service);
			let app = axum::Router::new()
				.fallback(forward)
				.with_state(Arc::new(Http {
					service: service.clone(),
					key: "fixture-key".into(),
				}));
			let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
			let url = format!(
				"http://{}/v1{}",
				listener.local_addr().unwrap(),
				wire.path()
			);
			let server = tokio::spawn(async move { axum::serve(listener, app).await.unwrap() });
			let mut request_body = request(wire);
			request_body["stream"] = json!(false);
			let response = reqwest::Client::new()
				.post(url)
				.bearer_auth("fixture-key")
				.json(&request_body)
				.send()
				.await
				.unwrap();
			assert_eq!(response.status().as_u16(), if fail { 502 } else { 200 });
			let id = response.headers()["x-cartridge-usage-id"]
				.to_str()
				.unwrap()
				.to_owned();
			let body: Value = response.json().await.unwrap();
			let report = &body["cartridge_usage"];
			assert_eq!(report["id"], id);
			assert_eq!(service.usage_report(&id).unwrap(), *report);
			assert_eq!(report["complete"], !fail);
			assert_eq!(report["totals"]["total_tokens"], if fail { 0 } else { 10 });
			assert_eq!(report["rounds_started"], 1);
			assert_eq!(report["input_reported_rounds"], if fail { 0 } else { 1 });
			if fail {
				assert!(body["error"]["message"].is_string());
			}
			server.abort();
			let _ = server.await;
		}
	}
}

#[test]
fn malformed_and_decreasing_snapshots_keep_known_counts_but_flag_uncertainty() {
	let ledger = usage::shared("counter-anomaly".into());
	let archive = Arc::new(usage::Archive::default());
	let mut guard = usage::Guard::new(Some(ledger.clone()), archive);
	{
		let mut ledger = usage::lock(&ledger);
		ledger.begin();
		ledger.observe(
			Wire::Chat,
			&json!({"prompt_tokens":10,"completion_tokens":4}),
		);
		ledger.observe(
			Wire::Chat,
			&json!({"prompt_tokens":-2,"completion_tokens":1.5}),
		);
		ledger.observe(
			Wire::Chat,
			&json!({"prompt_tokens":9,"completion_tokens":3}),
		);
		ledger.observe(
			Wire::Chat,
			&json!({"prompt_tokens":10,"completion_tokens":4}),
		);
		ledger.complete_round();
		ledger.complete_round();
	}
	let report = guard.finish("completed").unwrap();
	assert_eq!(report["totals"]["total_tokens"], 14);
	assert_eq!(report["rounds_completed"], 1);
	assert_eq!(report["complete"], false);
	assert_eq!(
		report["incomplete_reasons"],
		json!(["decreasing_usage_snapshot", "invalid_counter"])
	);
}

#[tokio::test]
async fn immediately_dropped_stream_has_an_archived_report_without_dispatch() {
	let (mut service, fake) = fixture(vec![], "allow");
	service.config.usage_accounting = true;
	let service = Arc::new(service);
	let response = streaming::response(service.clone(), Wire::Chat, request(Wire::Chat));
	let id = response.headers()["x-cartridge-usage-id"]
		.to_str()
		.unwrap()
		.to_owned();
	drop(response);
	tokio::task::yield_now().await;
	let report = service.usage_report(&id).unwrap();
	assert_eq!(report["status"], "cancelled");
	assert_eq!(report["rounds_started"], 0);
	assert_eq!(report["complete"], false);
	assert!(fake.calls.lock().unwrap().is_empty());
}

#[tokio::test]
async fn baseline_continuation_lifetime_probe() {
 let (service,fake)=fixture(vec![response(Wire::Responses,&[])],"allow");
 service.remember("proxy_probe".into(),"provider_a_response".into());
 let mut body=request(Wire::Responses);body["previous_response_id"]=json!("proxy_probe");
 body["model"]=json!("other-provider");body["metadata"]=json!({"client":"other-client"});
 service.request(Wire::Responses,body.clone()).await.unwrap();
 assert_eq!(fake.calls.lock().unwrap().iter().rfind(|(key,_)|key=="router").unwrap().1["body"]["previous_response_id"],"provider_a_response");
 for i in 0..1024 {service.remember(format!("proxy_{i}"),format!("upstream_{i}"));}
 let evicted=service.request(Wire::Responses,body.clone()).await.unwrap_err();
 let (restarted,_)=fixture(vec![],"allow");
 let restarted=restarted.request(Wire::Responses,body).await.unwrap_err();
 println!("wrong-provider mapping accepted; evicted={evicted:?}; restarted={restarted:?}");
 assert_eq!(evicted,restarted);
}
