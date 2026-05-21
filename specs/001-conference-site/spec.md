# Feature Specification: LIFO 2027 Conference Website

**Feature Branch**: `001-conference-site`

**Created**: 2026-05-12

**Status**: Draft

**Input**: User description: "Pripraviť stránku pre konferenciu LIFO — Local Innovation Forum. Konferencia bude 11. 2. 2027 v hoteli Clarion Bratislava. Materiály v `podklady/` sú zatiaľ návrhy, nie všetko je finálne."

## Context Summary

LIFO (Local Innovation Forum) je B2B konferencia s ambíciou prepojiť **samosprávy** so **súkromným kapitálom** a urýchliť realizáciu komunálnych projektov (PPP, EPC, energetické komunity, priemyselné parky, infraštruktúra). Konferencia má pozicionovanie "**delivery, nie policy**" — namiesto inšpirácie sľubuje konkrétny matchmaking, blueprints a follow-up. Web je primárne **pre-event** marketingový + konverzný (paid registration) nástroj, ktorý musí osloviť tri samostatné cieľovky (partneri/sponzori, samosprávy, investori) a doručiť ich do správneho toku (formulár pre sponzorov, platený ticketing pre účastníkov).

**Vzťah k platforme Project Nation**: LIFO je dlhodobo plánovaný **ako vstupný bod do širšej platformy Project Nation**, ktorá sa však bude budovať **až po rozbehnutí LIFO**. Pre účely tohto spec-u **rieši sa len LIFO konferencia**; akékoľvek prepojenie na Project Nation (zmienka, cross-link, shared brand) je **out of scope pri launchi** a doplní sa v ďalšej iterácii spec-u, keď platforma získa konkrétne obrysy.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Potenciálny partner (sponzor) hodnotí príležitosť a podáva dopyt (Priority: P1)

CFO, marketing director alebo BD partner z developerskej / bankovej / poradenskej firmy alebo z automotive sektora dostane odporúčanie alebo nájde LIFO. Otvorí web na desktope, počas 30 sekúnd potrebuje pochopiť, kto LIFO organizuje, prečo by ho mal sponzorovať a aká je návratnosť (vs. ich vlastný cost interného sourcingu lokality alebo akvizícii deal flowu). Prejde na "Pre partnerov", uvidí úrovne partnerstva s benefitmi, klikne CTA a odošle dopyt s firmou, kontaktom a preferovanou úrovňou.

**Why this priority**: Partnerstvá sú primárny príjem podujatia. Bez sponzorov nie je rozpočet. Webová stránka je prvý filter — ak za prvých 30 sekúnd partner nevidí jasnú ROI argumentáciu, stráca sa.

**Independent Test**: Vystaviť homepage + sekciu Pre partnerov + funkčný kontaktný formulár; otestovať na 3-5 cieľových osobách (mimo organizačného tímu) či vedia za 30 sekúnd povedať (a) o čom LIFO je, (b) prečo by ho ich firma mala podporiť, (c) ako kontaktovať organizátorov.

**Acceptance Scenarios**:

1. **Given** návštevník je top manažér v cieľovom segmente, **When** prvýkrát otvorí homepage, **Then** do 5 sekúnd vidí názov LIFO, dátum 11. 2. 2027, miesto Hotel Clarion Bratislava, jednu vetu pozicionovania a primárne CTA "Stať sa partnerom".
2. **Given** návštevník klikne "Stať sa partnerom", **When** sa otvorí sekcia partnerstiev, **Then** vidí 3+ úrovne partnerstva s konkrétnymi benefitmi a (ak sú schválené) cenami, vrátane jedno-vetného popisu ROI vs. interný sourcing.
3. **Given** návštevník chce kontakt, **When** odošle dopytový formulár, **Then** dostane okamžite e-mailové potvrdenie a organizačný tím dostane notifikáciu s identifikovaným segmentom (Partner / Samospráva / Investor / Médiá).

---

### User Story 2 — Pozvaný starosta dokončuje platenú registráciu na webe (Priority: P1 — tied with US1)

Starosta dostane e-mailovú pozvánku z LIFO target listu (prvé kolo) alebo telefonát od call-firmy (druhé kolo). Predtým ako prizná účasť, googli si LIFO a otvorí web na overenie kredibility. Po rozhodnutí klikne v pozvánkovom e-maile odkaz s **promo / zľavovým kódom** alebo prejde na web priamo, vyberie tarifu "Samospráva", aplikuje kód, vyplní fakturačné údaje obce, zaplatí kartou alebo zvolí bankový prevod. Dostane e-mail s e-ticketom (PDF + QR kód) a faktúrou.

**Why this priority**: Toto je **primárny konverzný moment pre attendee monetizáciu**. Bez funkčného platobného toku stráca acquisition kampaň zmysel — starosta presvedčený telefónom nebude vedieť dokončiť nákup.

**Independent Test**: Vystaviť sekciu "Pre samosprávy" + ticketing modul s tarifou Samospráva + early bird cenou + možnosťou aplikovať promo kód + B2B fakturačnými údajmi; otestovať end-to-end nákup na testovacej karte + bankovom prevode. Overiť že 3 reálni starostovia (mimo organizačného tímu) dokážu kúpiť lístok do 5 minút bez asistencie.

