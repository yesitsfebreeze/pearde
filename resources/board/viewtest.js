#!/usr/bin/env node
// pearde viewtest — open a rendered board page in a real browser and report
// what it built.
//
//   node viewtest.js <path-to-.view.html>
//   node viewtest.js http://127.0.0.1:8443/board/<name>
//   node viewtest.js --example            a fresh copy of the example board,
//                                         rendered and opened as a file
//
// Give it the served URL as well as the file. They are different code paths —
// the service injects its own head script and live loop — and a page that is
// fine as a file can be broken as a service.
//
// Exit 0 when every check passes, 1 when one fails, 2 when the browser driver
// is missing. It is a development gate, not part of the view: nothing here is
// loaded by the page and the skill ships no dependency.
//
// It needs `playwright-core` and a Chrome. Install the driver wherever you run
// this — `npm i playwright-core` — and it uses the Chrome already on the
// machine. A real browser rather than a DOM shim, because the page is an ES
// module and the common shims skip module scripts silently, reporting a blank
// page as a pass.

let chromium;
try {
  ({ chromium } = require("playwright-core"));
} catch (e) {
  console.error("viewtest: needs playwright-core — npm i playwright-core");
  console.error("viewtest: it drives the Chrome already installed here.");
  process.exit(2);
}

const path = require("path");
const fs = require("fs");
const os = require("os");
const { spawnSync } = require("child_process");

