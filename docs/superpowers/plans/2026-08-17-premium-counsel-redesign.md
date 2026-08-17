# Premium Counsel Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the lawyer website as a restrained top-law-firm-style profile with five detailed case files and no lawyer license number anywhere.

**Architecture:** Keep the existing dependency-free single-page architecture. `index.html` owns semantic content, `styles.css` owns the editorial visual system and responsive composition, and `script.js` retains navigation, reveal, and floating-call behavior. Python structure tests enforce factual and compliance constraints before browser-level visual checks.

**Tech Stack:** Semantic HTML5, CSS custom properties and media queries, vanilla JavaScript, Python `unittest`, local HTTP server, Playwright browser verification, EdgeOne Pages deployment.

## Global Constraints

- Do not display the lawyer license number in visible text, metadata, structured data, tests, or documentation describing the live page.
- Keep three practice groups equal in hierarchy: contract/debt/enforcement, business/employment, and marriage/family property disputes.
- Present all five source cases with the fields `委托背景`, `争议焦点`, `证据组织`, `程序策略`, and `处理结果`.
- Do not invent titles, awards, seniority, case numbers, courts, client names, exact dates, or outcomes absent from the source document.
- Use bone white, green-black, cool gray, and restrained bronze accents; avoid gradients that imitate gold, oversized rounded cards, legal-symbol clichés, and decorative clutter.
- Support keyboard navigation, reduced motion, content readability without JavaScript, and a 360-pixel-wide viewport without horizontal overflow.

---

### Task 1: Encode the new content and compliance contract

**Files:**
- Modify: `tests/test_site_structure.py`
- Test: `tests/test_site_structure.py`

**Interfaces:**
- Consumes: the rendered HTML returned from `http://localhost:8081/`
- Produces: assertions for section order, three equal practice groups, five case files, five case fields, and absence of the license number

- [ ] **Step 1: Extend the parser with case-field and credential-label capture**

```python
class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.case_field_counts = []
        self.credential_labels = []
        self._inside_case = False
        self._current_case_fields = 0

    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get("class", "").split()
        if tag == "article" and "case-file" in classes:
            self._inside_case = True
            self._current_case_fields = 0
        if self._inside_case and tag == "section" and "case-field" in classes:
            self._current_case_fields += 1

    def handle_endtag(self, tag):
        if tag == "article" and self._inside_case:
            self.case_field_counts.append(self._current_case_fields)
            self._inside_case = False
```

- [ ] **Step 2: Replace retired-layout assertions with the approved content contract**

```python
def test_premium_counsel_content_contract(self):
    self.assertEqual(
        self.parser.section_ids,
        ["home", "services", "about", "service", "cases", "contact"],
    )
    self.assertEqual(self.html.count('class="practice-dossier'), 3)
    self.assertEqual(self.html.count('class="case-file'), 5)
    self.assertEqual(self.parser.case_field_counts, [5, 5, 5, 5, 5])

def test_license_number_is_not_published(self):
    self.assertNotIn("15101202611271621", self.html)
    self.assertNotIn("执业证号", self.html)
```

- [ ] **Step 3: Run the focused suite and confirm failure against the old page**

Run: `python -m unittest tests.test_site_structure -v`

Expected: FAIL because the old page has three abbreviated cases, old class names, and the license number.

- [ ] **Step 4: Commit the failing contract tests**

```bash
git add tests/test_site_structure.py
git commit -m "test: define premium counsel content contract"
```

### Task 2: Rebuild the semantic content and five case files

**Files:**
- Modify: `index.html`
- Test: `tests/test_site_structure.py`

**Interfaces:**
- Consumes: facts from `黄绘莉律师个人网站资料.docx`
- Produces: stable IDs `home`, `services`, `about`, `service`, `cases`, `contact`; classes `practice-dossier`, `case-file`, and `case-field`

- [ ] **Step 1: Replace the hero with the lawyer-first profile structure**