**Acceptance Scenarios**:

1. **Given** starosta otvorí stránku z mobilu po obdržaní pozvánky, **When** prejde na "Pre samosprávy", **Then** prvá vec ktorú vidí je value proposition pre samosprávy + jasné CTA "Zaregistrovať sa za zvýhodnenú cenu" s aktuálnou Early Bird cenou.
2. **Given** starosta klikne CTA a aplikuje promo kód z pozvánkového e-mailu, **When** kód je platný, **Then** sa zobrazí konečná cena (s DPH aj bez DPH) a tarifa sa odomkne / zľava sa aplikuje.
3. **Given** starosta vyplní fakturačné údaje obce (IČO, DIČ, adresa) a zaplatí kartou, **When** platba je úspešná, **Then** dostane do 1 minúty e-mail s e-ticketom (PDF + QR) a faktúrou; transakcia sa zaeviduje pre organizačný tím.
4. **Given** starosta nemá kartu a chce platiť prevodom, **When** zvolí bankový prevod, **Then** dostane zálohovú faktúru s variabilným symbolom a info, že vstupenka sa aktivuje po pripísaní platby (manuálny alebo automatický match).
5. **Given** starosta sa pýta "prečo nie ITAPA / ZMOS", **When** prejde na FAQ, **Then** nájde priamu odpoveď s pozicionovaním LIFO.

---

### User Story 2b — Out-of-list záujemca podáva dopyt o účasť (Priority: P3)

Starosta / zástupca priemyselného parku, ktorý sa o LIFO dozvedel mimo target listu (LinkedIn, médiá, kolegovia), nemá pozvánku ani promo kód. Otvorí web, prejde na "Pre samosprávy", uvidí formulár "Mám záujem, ale nedostal som pozvánku" a podá ho. Organizačný tím manuálne posúdi a (ak schváli) pošle individuálnu pozvánku s kódom.

**Why this priority**: Otvára dvere pre nečakane silných záujemcov bez zriedenia kurátorského filtra. Bez tohto toku by sa cenná out-of-list demand stratila.

**Acceptance Scenarios**:

1. **Given** out-of-list záujemca vyplní dopyt s názvom obce a krátkou motiváciou, **When** odošle formulár, **Then** dostane potvrdenie typu "Manuálne posúdime do 5 pracovných dní" a tím dostane notifikáciu so segmentom "samospráva — out-of-list".

---

### User Story 3 — Investor / developer / banka hodnotí účasť (Priority: P2)

Senior manažér z investičnej firmy, developerskej spoločnosti alebo banky chce vedieť či LIFO doručí dealflow (nielen networking). Hľadá: line-up rečníkov, sample attendee samosprávy, formát matchmakingu, prístup k Investment Map. Prejde na "Pre investorov", uvidí value proposition, formát matchmakingu a registračný tok.

**Why this priority**: Investori sú druhá monetizačná cieľovka (cez VIP vstupy v partnerských balíkoch alebo individuálne); zároveň ich kvalita zvyšuje hodnotu eventu pre partnerov.

**Independent Test**: Vystaviť sekciu "Pre investorov" s konkrétnym popisom matchmaking formátu a sample profilov samospráv (anonymizované); otestovať či 3 ľudia zo sektora dokážu rozhodnúť GO/NO-GO.

**Acceptance Scenarios**:

1. **Given** investor hľadá deal flow, **When** otvorí "Pre investorov", **Then** vidí 1-vetný popis formátu matchmakingu (20-min stretnutia, IRL skóre, Investment Map).
2. **Given** investor sa rozhodne zúčastniť, **When** odošle prihlášku, **Then** dostane potvrdenie a info o termíne odhalenia Investment Map.

---

### User Story 4 — Novinár sťahuje press kit a kontaktuje PR (Priority: P3)

Novinár (Forbes, TREND, HN, Index, Euractiv) pripravuje článok o regionálnom rozvoji alebo PPP. Otvorí stránku, hľadá rýchle podklady. Prejde na "Pre médiá", stiahne press kit (logo, biography organizátora, kľúčové fakty, fotografie), kontaktuje PR osobu.

**Why this priority**: Mediálne pokrytie zvyšuje autoritu a kvalitu attendee i partnerov v ďalších ročníkoch. Press kit redukuje záťaž organizačného tímu odpovedaním na opakované otázky.

**Independent Test**: Vystaviť "Pre médiá" so stiahnuteľnou ZIP/PDF press kit a kontaktnou osobou; overiť že 1 reálny novinár dokáže pripraviť stub článok len z týchto materiálov.

**Acceptance Scenarios**:

1. **Given** novinár potrebuje fotografie organizátora a logo, **When** otvorí "Pre médiá", **Then** stiahne press kit jedným kliknutím (ZIP s logo SVG/PNG, biography, fakty, fotografie).

---

### User Story 5 — Potvrdený účastník kontroluje praktické info pred eventom (Priority: P3)

Účastník 2 dni pred konferenciou kontroluje praktické detaily: adresa hotela, parkovanie, MHD spojenie, kontaktná osoba pre dotazy, aktualizovaný program.

**Why this priority**: Redukuje záťaž organizačného tímu deň pred eventom, znižuje frustráciu účastníkov.

