import fs from 'node:fs';
import path from 'node:path';
const directory = import.meta.dir;
const [variant, guidanceFile, pairFile] = process.argv.slice(2);
if (!variant || !/^[a-z0-9-]+$/.test(variant) || !guidanceFile) throw Error('usage: bun run run.ts VARIANT GUIDANCE_FILE');
const digest = (value: string | Buffer) => new Bun.CryptoHasher('sha256').update(value).digest('hex');
const corpus = JSON.parse(fs.readFileSync(path.join(directory, 'fixtures.json'), 'utf8'));
const rubric = JSON.parse(fs.readFileSync(path.join(directory, 'rubric.json'), 'utf8'));
const frozen = JSON.parse(fs.readFileSync(path.join(directory, 'freeze.json'), 'utf8'));
for (const [name, sha] of Object.entries(frozen.files)) {
  if (digest(fs.readFileSync(path.join(directory, name))) !== sha) throw Error(`frozen input changed: ${name}`);
}
const pair = pairFile ? JSON.parse(fs.readFileSync(pairFile, 'utf8')) : null;
if (pair && pair.frozen_rubric_sha256 !== digest(fs.readFileSync(path.join(directory, 'rubric.json')))) throw Error('pair does not bind frozen rubric');
const modelName = pair?.model ?? rubric.model;
const settings = pair?.settings ?? rubric.settings;
const guidance = fs.readFileSync(guidanceFile, 'utf8');
const endpoint = rubric.endpoint;
const api = new URL(endpoint).origin;
async function metadata() {
  const tags = await (await fetch(api + '/api/tags')).json() as any;
  const model = tags.models.find((row: any) => row.name === modelName);
  if (!model) throw Error('frozen model unavailable');
  if (model.remote_host && (!pair || model.remote_host !== pair.remote_host || model.remote_model !== pair.remote_model)) throw Error('remote target differs from frozen pair');
  return model;
}
const installed = await metadata();
if (pair && installed.digest !== pair.expected_digest) throw Error('frozen paired model changed');
const show = await (await fetch(api + '/api/show', { method: 'POST', body: JSON.stringify({ model: modelName }) })).json() as any;
const version = await (await fetch(api + '/api/version')).json();
const output = path.join(directory, 'runs', variant);
fs.mkdirSync(output, { recursive: true });
const runManifest = {
  variant, model: modelName, model_digest: installed.digest,
  tokenizer_revision: pair?.tokenizer_revision ?? installed.digest,
  pair,
  tokenizer_revision_basis: 'The installed GGUF model digest includes its tokenizer; scalar tokenizer metadata is retained below.',
  tokenizer: Object.fromEntries(Object.entries(show.model_info ?? {}).filter(([key, value]) => key.startsWith('tokenizer.') && !Array.isArray(value))),
  model_details: show.details, capabilities: show.capabilities, ollama_version: version,
  endpoint, guidance_sha256: digest(guidance), fixture_sha256: frozen.files['fixtures.json'],
  rubric_sha256: frozen.files['rubric.json'], settings, seeds: rubric.seeds,
};
const manifestPath = path.join(output, 'manifest.json');
if (fs.existsSync(manifestPath)) {
  if (fs.readFileSync(manifestPath, 'utf8') !== JSON.stringify(runManifest, null, 2) + '\n') throw Error('existing run has different bound inputs');
} else fs.writeFileSync(manifestPath, JSON.stringify(runManifest, null, 2) + '\n', { flag: 'wx' });
for (let repeat = 0; repeat < rubric.repetitions; repeat++) {
  for (const fixture of corpus.fixtures) {
    const target = path.join(output, `${repeat + 1}-${fixture.id}.json`);
    if (fs.existsSync(target)) continue;
    const request: any = {
      model: modelName, stream: false,
      messages: [
        { role: 'system', content: guidance },
        { role: 'user', content: `${corpus.common_task}\n\nDeliverable surface: ${fixture.surface}.\n${fixture.task}\n\nSource:\n${fixture.source}` },
      ],
      options: { ...settings, seed: rubric.seeds[repeat] },
    };
    if (pair) request.think = pair.think;
    if (fixture.format) request.format = fixture.format;
    const started = new Date().toISOString();
    const response = await fetch(endpoint, { method: 'POST', body: JSON.stringify(request), signal: AbortSignal.timeout(120_000) });
    const body = await response.json() as any;
    if (!response.ok || body.error || typeof body.message?.content !== 'string' || !Number.isInteger(body.eval_count)) {
      fs.writeFileSync(path.join(output, `error-${Date.now()}-${fixture.id}.json`), JSON.stringify({ started, request, status: response.status, response: body }, null, 2) + '\n');
      throw Error(`model request failed for ${repeat + 1}-${fixture.id}; saved error receipt`);
    }
    let tokenization: any = null;
    try {
    if (pair?.native_completion_tokens && (body.message.thinking || body.model !== pair.response_model)) throw Error('native visible-token pair requires no reasoning and the frozen response model');
    if (pair && !pair.native_completion_tokens) {
      for (const key of ['tokenizer.ggml.add_bos_token','tokenizer.ggml.add_eos_token','tokenizer.ggml.add_padding_token']) {
        if (show.model_info?.[key] !== false) throw Error('raw visible token count requires disabled special-token insertion');
      }
      const tokenRequest = {model:modelName, raw:true, prompt:body.message.content, stream:false, options:{num_predict:1,num_ctx:settings.num_ctx,temperature:0}};
      if (!body.message.content) throw Error('empty deliverable; retain failed response before continuing');
      const tokenResponse = await (await fetch(api + '/api/generate', {method:'POST',body:JSON.stringify(tokenRequest),signal:AbortSignal.timeout(120_000)})).json() as any;
      if (tokenResponse.error || !Number.isInteger(tokenResponse.prompt_eval_count)) throw Error('visible tokenization failed');
      tokenization = {request:tokenRequest,response:tokenResponse,visible_tokens:tokenResponse.prompt_eval_count};
    }
    } catch (error) {
      fs.writeFileSync(path.join(output, `error-${Date.now()}-${fixture.id}.json`), JSON.stringify({ started, request, response: body, tokenization, error: String(error) }, null, 2) + '\n');
      throw error;
    }
    const record = {
      fixture: fixture.id, repeat: repeat + 1, category: fixture.category, started, completed: new Date().toISOString(),
      request, response: body, tokenization, generation_tokens: body.eval_count, output_tokens: tokenization?.visible_tokens ?? body.eval_count, input_tokens: body.prompt_eval_count,
      model_digest: installed.digest, tokenizer_revision: pair?.tokenizer_revision ?? installed.digest,
    };
    fs.writeFileSync(target, JSON.stringify(record, null, 2) + '\n', { flag: 'wx' });
    console.log(`${variant} ${repeat + 1}-${fixture.id}: ${record.output_tokens} output tokens; ${body.done_reason}`);
  }
}
if ((await metadata()).digest !== installed.digest) throw Error('model digest changed during evaluation; run is invalid');
fs.writeFileSync(path.join(output, 'complete.json'), JSON.stringify({ completed: new Date().toISOString(), responses: corpus.fixtures.length * rubric.repetitions, model_digest: installed.digest, manifest_sha256: digest(fs.readFileSync(manifestPath)) }, null, 2) + '\n');