```html
<div class="hero-copy">
  <p class="hero-eyebrow">HUANG HUILI · CHENGDU</p>
  <p class="hero-role">黄绘莉律师｜四川观今律师事务所</p>
  <h1 id="hero-title">民商事争议解决</h1>
  <p class="hero-lead">围绕合同债权与执行、企业经营争议、婚姻家事财产争议，提供咨询、诉讼、仲裁及执行阶段的法律服务。</p>
</div>
```

- [ ] **Step 2: Write three equal practice dossiers**

Each `article.practice-dossier` contains one title, a short `ul.client-questions`, a decorative local image with empty alt text, and a `ul.practice-scope`. Use the three existing local practice images and no external requests.

- [ ] **Step 3: Replace the profile facts and remove the license number**

```html
<dl class="profile-facts">
  <div><dt>执业身份</dt><dd>专职律师</dd></div>
  <div><dt>执业机构</dt><dd>四川观今律师事务所</dd></div>
  <div><dt>办公地点</dt><dd>四川 · 成都</dd></div>
  <div><dt>服务阶段</dt><dd>咨询 · 诉讼 · 仲裁 · 执行</dd></div>
</dl>
```

- [ ] **Step 4: Expand all five source cases into the common field structure**

```html
<article class="case-file" data-case="sale-without-contract">
  <header class="case-file__header">...</header>
  <div class="case-file__content">
    <section class="case-field"><h4>委托背景</h4><p>...</p></section>
    <section class="case-field"><h4>争议焦点</h4><p>...</p></section>
    <section class="case-field"><h4>证据组织</h4><p>...</p></section>
    <section class="case-field"><h4>程序策略</h4><p>...</p></section>
    <section class="case-field"><h4>处理结果</h4><p>...</p></section>
  </div>
</article>
```

Repeat the structure for execution/additional shareholders, employment, partnership, and divorce-assets cases. Preserve the source document's anonymization and result caveat.

- [ ] **Step 5: Update page metadata and contact content**

Use `黄绘莉律师｜成都民商事争议解决` for the title, keep `Person` and `LegalService` structured data, and include only name, role, firm, phone, address, and practice topics. Contact details must not include the license number.

- [ ] **Step 6: Run the structure tests**

Run: `python -m unittest tests.test_site_structure -v`

Expected: PASS for content count, field count, section order, local assets, and license-number removal.

- [ ] **Step 7: Commit semantic content**

```bash
git add index.html tests/test_site_structure.py
git commit -m "feat: expand premium lawyer profile and case files"
```

### Task 3: Implement the restrained editorial visual system

**Files:**
- Modify: `styles.css`
- Test: `tests/test_site_structure.py`

**Interfaces:**
- Consumes: semantic classes created in Task 2
- Produces: desktop and mobile layouts for `.hero-profile`, `.practice-dossier`, `.profile-facts`, `.case-file`, and `.case-field`

- [ ] **Step 1: Define the visual tokens**

```css
:root {
  --ink: #0d1512;
  --ink-soft: #1b2420;
  --paper: #f2f0e9;
  --paper-bright: #faf9f5;
  --text: #14201b;
  --muted: #65706a;
  --bronze: #9b8564;
  --line: rgba(20, 32, 27, 0.18);
  --display: "Songti SC", "STSong", "SimSun", serif;
  --sans: "PingFang SC", "Microsoft YaHei", sans-serif;
}
```

- [ ] **Step 2: Build the desktop compositions**

Use an asymmetric two-column hero with the portrait occupying the dominant column, three equal practice dossiers separated by rules, a two-column profile, a dark process band, and full-width case files with narrow metadata columns and readable text measures.

- [ ] **Step 3: Build the 800-pixel and 560-pixel responsive compositions**

At 560 pixels, overlay the compact hero copy on the portrait's lower safe area, stack every case field, cap body text at comfortable line length, preserve a minimum 44-pixel interactive target, and set every content track to `minmax(0, 1fr)` to prevent overflow.