**Acceptance Scenarios**:

1. **Given** účastník potrebuje sa dostať na miesto, **When** otvorí "Miesto konania", **Then** vidí presnú adresu, mapu (embed), MHD spojenie zo Stanice Bratislava a parkovacie info.
2. **Given** účastník hľadá najnovší program, **When** otvorí "Program", **Then** vidí program s tagom "Posledná aktualizácia: DD. MM. YYYY".

---

### Edge Cases

- **Pred zverejnením rečníkov** (T-6 mesiacov pred eventom): Sekcia "Program" má placeholder content ("Line-up zverejníme priebežne — zaregistrujte sa pre upozornenie") namiesto prázdnych slotov.
- **Pomalé pripojenie** (3G na vidieku): Stránka sa musí použiteľne načítať do 3 sekúnd na 3G.
- **Screen reader používatelia**: Všetky CTA, formuláre a obrázky majú alt texty / ARIA labely.
- **Mobil v zlom svetle**: Kontrast textu musí spĺňať WCAG 2.1 AA aj pre slabozraké.
- **Sponzor odstúpi**: Logo musí byť možné odstrániť bez dev releasu (cez obsahový backend alebo jednoduché CMS).
- **Náhla zmena dátumu / miesta**: Dátum a miesto musia byť na jednom mieste obsahu, nie hardcoded na 20 miestach v kóde.
- **Návštevník bez JS**: Kontaktný formulár musí fungovať aj s vypnutým JavaScriptom (alebo aspoň zobraziť e-mail kontakt ako fallback).
- **Spamové odoslania formulára**: Mechanizmus proti botom (honeypot / rate limit / captcha).
- **Po skončení eventu**: Stránka prejde do post-event módu — galéria, video highlights, výzva na ďalší ročník. Ticketing tok sa skryje alebo prepne do "Záujem o ďalší ročník".
- **Vypredaná tarifa**: Po dosiahnutí kapacity sa tarifa zobrazí ako "Vypredané"; návštevník vidí buď inú dostupnú tarifu alebo waitlist formulár.
- **Vyčerpaný promo kód**: Keď používateľ zadá kód ktorý už dosiahol limit použití, dostane jasné chybové hlásenie a CTA na "Mám záujem" formulár pre individuálny kód.
- **Zdieľanie promo kódu mimo target listu**: Limit použití na kóde + dátumová expirácia funguje ako prirodzená bariéra. Pri podozrení (napr. kód použitý z domén úplne mimo verejnej správy) musí mať organizačný tím možnosť kód okamžite deaktivovať bez dev releasu.
- **Neúspešná platba kartou**: Používateľ dostane jasné chybové hlásenie, vstupenka sa nerezervuje, môže skúsiť znova alebo prepnúť na prevod.
- **Bankový prevod nedorazí včas**: Zálohová faktúra má jasnú splatnosť; po jej prekročení sa rezervácia uvoľní a vstupenka sa vráti do kapacity (s notifikáciou kupujúcemu).
- **B2B nákup pre tím (viac vstupeniek na jednu firmu)**: Kupujúci nakúpi N vstupeniek, neskôr potrebuje pridať / zmeniť mená jednotlivých účastníkov pred check-inom.
- **Storno**: Kupujúci žiada vrátenie peňazí — postup podľa zverejnených storno podmienok (FR-039). Tím má manuálnu kontrolu.

## Requirements *(mandatory)*

### Functional Requirements

**Identita a positioning**

- **FR-001**: Stránka MUSÍ na každej podstránke prominentne (above the fold na desktope, do prvej obrazovky na mobile) zobraziť názov "LIFO — Local Innovation Forum", dátum **11. 2. 2027** a miesto **Hotel Clarion Bratislava**.
- **FR-002**: Stránka MUSÍ na homepage do 5 sekúnd od načítania komunikovať strategickú hodnotu LIFO (kapitál ↔ samosprávy, delivery nie policy) jednou vetou.
- **FR-003**: Stránka pri launchi **NEZOBRAZUJE** prepojenie na Project Nation (platforma sa rieši po rozbehnutí LIFO). Architektúra a layout MUSIA však ponechať **rezervu** (napr. footer slot, "about" sekcia) na neskoršie pridanie zmienky / cross-linku na Project Nation bez prepisu šablóny.

**Tri cieľovkové cesty (segmented funnel)**

- **FR-004**: Stránka MUSÍ ponúkať tri jasne oddelené vstupné body z homepage: (a) **Pre partnerov**, (b) **Pre samosprávy**, (c) **Pre investorov**, každý s vlastným value proposition a CTA.
- **FR-005**: Každý zo segmentových vstupov MUSÍ obsahovať: nadpis adresovaný cieľovke, 2-3 konkrétne benefity, 1-2 case study / referenciu (Martina Grandi: JLR Nitra, Volvo Valaliky), CTA na formulár.

**Obsahové sekcie**