// --example: copy resources/board/example to a temp dir, plan and render it
// there, and open that page. Never the directory itself — a check that ticks
// a box in the example changes what every other check sees. The copy is
// removed on exit; the snapshots it writes under --snap are keyed by the
// board's own name, `example`.
let arg = process.argv[2];
let scratch = null;
if (arg === "--example") {
  scratch = fs.mkdtempSync(path.join(os.tmpdir(), "pearde-example-"));
  fs.cpSync(path.join(__dirname, "example"), path.join(scratch, "pearde"), { recursive: true });
  const r = spawnSync("python3", [path.join(__dirname, "plan.py"), "gantt", scratch],
                      { encoding: "utf8" });
  const printed = [...(r.stdout || "").matchAll(/^gantt: (.+\.html)$/mg)].pop();
  if (r.status !== 0 || !printed) {
    console.error("viewtest: could not render the example copy\n" + (r.stderr || r.stdout));
    fs.rmSync(scratch, { recursive: true, force: true });
    process.exit(2);
  }
  arg = printed[1].trim();
  process.on("exit", () => fs.rmSync(scratch, { recursive: true, force: true }));
}
const served = /^https?:\/\//.test(arg || "");
if (!arg || (!served && !fs.existsSync(arg))) {
  console.error("viewtest: node viewtest.js <path-to-.view.html | url | --example>");
  process.exit(2);
}
const file = served ? arg : path.resolve(arg);
(async () => {
  const browser = await chromium.launch({ channel: "chrome" });
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
  const errors = [];
  page.on("pageerror", e => errors.push(String(e.message).split("\n")[0]));
  page.on("console", m => { if (m.type() === "error") errors.push(m.text()); });
  page.on("response", r => {
    if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
  });

  // count real canvas work without a stub: wrap the 2D context up front
  await page.addInitScript(() => {
    window.__draws = 0;
    const g = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (...a) {
      const ctx = g.apply(this, a);
      if (!ctx || ctx.__wrapped) return ctx;
      ctx.__wrapped = true;
      for (const k of ["fillRect", "strokeRect", "fillText", "stroke", "fill",
                       "drawImage", "arc", "moveTo", "lineTo", "roundRect"]) {
        const f = ctx[k];
        if (typeof f === "function") ctx[k] = function (...b) { window.__draws++; return f.apply(this, b); };
      }
      return ctx;
    };
  });

  await page.goto(served ? file : "file://" + file, { waitUntil: "load" });
  await page.waitForTimeout(700);

  const r = await page.evaluate(() => {
    const $ = s => document.querySelector(s), q = s => [...document.querySelectorAll(s)];
    const P = window.pearde;
    return {
      lit: window.__litOK === true,
      slot: !!(window.pearde && typeof window.pearde.slot === "function"),
      seams: ["toolbar", "sidebar", "inspector"]
        .every(n => !!document.getElementById("seam-" + n)),
      seamsQuiet: ["toolbar", "sidebar", "inspector"].every(n => {
        const el = document.getElementById("seam-" + n);
        return el.children.length > 0 || getComputedStyle(el).display === "none";
      }),
      pearde: !!P && typeof P === "object",
      data: !!(P && P.data && P.data.cpm),
      board: !!(P && "board" in P),
      refresh: !!(P && typeof P.refresh === "function"),
      apply: !!(P && typeof P.apply === "function"),
      onHold: !!(P && typeof P.onHold === "function"),
      hold: typeof window.__pearde_hold === "function",
      titlebar: !!$("#titlebar"),
      views: q("#views a").length,
      canvas: !!$("#cv"),
      draws: window.__draws,
      land: !!$("#land"),
      frontierIsElement: $("#land")?.tagName.toLowerCase() === "pearde-frontier",
      frontierLightDom: !$("#land")?.shadowRoot,
      frontierRows: $("#land") ? $("#land").querySelectorAll("[data-go]").length : 0,
      stats: (($("#stats") || {}).textContent || "").trim().length,
      drawer: !!$("#drawer"),
      canvasPainted: (() => {
        const c = $("#cv"); if (!c) return false;
        return c.width > 0 && c.height > 0;
      })(),
    };
  });

  const checks = [
    ["no page error", errors.length === 0, errors.slice(0, 2).join(" | ")],
    ["Lit is bound, offline", r.lit, ""],
    ["pearde.slot is callable", r.slot, ""],
    ["all three seams present", r.seams, ""],
    ["an unused seam renders nothing", r.seamsQuiet, ""],
    ["window.pearde published", r.pearde, ""],
    ["pearde.data is the payload", r.data, ""],
    ["pearde.board is the key", r.board, ""],
    ["pearde.refresh callable", r.refresh, ""],
    ["pearde.apply callable", r.apply, ""],
    ["pearde.onHold callable", r.onHold, ""],
    ["hold hook still wired", r.hold, ""],
    ["the toolbar built", r.titlebar, ""],
    ["seven section anchors", r.views === 7, `got ${r.views}`],
    ["the canvas is sized", r.canvasPainted, ""],
    ["the gantt drew", r.draws > 20, `${r.draws} draw ops`],
    ["the frontier column built", r.land, ""],
    ["the frontier is a component", r.frontierIsElement, ""],
    ["it renders into light DOM", r.frontierLightDom, ""],
    ["its rows are doors", r.frontierRows > 0, `${r.frontierRows} doors`],
    ["the stats bar has numbers", r.stats > 0, ""],
    ["the inspector exists", r.drawer, ""],
  ];

  // ── seven views, one at a time ──────────────────────────────────────────
  // The three things this page is, asserted rather than eyeballed: the
  // sections are in the PRD's order, exactly one is visible on load, every
  // one of them has drawn before anything was clicked, and the page does not
  // scroll sideways on a phone.
  const page1 = await page.evaluate(() => {
    const secs = [...document.querySelectorAll("section[data-view]")];
    return {
      order: secs.map(s => s.dataset.view),
      // one section visible on load — the timeline — the rest display:none
      visible: secs.filter(s => getComputedStyle(s).display !== "none")
                   .map(s => s.dataset.view),
      // a section that never drew is an empty frame: its content is missing
      // from the DOM. Hidden sections measure 0, so this checks the DOM, not
      // the box — the check that would have caught the one-draw-per-repaint
      // dispatcher.
      emptyHosts: secs.filter(s => {
        const host = s.querySelector(
          "pearde-board,pearde-list,pearde-memos,pearde-report,#asks,#tiles");
        return host && host.querySelectorAll("*").length === 0;
      }).map(s => s.dataset.view),
      // the timeline's own content — the legend is DOM, the canvas is
      // checked separately above
      timelineDrew: (() => {
        const t = document.querySelector('section[data-view="timeline"]');
        return !!t && !!t.querySelector("#legend *");
      })(),
      whatsup: !!document.querySelector("pearde-whatsup"),
      // the prose lives in the state panel now, behind the left edge tab —
      // the plan keeps the viewport, the words keep their reading measure
      statePanel: (() => {
        const s = document.querySelector("#state");
        return !!s && !!s.querySelector("pearde-whatsup") &&
               !!s.querySelector("#purpose") && !!s.querySelector("#now") &&
               !!document.querySelector("#statetab");
      })(),
      // the half of the panel that is not the report — all a merged page has
      stateDoors: (() => {
        const s = document.querySelector("#state");
        return !!s && !!s.querySelector("#purpose") && !!s.querySelector("#now")
               && !!document.querySelector("#statetab");
      })(),
      boardRows: document.querySelectorAll("#boardlist .brow").length,
      tcontrolsInside: !!document.querySelector(
        'section[data-view="timeline"] #tcontrols'),
      focusTab: !!document.querySelector(
        'section[data-view="timeline"] #landtog'),
    };
  });
  // `all` is the same page over every watched board (references/parts/all.md):
  // it gains the dashboard it opens on and loses the two things that belong
  // to one board — the report, and every door that writes. Everything else on
  // this page is asserted the same way, because it IS the same page.
  const VIRTUAL = await page.evaluate(
    () => !!(window.__PAYLOAD__ && window.__PAYLOAD__.virtual));
  const ORDER = VIRTUAL
    ? ["boards", "timeline", "board", "analytics", "asks", "list", "memos"]
    : ["timeline", "board", "analytics", "asks", "list", "memos", "report"];
  const FIRST = VIRTUAL ? "boards" : "timeline";
  checks.push(["the sections are in the PRD's order",
               page1.order.join(",") === ORDER.join(","), page1.order.join(" ")]);
  checks.push(["exactly one section is visible on load",
               page1.visible.length === 1 && page1.visible[0] === FIRST,
               page1.visible.join(" ")]);
  checks.push(["every section drew on first load, no click",
               page1.emptyHosts.length === 0,
               page1.emptyHosts.length ? "empty frames: " + page1.emptyHosts.join(" ") : ""]);
  checks.push(["the timeline's legend drew",
               page1.timelineDrew, ""]);
  checks.push([VIRTUAL
                 ? "the state panel holds the doors and the vision line"
                 : "the state panel holds the doors, the prose and the vision line",
               VIRTUAL ? (!page1.whatsup && page1.stateDoors)
                       : (page1.whatsup && page1.statePanel), ""]);
  if (VIRTUAL)
    checks.push(["the merged page draws a row per board",
                 page1.boardRows > 0, `${page1.boardRows} boards`]);
  checks.push(["the plan's footer strip is inside the plan's section",
               page1.tcontrolsInside, ""]);
  checks.push(["the focus tab is too", page1.focusTab, ""]);

  // narrow: the page must not scroll sideways. Before this PRD it did —
  // `body.scrollWidth` 543 against a 390 client, the bar alone 449.
  const wide0 = page.viewportSize();
  await page.setViewportSize({ width: 390, height: 844 });
  await page.waitForTimeout(400);
  const narrow = await page.evaluate(() => ({
    body: document.body.scrollWidth,
    client: document.documentElement.clientWidth,
    culprits: [...document.querySelectorAll("body *")]
      .filter(e => e.getBoundingClientRect().width >
                   document.documentElement.clientWidth + 1)
      .filter(e => !e.closest("#list"))     // the table scrolls in its own box
      .slice(0, 4)
      .map(e => e.tagName.toLowerCase() + (e.id ? "#" + e.id : "")),
  }));
  checks.push(["at 390px the page does not scroll sideways",
               narrow.body === narrow.client,
               `body ${narrow.body} vs client ${narrow.client}` +
               (narrow.culprits.length ? " — " + narrow.culprits.join(" ") : "")]);
  if (wide0) await page.setViewportSize(wide0);
  await page.waitForTimeout(300);

  // N opens the new-PRD modal, and the modal carries its editor toolbar.
  // On `all` there is no such door at all, and its absence is the assertion.
  if (VIRTUAL) {
    const doors = await page.evaluate(() => ({
      newprd: !!document.querySelector("#newprd"),
      save: !!document.querySelector("#dgo"),
      report: !!document.querySelector('#views a[data-v="report"]'),
    }));
    checks.push(["the merged page offers no door that writes",
                 !doors.newprd && !doors.save && !doors.report,
                 [doors.newprd && "+ PRD", doors.save && "save",
                  doors.report && "report"].filter(Boolean).join(" ")]);
  } else {
  await page.keyboard.press("n");
  await page.waitForTimeout(250);
  const modal = await page.evaluate(() => ({
    open: !!document.querySelector("#newbox.on"),
    tools: !!document.querySelector("#newbox #ntools #mdbold"),
  }));
  checks.push(["N opens the new-PRD modal with its editor toolbar",
               modal.open && modal.tools,
               modal.open && modal.tools ? ""
                 : modal.open ? "toolbar missing" : "did not open"]);
  await page.keyboard.press("Escape");
  await page.waitForTimeout(150);
  }

  // the theme switch: pin, and the root wears the stamp; a full cycle
  // releases it back to the system
  const t0 = await page.evaluate(() => document.documentElement.dataset.theme || "");
  await page.click("#themetog").catch(() => {});
  await page.waitForTimeout(150);
  const t1 = await page.evaluate(() => document.documentElement.dataset.theme || "");
  await page.click("#themetog").catch(() => {});
  await page.click("#themetog").catch(() => {});
  await page.waitForTimeout(150);
  const t3 = await page.evaluate(() => document.documentElement.dataset.theme || "");
  checks.push(["the theme switch pins a theme and a cycle releases it",
               t0 === "" && (t1 === "light" || t1 === "dark") && t3 === "",
               `${t0 || "system"} → ${t1 || "system"} → ${t3 || "system"}`]);

  for (const v of ORDER) {
    const before = errors.length;
    await page.click(`#views a[data-v="${v}"]`).catch(e => errors.push(`${v}: ${e.message}`));
    await page.waitForTimeout(120);
    const shown = await page.evaluate(n => {
      const secs = [...document.querySelectorAll("section[data-view]")];
      const visible = secs.filter(s => getComputedStyle(s).display !== "none")
                          .map(s => s.dataset.view);
      return visible.length === 1 && visible[0] === n;
    }, v);
    checks.push([`section "${v}" is the one shown`, errors.length === before && shown,
                 errors.slice(before).join(" | ") || (shown ? "" : "not the only section shown")]);
    // the board is a kanban: it must fit the viewport, not scroll the page.
    // The columns scroll inside themselves; the view does not.
    if (v === "board") {
      const fits = await page.evaluate(() => {
        const sh = document.documentElement.scrollHeight;
        return sh <= window.innerHeight + 1;
      });
      checks.push(["the board view fits the viewport", fits,
                   fits ? "" : "the page scrolls on the board view"]);
    }
    // asks reads each PRD over the wire and renders its pass as picks. A card
    // that could not read, or a parsed pass showing no options, is the view
    // degrading quietly — which is exactly what it used to do.
    if (v === "asks") {
      await page.waitForTimeout(900);
      const a = await page.evaluate(() => {
        const cards = [...document.querySelectorAll(".ask2")];
        return {
          n: cards.length,
          broken: cards.filter(c => /could not read the PRD/.test(c.textContent)).length,
          withPicks: cards.filter(c => c.querySelector(".qq .opt")).length,
          // a pass that parsed but rendered no options is the failure mode:
          // a card showing an empty question block answers nothing
          emptyPasses: cards.filter(c =>
            c.querySelector(".qq") && !c.querySelector(".qq .opt")).length,
          // a parsed pass answers per question — the card's bulk
          // textarea/submit must be gone, one submit per question only
          // — a foot carrying a textarea or a send button, still visible
          // beside a parsed pass. A foot holding only a link (`all` puts the
          // door to the PRD's own board there) answers nothing and is not one
          bulkOnParsed: cards.filter(c => {
            const f = c.querySelector(".foot");
            return c.querySelector(".qq") && f &&
              getComputedStyle(f).display !== "none" &&
              !!f.querySelector("textarea, .send");
          }).length,
          // every question carries its own reopen (revealed once answered)
          passesMissingReopen: [...document.querySelectorAll("#asks .qq")]
            .filter(q => !q.querySelector(".qreopen")).length,
          // a card that is not askable says so rather than dumping the body
          dumps: cards.filter(c => c.querySelector(".q") &&
            !c.querySelector(".qq") && !c.querySelector(".qbad") &&
            !/could not read|nothing yet|through the service/
              .test(c.querySelector(".q").textContent) &&
            !c.querySelector(".flag.blocked")).length,
          // every question answers on its own, and one already written back
          // is not in the inbox at all — it is in the answered panel
          passesMissingSend: [...document.querySelectorAll("#asks .qq")].filter(q =>
            !q.classList.contains("answered") && !q.querySelector(".qsend")).length,
          answeredStillAsking: document.querySelectorAll("#asks .qq.answered")
            .length,
          panel: !!document.querySelector("#answered .ahd"),
          panelRows: document.querySelectorAll("#answered .adone").length,
          panelUnsorted: (() => {
            // newest first, and an undated answer sorts under the dated ones
            const d = [...document.querySelectorAll("#answered .when")]
              .map(w => w.textContent.trim());
            return d.filter((x, i) => i && d[i - 1] !== "undated" &&
              x !== "undated" && d[i - 1] < x).length;
          })(),
        };
      });
      checks.push(["no ask card failed to read its PRD", a.broken === 0,
                   `${a.broken} of ${a.n}`]);
      checks.push(["no card renders a pass with no options", a.emptyPasses === 0,
                   `${a.withPicks} of ${a.n} cards carry picks`]);
      checks.push(["a parsed pass has no bulk submit",
                   a.bulkOnParsed === 0, `${a.bulkOnParsed} cards`]);
      checks.push(["every question carries its own reopen",
                   a.passesMissingReopen === 0, ""]);
      checks.push(["an unaskable card says so instead of dumping the body",
                   a.dumps === 0, `${a.dumps} cards`]);
      checks.push(["every open question has its own submit",
                   a.passesMissingSend === 0, ""]);
      checks.push(["an answered question has left the inbox",
                   a.answeredStillAsking === 0, ""]);
      checks.push(["the answered panel built", a.panel,
                   `${a.panelRows} answered`]);
      checks.push(["the answered panel is in date order",
                   a.panelUnsorted === 0, `${a.panelUnsorted} out of order`]);
    }
  }

  // The plan's scale is fitted to the plot's width and to how much plan is
  // left. A window resized while the plan is hidden fits to a plot of no
  // width — every bar in a 120px band at the left of the frame, the minimap
  // still spanning the whole track because it never reads the scale. So:
  // hide the plan, resize, come back, and the world the scroller is told
  // about must still be wider than the frame it is read in.
  await page.click('#views a[data-v="board"]').catch(() => {});
  await page.waitForTimeout(120);
  await page.setViewportSize({ width: 1100, height: 900 });
  await page.waitForTimeout(300);
  await page.click('#views a[data-v="timeline"]').catch(() => {});
  await page.waitForTimeout(400);
  const fit = await page.evaluate(() => {
    const plot = document.getElementById("plot");
    const sel = document.getElementById("zsel");
    return { w: plot.clientWidth,
             spacer: parseFloat(document.getElementById("spacer").style.width) || 0,
             view: sel ? sel.value : "" };
  });
  checks.push(["a resize behind the plan does not squash the plot",
               fit.view !== "default" || fit.spacer > fit.w + 1,
               `${fit.view} · spacer ${Math.round(fit.spacer)} vs plot ${fit.w}`]);
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.waitForTimeout(300);

  // --snap <dir> writes each view's DOM; --check <dir> compares against it.
  // A port is provable when every view's markup is unchanged.
  const mode = process.argv[3], dir = process.argv[4];
  if (mode === "--snap" || mode === "--check") {
    fs.mkdirSync(dir, { recursive: true });
    // the board's own name, not its directory — every board's dir is `prds`,
    // so a directory-derived key collides across boards
    const tag = (await page.evaluate(() => (window.pearde && window.pearde.data
      && window.pearde.data.board) || "board")).replace(/[^A-Za-z0-9_.-]/g, "-");
    for (const v of ["timeline", "board", "asks", "list", "analytics", "memos", "report"]) {
      await page.click(`#views a[data-v="${v}"]`).catch(() => {});
      await page.waitForTimeout(150);
      const dom = await page.evaluate(n => {
        const s = document.querySelector(`section[data-view="${n}"]`);
        const land = document.querySelector("#land");
        // Lit stamps a random marker id per page load, the service prints
        // "3s ago", and a claim written at a fixed time renders "holding 40m"
        // that grows with the clock. None is a change to the markup.
        const clean = h => h
          .replace(/lit\$\d+\$/g, "lit$M$")
          .replace(/>[^<]*?\b\d+[smhd] ago\b[^<]*?</g, ">AGO<")
          .replace(/holding \d+(?:\.\d+)?[mh]\b/g, "holding AGO")
          .replace(/\s+/g, " ").trim();
        const text = e => (e ? e.textContent : "").replace(/\s+/g, " ").trim();
        return {
          markup: clean((s ? s.innerHTML : "") + "||" + (land ? land.innerHTML : "")),
          text: (text(s) + " || " + text(land)).replace(/\b\d+[smhd] ago\b/g, "AGO")
            .replace(/holding \d+(?:\.\d+)?[mh]\b/g, "holding AGO"),
        };
      }, v);
      const at = path.join(dir, `${tag}.${v}.html`);
      const atText = path.join(dir, `${tag}.${v}.txt`);
      if (mode === "--snap") {
        fs.writeFileSync(at, dom.markup);
        fs.writeFileSync(atText, dom.text);
      } else {
        for (const [what, file, got] of [["markup", at, dom.markup],
                                          ["text", atText, dom.text]]) {
          const want = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : null;
          checks.push([`view "${v}" ${what} unchanged`, want !== null && want === got,
                       want === null ? "no snapshot"
                         : want === got ? ""
                         : `differs at char ${[...got].findIndex((c, i) => c !== want[i])}`]);
        }
      }
    }
    if (mode === "--snap") console.log(`  snapshots written to ${dir}`);
  }

  // The whole track is the floor: there is nothing before the first landed
  // bar and nothing after the vision, so zooming out past that buys empty
  // ground with the plan's own size. Held down, the − button must land on
  // the same scale "fit all" does and stop there.
  await page.click('#views a[data-v="timeline"]').catch(() => {});
  await page.waitForTimeout(200);
  for (let i = 0; i < 25; i++) await page.click("#zo").catch(() => {});
  await page.waitForTimeout(500);
  const out = await page.evaluate(() => ({
    plot: document.getElementById("plot").clientWidth,
    spacer: Math.round(parseFloat(document.getElementById("spacer").style.width) || 0),
  }));
  await page.click("#cv").catch(() => {});
  await page.keyboard.press("f");
  await page.waitForTimeout(500);
  const all = await page.evaluate(() =>
    Math.round(parseFloat(document.getElementById("spacer").style.width) || 0));
  checks.push(["zooming out stops at the whole track",
               out.spacer > 0 && Math.abs(out.spacer - all) <= 2 &&
               out.spacer >= out.plot,
               `−25 → ${out.spacer}, fit all → ${all}, plot ${out.plot}`]);

  // "fit all" is both axes: a plan that fits across and runs off the bottom
  // is not fitted. After f the world the scroller is told about must be no
  // taller than the plot, so every row is on the screen at once.
  const down = await page.evaluate(() => ({
    world: Math.round(parseFloat(document.getElementById("spacer").style.height) || 0),
    plot: document.getElementById("plot").clientHeight,
  }));
  checks.push(["fit all puts every row on the screen",
               down.world > 0 && down.world <= down.plot + 2,
               `world ${down.world}, plot ${down.plot}`]);

  // The boot fit: the page is opened once, at the width it keeps. The focus
  // panel is 272px of the plot and the markup paints it open, so a board
  // opened with the panel shut used to fit the gantt narrow and then slide,
  // and the reader watched the plan zoom out on every load. Sampled per
  // frame from before the module runs: the plot's width and the world the
  // scroller is told about may each land on one value, not walk to it.
  await page.addInitScript(() => {
    try { localStorage.setItem("pearde.land", "0"); } catch (e) {}
    window.__boot = [];
    const tick = () => {
      const p = document.getElementById("plot"), sp = document.getElementById("spacer");
      if (p) window.__boot.push([p.clientWidth,
                                 Math.round(parseFloat(sp && sp.style.width) || 0)]);
      if (performance.now() < 1500) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });
  await page.reload({ waitUntil: "load" });
  await page.waitForTimeout(1700);
  const walk = await page.evaluate(() => {
    // a fit that has not happened yet is 0, not a step
    const seen = (window.__boot || []).filter(s => s[1] > 0);
    const distinct = seen.filter((s, i) => !i || s[0] !== seen[i - 1][0] ||
                                                 s[1] !== seen[i - 1][1]);
    return { frames: seen.length, steps: distinct.length,
             first: distinct[0], last: distinct[distinct.length - 1] };
  });
  checks.push(["the plan does not animate its way to width on load",
               walk.frames > 0 && walk.steps <= 2,
               `${walk.steps} step(s) over ${walk.frames} frames` +
               (walk.first ? ` · ${walk.first.join("/")} → ${(walk.last || []).join("/")}` : "")]);

  await browser.close();
  let bad = 0;
  for (const [name, ok, note] of checks) {
    if (!ok) bad++;
    console.log(`  ${ok ? "ok  " : "FAIL"}  ${name}` + (note ? (ok ? `  (${note})` : `  — ${note}`) : ""));
  }
  console.log(`\n${checks.length - bad}/${checks.length} passed`);
  process.exit(bad ? 1 : 0);
})();