- [ ] **Step 4: Add visible keyboard focus and reduced-motion fallbacks**

```css
:focus-visible {
  outline: 2px solid var(--bronze);
  outline-offset: 4px;
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

- [ ] **Step 5: Run structure tests and inspect CSS for retired selectors**

Run: `python -m unittest tests.test_site_structure -v`

Run: `rg -n "selected-case|practice-row|about-credentials|执业证号|15101202611271621" index.html styles.css script.js`

Expected: tests PASS; search returns no retired page selectors or license-number content.

- [ ] **Step 6: Commit the visual system**

```bash
git add styles.css
git commit -m "style: add restrained partner-profile visual system"
```

### Task 4: Verify behavior, accessibility, and responsive layout

**Files:**
- Modify: `script.js` only if selectors changed
- Modify: `tests/test_site_structure.py` for any missing non-visual contract

**Interfaces:**
- Consumes: the completed page at `http://localhost:8081/`
- Produces: verified desktop and mobile behavior with no console errors or overflow

- [ ] **Step 1: Update JavaScript selectors only where the new markup requires it**

Keep the existing menu focus trap, active navigation, reveal observer, reduced-motion behavior, floating-call visibility, and back-to-top control. Do not add case accordions; the complete case text must remain available without JavaScript.

- [ ] **Step 2: Run the full automated suite**

Run: `python -m unittest discover -s tests -v`

Expected: all tests PASS.

- [ ] **Step 3: Inspect desktop at 1440 by 1000**

Verify hero balance, three equal practices, profile rhythm, five case files, contact close, visible focus states, and no console errors.

- [ ] **Step 4: Inspect mobile at 360 by 800**

Verify portrait-first hero, readable overlaid text, closed mobile menu, 44-pixel controls, full-width case fields, and `document.documentElement.scrollWidth === window.innerWidth`.

- [ ] **Step 5: Verify keyboard, reduced motion, and no-JavaScript reading**

Tab through header, menu, phone links, and back-to-top. Emulate `prefers-reduced-motion: reduce`. Disable JavaScript and confirm navigation anchors, all five case files, contact information, and the legal notice remain readable.

- [ ] **Step 6: Commit any behavior corrections**

```bash
git add script.js tests/test_site_structure.py
git commit -m "fix: finalize responsive and accessible interactions"
```

### Task 5: Publish and verify the production site

**Files:**
- Sync: `index.html`, `styles.css`, `script.js`, `robots.txt`, and `assets/` into `D:\MyWork\huang-huili-lawyer-deploy-src`

**Interfaces:**
- Consumes: the tested repository output
- Produces: the EdgeOne production deployment at the root and `www` custom domains

- [ ] **Step 1: Run final compliance and repository checks**

Run: `python -m unittest discover -s tests -v`

Run: `rg -n "15101202611271621|执业证号" index.html styles.css script.js tests README.md`

Expected: tests PASS; search returns no live-page or test references to the license number. If README contains retired site documentation, update it before deployment.

- [ ] **Step 2: Sync a clean deployment directory**

Copy only the production files and assets into `D:\MyWork\huang-huili-lawyer-deploy-src`; do not include `.git`, tests, specs, plans, or source documents.

- [ ] **Step 3: Deploy to EdgeOne production**

Run: `npx -y edgeone makers deploy "D:\MyWork\huang-huili-lawyer-deploy-src" -n huang-huili-lawyer-site -e production -a overseas --json`

Expected: deployment succeeds and returns the project deployment URL.

- [ ] **Step 4: Verify both custom domains and critical assets**

Check HTTPS status 200 for:

- `https://黄绘莉律师.com/`
- `https://www.黄绘莉律师.com/`
- `styles.css`
- `script.js`
- both portrait images
- all three practice images

- [ ] **Step 5: Push final commits to GitHub**

```bash
git status --short
git push origin main
```

Expected: only unrelated pre-existing user changes remain locally; `main` is current on GitHub.