- **FR-006**: Stránka MUSÍ zobraziť **Program / agendu** s blokmi: Keynote, panely, workshop pre samosprávy, matchmaking blok. Pred finalizáciou rečníkov sa zobrazí placeholder s témami blokov.
- **FR-007**: Stránka MUSÍ zobraziť sekciu **Rečníci** so zoznamom potvrdených speakerov: meno, rola, organizácia, foto, krátke bio (max 60 slov). Nepotvrdených NIKDY nezobrazovať.
- **FR-008**: Stránka MUSÍ zobraziť sekciu **Pre partnerov** s úrovňami partnerstva (Generálny / Hlavný / Partner fóra alebo ekvivalent po finalizácii) — benefity a (ak schválené) ceny.
- **FR-009**: Stránka MUSÍ zobraziť **Investment Map** ako kľúčový asset (popisne, vizualizácia ukážky, gating: "plný prístup pre partnerov").
- **FR-010**: Stránka MUSÍ zobraziť sekciu **Miesto konania** (Hotel Clarion Bratislava): adresa, mapa, MHD, parkovanie, bezbariérovosť.
- **FR-011**: Stránka MUSÍ zobraziť **FAQ** s minimálne 6 otázkami pokrývajúcimi námietky z "Objection Handler" (čas, hodnota, "ďalšia konferencia?", veľkosť obce, peniaze, politická neutralita).
- **FR-012**: Stránka MUSÍ zobraziť **Pre médiá** s stiahnuteľným press kitom (logo, biography, fakty, fotografie) a kontaktom na PR osobu.
- **FR-013**: Stránka MUSÍ zobraziť **Kontakt** a **organizačný tím** (Martina Grandi ako lead).

**Konverzia a formuláre**

- **FR-014**: Stránka MUSÍ poskytnúť **dopytový formulár** s povinnou identifikáciou segmentu (Partner / Samospráva / Investor / Médiá / Iný) a podľa segmentu zobraziť relevantné polia (napr. pre samosprávy: názov obce, počet obyvateľov, hlavná výzva).
- **FR-015**: Formulár MUSÍ posielať notifikáciu organizačnému tímu (e-mail) s identifikovaným segmentom a všetkými poľami; submiter dostane okamžité potvrdenie.
- **FR-016**: Stránka MUSÍ ponúknuť **newsletter signup** s GDPR-kompatibilným súhlasom a možnosťou odhlásenia.
- **FR-017**: Všetky formuláre MUSIA mať **anti-spam mechanizmus** (honeypot, rate limit alebo captcha).

**Brand a vizuál**

- **FR-018**: Stránka MUSÍ dodržiavať **LIFO brand kit** (logo, paleta, typografia, doplnkové vizuálne prvky) tak, ako bude dodaný v separátnom brand pack-u od grafika. Pred finalizáciou brand kit-u platia **pracovné pravidlá** uvedené nižšie (FR-018a až FR-018c) ako bezpečné default-y, ktoré minimalizujú dohru pri swap-e na finálnu identitu.
  - **FR-018a**: LIFO logo (vlastné, finálne) MUSÍ byť v hlavičke každej stránky vo vektorovom formáte (SVG) so správnymi alt textami; **bez prerábania, deformácie, alebo doplnkových efektov**.
  - **FR-018b**: Pracovná paleta (do dodania finálneho brand kit-u): **tlmená inštitucionálna paleta** — tmavá primárna farba + neutrálna sekundárna (sivá / off-white) + max 1 akcentová farba (do 10 % plochy). **Bez gradientov, bez "NGO estetiky", bez zaoblených dekoratívnych fontov.**
  - **FR-018c**: Pracovná typografia (do dodania finálneho výberu): jedna **premium grotesk** rodina (napr. Inter / IBM Plex Sans / podobné moderné neutrálne písmo dostupné cez Google Fonts alebo licencované). Po dodaní LIFO brand kit-u sa swap-uje 1:1 cez CSS variable.
- **FR-019**: Implementácia MUSÍ izolovať brand tokeny (farby, fonty, radii, spacing) do **jedného centrálneho miesta** (CSS custom properties / theme tokens), aby výmena pracovných za finálne hodnoty bola **bez dotyku do markupu komponentov**.
- **FR-020**: Stránka **NEPOUŽÍVA** vizuálne prvky Project Nation brand briefu (symbol "Interlock", typografický prvok "Pillar Pivot", paleta Deep Navy + Anthracite + brass). Tieto ostávajú vyhradené pre budúcu Project Nation platformu.

**Prístupnosť a výkon**

- **FR-021**: Stránka MUSÍ spĺňať **WCAG 2.1 AA**: klávesová navigácia, alt texty, kontrast textu min 4.5:1, ARIA pre interaktívne prvky.
- **FR-022**: Stránka MUSÍ byť **mobile-first**: použiteľná a čitateľná na obrazovke od 320 px šírky.
- **FR-023**: Stránka MUSÍ načítať (LCP) do **3 sekúnd na mobilnom 3G pripojení** pre úvodnú stránku.
- **FR-024**: Stránka MUSÍ byť optimalizovaná pre vyhľadávače (sémantické HTML, meta tagy, Open Graph pre LinkedIn/Facebook, hreflang ak viacjazyčná).

**GDPR a právne**

- **FR-025**: Stránka MUSÍ obsahovať **Zásady ochrany osobných údajov** a **Cookies banner** s explicitným opt-in pre analytické / marketingové cookies.
- **FR-026**: Submission dáta z formulárov MUSIA byť uložené s identifikovanou právnou bázou (oprávnený záujem / súhlas) a retention period (max 24 mesiacov po evente, ak neexistuje iný titul).

