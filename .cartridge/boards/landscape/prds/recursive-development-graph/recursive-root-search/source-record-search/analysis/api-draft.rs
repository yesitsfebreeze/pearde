// Design artifact only; implementation source remains held until PRD collection.
// Keep these types in source_search.rs; do not widen census or Memo owner parsing.
use landscape::census::{Census, Kind, Runtime};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::{future::Future, path::PathBuf};
use tokio::time::Instant;

#[derive(Clone, Debug, Serialize)]
#[serde(tag = "action", rename_all = "snake_case")]
pub enum OwnerRequest {
    Index { expected_source_revision: String },
    Read { expected_source_revision: String, path: String, expected_revision: String },
}

#[derive(Clone, Copy, Debug, Deserialize, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum RevisionKind { SourceBytes }

// Deserialization alone does not validate a reference. The public read boundary
// checks every length/count before cloning and recomputes census::address.
#[derive(Clone, Debug, Deserialize, Serialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct Reference {
    pub owner: Vec<String>,
    pub kind: Kind,
    pub path: String,
    pub identity: String,
    pub source_revision: String,
    pub record_revision: String,
    pub revision_kind: RevisionKind,
}

#[derive(Clone, Copy, Debug, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum Status { Available, Partial, Unavailable, Changed, Malformed, Capacity, Timeout }

#[derive(Clone, Copy, Debug)]
pub struct Limits {
    pub max_sources: usize,       // 1..=256, default32
    pub max_records: usize,       // 1..=128, default64
    pub max_input_bytes: usize,   // bounded aggregate, default4MiB, ceiling8MiB
    pub max_hits: usize,          // 1..=128, default20
    pub max_search_bytes: usize,  // 4096..=1MiB, default65536
    pub max_read_bytes: usize,    // 4096..=8MiB, default8MiB
    pub deadline_ms: u64,         // 1..=2000, default500
}

#[derive(Clone, Debug, Serialize)]
pub struct Hit {
    pub reference: Reference,
    pub title: String,
    pub score: f64,
    pub snippet: String,
    pub snippet_truncated: bool,
    pub runtime: Runtime,
    pub callable: bool, // alwaysfalse; never copied from owner/model reply
}

#[derive(Clone, Debug, Serialize)]
pub struct SourceStatus {
    pub owner: Vec<String>,
    pub kind: Kind,
    pub status: Status,
    pub index_revision: Option<String>,
}

#[derive(Clone, Debug, Serialize)]
pub struct SearchResult {
    schema: &'static str, // cartridge-source-search/v1
    status: Status,
    complete: bool,
    truncated: bool,
    omitted: bool,
    census_revision: String,
    hits: Vec<Hit>,
    sources: Vec<SourceStatus>,
    // Private fields with borrowed getters keep the returned snapshot immutable.
}

#[derive(Clone, Debug, Serialize)]
pub struct ReadResult {
    schema: &'static str,
    status: Status,
    complete: bool,
    reference: Option<Reference>, // present only on validated public success
    text: Option<String>,        // complete exact UTF8 source, never a projection
    bytes: Option<usize>,
    callable: bool,
}

pub async fn search<F, Fut>(_census: &Census, _query: &str, _limits: Limits, _call: F) -> SearchResult
where F: FnMut(Kind, PathBuf, OwnerRequest) -> Fut, Fut: Future<Output = Value> {
    todo!("defer implementation until dependency source is collected")
}
pub async fn search_until<F, Fut>(_census: &Census, _query: &str, _limits: Limits, _deadline: Instant, _call: F) -> SearchResult
where F: FnMut(Kind, PathBuf, OwnerRequest) -> Fut, Fut: Future<Output = Value> {
    todo!("use min(shared absolute deadline, validated local deadline)")
}
pub async fn read<F, Fut>(_census: &Census, _reference: &Reference, _limits: Limits, _call: F) -> ReadResult
where F: FnMut(Kind, PathBuf, OwnerRequest) -> Fut, Fut: Future<Output = Value> {
    todo!("validate/recompute exact structured owner address; no basename lookup")
}
pub async fn read_until<F, Fut>(_census: &Census, _reference: &Reference, _limits: Limits, _deadline: Instant, _call: F) -> ReadResult
where F: FnMut(Kind, PathBuf, OwnerRequest) -> Fut, Fut: Future<Output = Value> {
    todo!("one selected owner read with expected source and record revisions")
}
