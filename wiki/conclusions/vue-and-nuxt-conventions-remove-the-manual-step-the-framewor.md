---
title: vue-and-nuxt-conventions-remove-the-manual-step-the-framewor
date: 2026-09-04
type: conclusion
tags: [conclusion, conventions, nuxt, vue]
sources:
  - "[[260904-5564]]"
  - "[[260904-14da]]"
derived_from: []
---

# vue-and-nuxt-conventions-remove-the-manual-step-the-framework-already-does

Every rule across both layers deletes a manual step the framework already performs correctly: useTemplateRef over a bare ref, defineModel over a hand-wired prop-plus-emit pair, auto-import over an explicit import, NuxtLink over RouterLink, nuxt-svgo over manually importing SVG files. The remaining manual code — withDefaults on every optional prop, <ClientOnly>/onMounted around browser-only access — sits exactly where the framework cannot infer the answer: a default value or an SSR/client boundary, both project-specific decisions no auto-import can make.

Consequence: a Vue/Nuxt review reduces to one check — does this line hand-code something Nuxt's build step already resolves, and if so, is there a stated project-specific reason it couldn't be.