**Obsahový workflow**

- **FR-027**: Dátum, miesto, rečníci, partneri a partnerské úrovne MUSIA byť editovateľné bez dev releasu (jednoduchý CMS, markdown súbory v repo, alebo headless CMS — rozhodnutie v `/speckit-plan`).

**Viacjazyčnosť**

- **FR-028a**: Stránka MUSÍ byť spustená vo verziách **SK** (východiskový) a **EN** (povinné minimum pri launchi). Dôvod: zahraniční rečníci (Janusz Michałek / PL, EIB, McKinsey) a nadnárodní sponzori potrebujú anglickú verziu už pri prvej návšteve.
- **FR-028b**: Obsahový model a routing MUSIA byť pripravené na **rozšírenie o ďalšie jazyky bez prepisu architektúry**: **DE, PL, IT, ES** (poradie pridania určí obchodný plán; PL prioritne kvôli rečníkovi a poľským sponzorom, DE prioritne kvôli AT/DE investorom).
- **FR-028c**: Každá jazyková verzia MUSÍ mať vlastnú URL (cesta typu `/sk/`, `/en/`, `/de/` ...) a korektné `hreflang` značky pre SEO.
- **FR-028d**: Stránka MUSÍ ponúkať jasný **prepínač jazyka** v hlavičke; voľba sa pamätá pre opakované návštevy (cookie / localStorage s GDPR-kompatibilným spracovaním).
- **FR-028e**: Ak prebieha prekladová medzera (text v jednej jazykovej verzii ešte nie je preložený do inej), stránka MUSÍ použiť definovanú **fallback stratégiu** (napr. zobrazí EN obsah s vizuálnym indikátorom "Translation pending"), nie zlomenú stránku ani prázdny blok.

**Acquisition a paid registration model**

- **FR-029a**: **Acquisition** pre samosprávy prebieha **mimo webu**: (1) e-mailová pozvánka z target listu, (2) follow-up telefonát od externej call-firmy. Po dohode starosta prejde na web a **dokončí platenú registráciu**. Pre investorov, biznis a ostatných môže byť acquisition kombinácia outreachu a samodopytu cez web.
- **FR-029b**: Sekcia "Pre samosprávy" MUSÍ slúžiť ako **kredibilitný materiál** pred konverziou — keď starosta dostane pozvánku a googli si LIFO predtým ako odpovie / zaplatí, na webe musí nájsť: kto organizuje (Martina Grandi, track record JLR/Volvo), kto z partnerov je zapojený, aký konkrétny výstup si odnesie, akí ďalší starostovia / investori prídu.
- **FR-029c**: Stránka MUSÍ ponúknuť **sekundárny "Mám záujem, ale nedostal som pozvánku"** formulár pre out-of-list záujemcov. Submission ide do toho istého pipelinu ako ostatné dopyty (s tagom segmentu).

### Ticketing a pricing (PAID model — všetci účastníci platia)

- **FR-030**: Stránka MUSÍ poskytnúť **online ticketing tok** end-to-end: výber tarify → vyplnenie údajov účastníka (meno, organizácia, e-mail, telefón, fakturačné údaje) → platba → potvrdenie + e-ticket + faktúra/zálohová.
- **FR-031**: Stránka MUSÍ podporovať **viacúrovňové cenové tarify pre účastníkov** (oddelené od sponzorských tier z FR-008). Štandardne minimálne: (a) **Samospráva**, (b) **Investor / Business**, (c) **VIP** — finálny počet a názvy v plán fáze. Každá tarifa má vlastnú cenu (možno aj zľavnenú voči konkurenčným eventom typu ITAPA).
- **FR-032**: Stránka MUSÍ podporovať **early bird mechanizmus**: každá tarifa má minimálne dve fázy ceny — **Early Bird** (do dátumu D1) a **Regular** (od D1+1 do D2 alebo do vypredania). Roadmapa: príprava na "Last Minute" / "On-site" tarifu pre ďalšie ročníky.
- **FR-033**: Cena MUSÍ byť na stránke zobrazená s **dátumom skončenia aktuálnej fázy** (countdown alebo dátum), aby early bird motivácia bola viditeľná. Po prechode na ďalšiu fázu sa zobrazí nová cena bez dev releasu.
- **FR-034**: Stránka MUSÍ podporovať **kapacitné limity per tarifa**: keď je tarifa vypredaná, zobrazí sa stav "Vypredané" a kupujúci je presmerovaný na inú dostupnú tarifu alebo waitlist.
- **FR-035**: Stránka MUSÍ vystaviť **faktúru** (alebo zálohovú faktúru / proforma) s povinnými náležitosťami podľa slovenských daňových predpisov (IČO, DIČ, IČ DPH ak je platiteľ, sadzba DPH, dátum dodania, splatnosť). Faktúra sa doručuje e-mailom kupujúcemu okamžite po platbe.
- **FR-036**: Stránka MUSÍ podporovať **B2B faktúru na firmu / obec / inštitúciu** (povinné polia: IČO, DIČ, IČ DPH, adresa sídla, registrácia) a B2C faktúru na fyzickú osobu (povinné polia: meno, adresa).
- **FR-037**: Stránka MUSÍ podporovať **platbu kartou** (Visa / Mastercard) cez 3-D Secure platobnú bránu. Voliteľne: **bankový prevod** s vygenerovanou zálohovou faktúrou (vstupenka sa aktivuje po pripísaní platby).
- **FR-038**: Stránka MUSÍ poslať **e-ticket** (PDF s menom, tarifou, QR alebo unikátnym kódom pre check-in) na e-mail kupujúceho po úspešnej platbe. Pri B2B nákupe pre viac účastníkov MUSÍ kupujúci vedieť pridať mená účastníkov pred check-inom.
- **FR-039**: Stránka MUSÍ mať publikované **storno podmienky** (refund policy) pred dokončením nákupu a vyžadovať explicitný súhlas s nimi.
- **FR-040**: Všetky ceny MUSIA byť zobrazené **s DPH aj bez DPH** (B2B kupujúci si potrebuje overiť netto cenu pre rozpočet).
- **FR-041**: Stránka MUSÍ podporovať **promo / zľavové kódy** ako primárny gating mechanizmus pre tarifu "Samospráva":
  - **FR-041a**: Tarifa "Samospráva" je **štandardne skrytá** v ticketing UI. Stane sa viditeľnou (alebo sa aplikuje zľava) len po zadaní platného promo kódu.
  - **FR-041b**: Promo kód MUSÍ mať konfigurovateľné atribúty: (1) **limit počtu použití** (napr. 200×), (2) **dátum platnosti od/do**, (3) **typ zľavy** (% zľava, fixná suma, alebo "odomknúť skrytú tarifu za nastavenú cenu"), (4) **viazanie na konkrétnu tarifu** (kód `LIFO27-SAMOSPRAVA` odomyká len túto tarifu).
  - **FR-041c**: Po vyčerpaní limitu sa kód deaktivuje a používateľovi sa zobrazí chyba "Kód už nie je platný — kontaktujte nás".
  - **FR-041d**: Pre out-of-list záujemcov (cez "Mám záujem" formulár) MUSÍ byť možné vystaviť **individuálny one-time kód** s limitom 1 použitie a krátkou platnosťou (napr. 7 dní).
  - **FR-041e**: Verejné tarify (Investor / Business / VIP) **NIE SÚ** gated — kúpiť ich môže ktokoľvek za uvedenú cenu. Gating sa týka len tarify "Samospráva" (a budúcich potenciálnych zvýhodnených tarif).

### Key Entities

- **Visitor**: Anonymný používateľ stránky. Segmentuje sa pri prvej interakcii (homepage CTA, formulár). Atribúty: segment (Partner / Samospráva / Investor / Médiá / Iný), zdroj návštevy (UTM), zariadenie.
- **Inquiry**: Odoslanie kontaktného formulára. Atribúty: segment, meno, e-mail, telefón, organizácia, segmentovo-špecifické polia, správa, časová pečiatka, zdrojová stránka, GDPR súhlas.
- **Speaker**: Potvrdený rečník. Atribúty: meno, rola, organizácia, bio (krátke), foto, priradenie k programovému bloku, sociálne odkazy, poradie zobrazenia.
- **Program Block**: Časť agendy. Atribúty: názov, typ (keynote / panel / workshop / matchmaking), čas začiatok–koniec, opis, priradení rečníci.
- **Partner**: Sponzor / partner. Atribúty: organizácia, úroveň, logo, link, poradie zobrazenia, status (potvrdený / pending — zobrazujú sa len potvrdení).
- **Partnership Tier**: Úroveň partnerstva. Atribúty: názov, krátky popis, zoznam benefitov, cena (ak verejná), počet dostupných miest, poradie.
- **Page Content Block**: Editovateľný textový blok pre sekcie (homepage hero, FAQ položky, Investment Map popis, atď.). Umožňuje úpravy bez dev releasu.
- **Newsletter Subscriber**: E-mail prihlásený k odberu. Atribúty: e-mail, dátum prihlásenia, segment (ak vybraný), GDPR súhlas, opt-out token.
- **Ticket Tier**: Cenová tarifa pre účastníkov. Atribúty: názov (Samospráva / Investor / Business / VIP), poradie zobrazenia, kapacita, počet dostupných miest, **viditeľnosť** (verejná / gated), zoznam fáz s cenou (Early Bird / Regular).
- **Pricing Phase**: Časové okno pre cenu tarify. Atribúty: tarifa, názov fázy (Early Bird / Regular / Last Minute), dátum začiatok–koniec, cena bez DPH, cena s DPH, mena.
- **Promo Code**: Kód uplatniteľný v pokladni. Atribúty: kód, typ (% / fixná / unlock), hodnota, viazanie na konkrétnu tarifu (ak je), limit použití, počet použití, dátum platnosti od/do, status (aktívny / vyčerpaný / expirovaný).
- **Order**: Nákupná transakcia. Atribúty: tarifa(y), počet ks, kupujúci (B2B/B2C), fakturačné údaje, použitý promo kód, hrubá / netto suma, DPH, stav platby (pending / paid / failed / refunded), metóda platby (karta / prevod), časová pečiatka.
- **Attendee**: Konkrétny účastník priradený k vstupenke. Atribúty: meno, organizácia, e-mail, telefón, segment, priradenie k Order, unikátny check-in kód (QR), status (potvrdený / neprihlásený / na waitliste).
- **Invoice**: Účtovný doklad. Atribúty: číslo faktúry, kupujúci (IČO, DIČ, IČ DPH, adresa), dodávateľ (organizátor), položky, suma s DPH, suma bez DPH, sadzba DPH, dátum vystavenia, splatnosť, variabilný symbol, stav (vystavená / uhradená).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Návštevník v cieľovom segmente dokáže do **30 sekúnd** od načítania homepage odpovedať na otázky (a) "Čo je LIFO?", (b) "Pre koho je?", (c) "Čo z toho budem mať?" — overené 5-second testom na minimálne 5 osobách z každého segmentu.
- **SC-002**: Stránka načíta úvodný obsah (LCP) **pod 3 sekundy** na simulovanom 3G mobilnom pripojení.
- **SC-003**: **100 %** verejných stránok prejde automatizovaným WCAG 2.1 AA auditom bez kritických chýb (kontrast, alt texty, klávesová navigácia).
- **SC-004**: Minimálne **80 %** prichádzajúcich dopytov má jednoznačne identifikovaný segment v okamihu doručenia organizačnému tímu (eliminuje manuálne triedenie).
- **SC-005**: Stránka dosiahne pozíciu **#1–3** vo vyhľadávači pre dotazy "LIFO konferencia 2027", "Local Innovation Forum Slovensko" do 60 dní od spustenia.
- **SC-006**: Do dňa konferencie web vygeneruje minimálne **N kvalifikovaných partnerských dopytov** vedúcich k podpísaným partnerstvám (N stanoví obchodný cieľ v Plán fáze; benchmark: 3× počet skutočne potrebných partnerov).
- **SC-007**: **Press kit stiahne minimálne 10 unikátnych mediálnych domén** do dňa konferencie.
- **SC-008**: Organizačný tím dokáže **aktualizovať obsah** (nový rečník, nová sekcia FAQ, posun času) za **menej ako 30 minút** bez zásahu vývojára.
- **SC-009**: **Zero kritických chýb v produkcii** počas 2 týždňov pred konferenciou (najkritickejší okamih obratu).
- **SC-010**: Bounce rate na homepage pod **55 %** (B2B konferenčný benchmark) v období 60 dní pred eventom.
- **SC-011**: **Funnel konverzia "klik z pozvánky → zaplatená vstupenka"** dosiahne minimálne **40 %** pri pozvaných samosprávach (benchmark pre dobre nasmerovaný B2B outreach po telefonickom follow-upe).
- **SC-012**: **Drop-off na checkoute** (pridal lístok do košíka, ale nezaplatil) pod **30 %** — overuje použiteľnosť ticketing toku.
- **SC-013**: **Priemerný čas dokončenia nákupu** (od kliknutia "Zaregistrovať sa" po doručenie e-ticketu) **pod 5 minút** pre kartovú platbu.
- **SC-014**: **Zero kritických platobných incidentov** (failed charge bez chybového hlásenia, duplicitné účtovanie, e-ticket nedoručený) počas celého predajného obdobia.
- **SC-015**: **100 % vystavených faktúr spĺňa slovenské daňové náležitosti** — overené účtovníkom pri prvom plnení a následnou kontrolou každú vystavenú dávku.

## Assumptions

- **Primárny účel**: Web je **pre-event** marketing + lead-gen + registrácia. Live event-day funkcie (livestream, in-app networking, real-time agenda) sú **out of scope pre v1**; ak vzniknú, riešia sa samostatnou špecifikáciou.
- **Post-event mód**: Po konferencii sa web prepne do post-event módu (galéria, video, výzva na ďalší ročník). Toto je **v scope pre v1** ako jednoduchá obsahová zmena, nie samostatná aplikácia.
- **Confirmed facts**: Názov "LIFO — Local Innovation Forum", dátum 11. 2. 2027 a miesto Hotel Clarion Bratislava sú **finálne** podľa potvrdenia od zadávateľky (Martina Grandi). Tieto budú v copy hardcoded ako fakt.
- **Draft content**: Materiály v `podklady/` (program, rečníci, ceny partnerstva, biznis model) sú **návrhy**, finalizujú sa priebežne; obsahový model musí umožniť ich aktualizáciu bez dev releasu.
- **Brand**: LIFO má **vlastné logo** (dodá zadávateľka). Kompletný brand kit (paleta, typografia, doplnkové prvky) sa dotvára paralelne s vývojom webu; do dodania platia pracovné default-y z FR-018b/c, ktoré sa swapnú cez CSS tokeny.
- **Audience velikosti**: Očakávaný počet účastníkov na evente cca 150 zástupcov samospráv + investori + speakri + partneri ≈ **200–250 osôb** pre ročník 2027. Web musí zvládať návštevnosť rádovo **stovky až nízke tisícky unikátnych návštevníkov mesačne** v období pred eventom; nie je to viral-traffic site.
- **Plán rastu**: LIFO je plánovaný **ako škálovateľný flagship event** s ambíciou rozšírenia v ďalších ročníkoch (geograficky aj objemovo) a dlhodobo ako vstupný bod do platformy Project Nation (viď Context Summary). Webová architektúra a obsahový model musia umožniť rast bez prepisu — najmä cez (a) viacjazyčnosť, (b) editovateľný obsah, (c) odolnosť voči zmenám značky a programového formátu, (d) možnosť neskoršieho cross-linku na Project Nation bez refaktoringu.
- **Viacjazyčnosť pri launchi**: Spúšťame **SK + EN**. Roadmapa: **DE, PL, IT, ES** v poradí podľa obchodnej priority (PL prioritne kvôli rečníkovi Janusz Michałek + poľským investorom, DE kvôli AT/DE kapitálu). Architektúra musí byť i18n-ready od prvého dňa; ďalšie jazyky pribúdajú ako obsahové releasy, nie ako tech refaktor.
- **Hosting a doména**: LIFO web žije na **`lifo.urbanlama.eu`** — subdoména existujúcej `urbanlama.eu` (zadávateľkina materská doména na Webglobe DNS). App hosting na **Netlify** (CDN-fronted, serverless funkcie pre formuláre + Stripe webhook); Webglobe slúži ako DNS broker (CNAME `lifo` → Netlify). HTTPS automaticky cez Let's Encrypt na Netlify. Pre budúce ročníky možnosť pridať dedicated doménu (`lifoforum.sk` a podobné) je open.
- **Formuláre**: Formulárové submissions sa primárne **doručujú e-mailom** organizačnému tímu. Plnohodnotná CRM integrácia (HubSpot, Salesforce) je **out of scope** pre v1, ale dátová štruktúra musí umožniť budúci export.
- **Analytika**: Štandardná webová analytika (GA4 alebo Plausible — GDPR-friendly varianta odporúčaná) je v scope; hlbšia attribution modeling je out of scope.
- **Platba**: Web **prijíma platby online** v rozsahu definovanom FR-030 až FR-041 — kartové platby cez 3-D Secure platobnú bránu a voliteľne bankový prevod so zálohovou faktúrou. Konkrétny poskytovateľ platobnej brány (napr. Stripe / GP webpay / Trust Pay / Besteron) sa vyberie v plán fáze; výber musí podporovať B2B fakturáciu na slovenský trh a multi-currency, ak vyžadované pre zahraničných sponzorov/investorov. **Partnerstvá (sponzoring)** sa NAĎALEJ fakturujú offline (mimo webu) — sponzori sú low-volume, high-touch.
- **Bezpečnosť**: Štandardné HTTPS, HSTS, secure cookies, bot mitigation cez hosting platformu. Žiadne citlivé osobné údaje (rodné čísla, finančné dáta) sa nezbierajú.
- **Záväzný brand kit**: V prípade konfliktu medzi touto špecifikáciou a **finálnym LIFO brand kit-om** (logo, paleta, typografia, supergraphic) — brand kit má prednosť v otázkach vizuálu a vyžaduje sa formálna výnimka. Pôvodný `Project_Nation_STRATEGIC_BRAND_BRIEF.txt` v `podklady/` platí len pre budúcu Project Nation platformu, **nie pre LIFO**.

## Reference (Visual & Structural Inspiration)

Pre štruktúru a "feeling" stránky slúžia ako referencia konferenčné weby od Blue Events (CZ), konkrétne:

- **[lidskykapital.cz](https://www.lidskykapital.cz/)** — B2B HR konferencia, jednoduchý single-page koncept: hero (dátum + miesto + téma ročníka + tri CTA), o konferencii, partneri, foto galéria, ohlasy v médiách, kontakt.
- **[retailindetail.cz](https://www.retailindetail.cz/)** — sesterský event, **rovnaká šablóna** (potvrdené zadávateľkou). *(WebFetch zablokovaný 403 — pri ďalšej iterácii spec-u verifikovať manuálne, ak treba.)*

**Princípy, ktoré z referencií preberáme**:
- Jednoduchá single-page navigácia (5–6 položiek), nie hlboká hierarchia podstránok.
- Hero komunikuje fakt (dátum + miesto + ročníková téma) okamžite, bez "agency-speak".
- Sekcie sa otvárajú postupne ako sa blíži event — pri launchi nemusí byť kompletný program a zoznam rečníkov; placeholder/teaser obsah je akceptovateľný.
- Vzdušný, fotograficky bohatý layout. Hustý text len v cielenej sekcii (FAQ, ohlasy).

**Odchýlky pre LIFO** (oproti referencii):
- **Brand**: LIFO má vlastné logo a vlastný (priebežne dokončovaný) brand kit; referenčné weby používajú vlastnú farebnosť, ktorá pre LIFO neplatí.
- **Ceny sú viditeľné** v ticketingu, vrátane Early Bird countdownu — referencie ceny väčšinou neukazujú.
- **Prvý ročník = žiadne foto z minulého ročníka**. Sekciu "Galéria" nahrádza sekcia **"Kto za LIFO stojí"** (Martina Grandi track record: JLR Nitra 450+ ha, Volvo Valaliky 380+ ha, 30+ samospráv).
- **Viacjazyčnosť**: LIFO ide SK + EN pri launchi + roadmapa DE/PL/IT/ES; referencie sú jednojazyčné.
