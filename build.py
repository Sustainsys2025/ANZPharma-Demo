#!/usr/bin/env python3
"""Rebuilds the four HTML pages next to this script. Run: python3 build.py
Edit BRANDS / RETAILERS / page copy below; styles live in css/styles.css, behaviour in js/main.js."""
import os, html, json, urllib.parse

OUT = os.path.dirname(os.path.abspath(__file__))
LIVE = "https://www.anzpharma.co.nz"
UP = "https://brand.anzpharma.co.nz/uploads/"
e = html.escape


def live(path):
    return LIVE + urllib.parse.quote(path)


RETAILERS = [
    ("Chemist Warehouse", "chemistwarehouse.jpg"), ("Green Cross Health", "greencross.jpg"),
    ("Woolworths", "woolworths.png"), ("Foodstuffs NZ", "foodstuffs.jpg"),
    ("The Warehouse", "thewarehouse.jpg"), ("Farmers", "farmers.jpg"),
    ("Kmart", "k mart logo .png"), ("Bargain Chemist", "bargain chemist.png"),
    ("Countdown Pharmacy", "countdown-pharmacy.jpg"), ("Pharmacy Direct", "pharmacy-direct.jpg"),
    ("Health 2000", "health2000.jpg"), ("CDC Pharmaceuticals", "cdc.png"),
    ("Baby Bunting", "baby bunting .png"), ("Baby on the Move", "babyonthemove.jpg"),
    ("Commonsense Organics", "commonsense-organic.jpg"), ("Farmlands", "farmland logo.png"),
    ("Spotlight", "spotlight .png"), ("Postie", "postie.jpg"),
    ("Night ’n Day", "nightnday.jpg"), ("Lagardère Travel Retail", "ls-travel.jpg"),
]

CATS = [
    ("baby", "Baby and family"), ("oral", "Oral care"), ("skin", "Skin and personal care"),
    ("health", "Health and wellness"), ("food", "Food and drink"), ("home", "Home and lifestyle"),
]
CATNAME = dict(CATS)

# slug, name, category, type, fact chip, short line, about, hero, logo, gallery
BRANDS = [
    ("carmex", "Carmex", "skin", "Lip care", "Since 1937",
     "The classic lip balm, in a jar, tube or stick.",
     "Carmex began in 1937, when Alfred Woelbing made lip balm in his kitchen to soothe his own chapped lips. One trusted formula in three formats has kept a loyal following ever since. ANZ Pharma is the official Carmex distributor in New Zealand.",
     "hero_411775523725.png", "511773348361.png", ["271775523766.png", "981775523757.png", "821775523739.png"]),
    ("fiji-water", "Fiji Water", "food", "Bottled water", "Since 1996",
     "Artesian water drawn from an ancient aquifer in Fiji.",
     "Fiji Water has bottled water from a sustainable artesian aquifer in Fiji since 1996, and invests in the environment and local communities where it operates.",
     "hero_911793245798.png", "961793245639.png", ["811793245911.png", "551793245832.png", "961793245822.png"]),
    ("first-light-natural-health", "First Light Natural Health", "health", "Natural health", "Plant-powered",
     "Gentle natural remedies for everyday emotional support.",
     "First Light makes plant-based emotional remedies for stress, overwhelm and the ups and downs of family life, with a holistic approach to balance and calm. ANZ Pharma is the official distributor in New Zealand.",
     "hero_751775529549.png", "221727736343.png", ["171775529585.png", "371775529571.png", "711775529562.png"]),
    ("four-seasons", "Four Seasons", "skin", "Sexual health", "Australian, since 1984",
     "Condoms, lubricants and gels in a wide range of sizes and styles.",
     "Australian owned since 1984, Four Seasons was first to offer condoms in a range of sizes. The line covers ultra-thin, textured and flavoured styles plus lubricants and gels, and the brand actively supports safe-sex education.",
     "hero_371775525160.png", "181679461291.jpg", ["221679461292.jpg", "931679461292.jpg", "691679461292.jpg"]),
    ("george-edi-fragrance", "George & Edi", "home", "Home fragrance", "Made in NZ",
     "Small-batch scents and candles, crafted in New Zealand.",
     "Sisters Sarah and Rose founded George & Edi in Wānaka in 2011, starting with candles sold at local markets. The range is made in New Zealand with natural ingredients: affordable luxury for every day. ANZ Pharma is the official distributor in New Zealand.",
     "hero_881775692651.png", "191775692651.png", ["421775692673.png", "481775692663.png", "951775692651.png"]),
    ("glucology-ibd-medical", "Glucology", "health", "Diabetes care", "350,000+ users",
     "Practical, discreet everyday products for people living with diabetes.",
     "Created by IBD Medical, Glucology makes affordable support products that make daily and on-the-go diabetes management easier, starting with its copper-based Diacare socks. More than 350,000 people use the range.",
     "hero_911782354455.png", "731734410360.png", ["401782354139.jpg", "361782354129.jpg", "711782354116.png"]),
    ("jack-n-jill", "Jack N’ Jill", "baby", "Kids oral and personal care", "Sold in 60+ countries",
     "Safer oral and personal care made for babies and kids.",
     "A much-loved Australian name from the 1940s, revived by Melbourne couple Rachel and Justin Bernhaut after they went looking for safer products for their newborn. Fifteen years on, the range has grown past 100 products.",
     "hero_721775709485.png", "131775708464.png", ["201775709512.png", "601775709494.png", "241775709485.png"]),
    ("justines", "Justine’s", "food", "Protein baked goods", "Baked in Wellington",
     "Protein-rich cookies and treats, baked fresh every day.",
     "Founded in 2005, Justine’s bakes its protein-rich range daily at its Wellington factory and supplies more than 1,500 retailers in New Zealand and overseas.",
     "hero_951775525321.png", "641638233474.png", ["791775525945.png", "541775525706.png", "751775525696.png"]),
    ("kolorex", "Kolorex", "health", "Skin and gut care", "NZ horopito",
     "Intimate care, skin and gut products powered by native horopito.",
     "Kolorex is built on horopito, a native New Zealand herb with natural antifungal properties. Nearly 30 years of research into growing and extracting it underpin the intimate care, derma and gut care ranges.",
     "hero_621775528438.png", "411716344920.png", ["691775528455.png", "781775528446.png", "641775528438.png"]),
    ("little-genie", "Little Genie", "baby", "Eco baby care", "An ANZ Pharma brand",
     "Biodegradable nappy pants, wipes and nursing pads.",
     "Started by two eco-conscious New Zealand dads, Little Genie makes baby products that are kind to babies and to the environment. The brand is now owned by ANZ Pharma.",
     "hero_671773180424.png", "991773180424.png", ["201773180424.png", "961773180425.png", "311773180425.png"]),
    ("melrose", "Melrose", "health", "Health foods and supplements", "100+ products",
     "Australian natural foods, oils and supplements for daily use.",
     "Family-owned Melrose Health works to a food-is-medicine philosophy, with more than 100 core products across vitamins, nutrient blends, omegas, cooking oils and personal care.",
     "hero_211775527978.png", "231661808443.png", ["811775528001.png", "811775527989.png", "461775527978.png"]),
    ("mineralyte", "Mineralyte", "health", "Hydration", "Australian made",
     "Rapid hydration with 21 electrolytes and minerals, and no sugar.",
     "Mineralyte Hydrate+ is made in Australia from locally sourced ingredients, with 21 electrolytes, minerals and trace elements and no sugar, sweeteners, preservatives or colours. ANZ Pharma is the official distributor in New Zealand.",
     "hero_341775532894.png", "801744784710.png", ["961775533053.png", "271775533043.png", "481775533034.png"]),
    ("mustela", "Mustela", "baby", "Baby skincare", "75+ years",
     "Natural-origin skincare that is safe from birth.",
     "Mustela brings more than 75 years of baby-skin expertise to skincare formulated for normal, dry, very sensitive and eczema-prone skin. ANZ Pharma is the official distributor in New Zealand.",
     "hero_331775526187.png", "251772756858.png", ["611772756877.jpg", "921772756870.jpg", "731772756858.jpg"]),
    ("piranha", "Piranha", "food", "Snacks", "Australian made",
     "Bold snack foods made with natural ingredients.",
     "Piranha is 100% Australian owned and manufactured. Its snacks are cooked in sunflower oil with no artificial colours, preservatives or added MSG, and the range includes gluten-free and vegan options.",
     "hero_381775515564.png", "181635986114.jpg", []),
    ("skin-control", "Skin Control", "skin", "Skincare", "Since 2018",
     "Affordable, vegan-friendly skincare, best known for pimple patches.",
     "Skin Control launched in Australia in 2018 to give teens and adults with acne-prone skin an affordable alternative. Its pimple patches became a cult favourite. ANZ Pharma is the official distributor in New Zealand.",
     "hero_191775527556.png", "821721190728.png", ["651775527577.png", "651775527567.png", "691775527556.png"]),
    ("soap2go", "soap2GO", "skin", "Hand sanitiser", "Since 2007",
     "The travel-friendly hand sanitiser found in airports and pharmacies.",
     "Developed in 2007 for travellers, carers and parents, soap2GO is stocked in airports across Australia and New Zealand, in pharmacies and in travel retail.",
     "hero_701775512555.jpg", "221637633615.png", ["171775513253.png", "801775513103.jpg", "521775513092.jpg"]),
    ("tepe", "TePe", "oral", "Oral hygiene", "Since 1965",
     "Toothbrushes, interdental brushes, tongue cleaners and floss.",
     "Founded in 1965, TePe designs oral hygiene products to help people look after their teeth and gums, and tests every product for quality and effectiveness.",
     "hero_701780635705.png", "761776404784.png", []),
    ("waterdrop", "Waterdrop", "food", "Drink flavouring", "Sugar-free",
     "Small cubes that turn plain water into a fruity drink.",
     "A Waterdrop Microdrink is a sugar-free cube of fruit and plant extracts that dissolves in still or sparkling water. The idea dates from 2016 and aims to help people drink more water without pre-filled bottles.",
     "hero_411775533271.png", "921756385273.png", ["701756434586.jpg", "151756434573.jpg", "601756434556.jpg"]),
    ("waterwipes", "WaterWipes", "baby", "Baby wipes", "99.9% water",
     "Baby wipes made from purified water and a drop of fruit extract.",
     "WaterWipes contain just two ingredients, 99.9% purified water and a drop of fruit extract, so they suit newborns and the most sensitive skin. The wipes are large, soft and strong.",
     "hero_671781495614.png", "721781731890.png", ["631781731928.jpg", "621781731912.png", "701781731902.jpg"]),
    ("white-glo", "White Glo", "oral", "Teeth whitening", "Australian",
     "Whitening oral care that is safe to use every day.",
     "White Glo is an Australian teeth-whitening brand with decades of experience. Its products are made for daily use and to meet the requirements of Australian dentists.",
     "hero_181775103220.jpg", "461775103220.png", ["511775103256.jpg", "741775103242.jpg", "601775103222.jpg"]),
]
B = {b[0]: b for b in BRANDS}
SHOWCASE = ["waterwipes", "carmex", "mustela", "white-glo", "fiji-water", "kolorex"]

SERVICES = [
    ("freight", "Freight", "We collect at source and bring your stock to our door.",
     ["Forwarding and shipment coordination", "Collection at source", "Freight and shipping", "Delivery to the ANZ Pharma distribution centre"]),
    ("warehouse", "Warehouse", "7,800 sqm in East Tamaki, with room for 14,000 pallets.",
     ["Own and customer warehousing", "Direct-store-delivery and DC distribution", "Wholesale operations and B2B fulfilment", "Regulatory support and quality controls"]),
    ("sales", "Sales and service", "A field team that gets brands ranged and keeps them selling.",
     ["Field sales management", "Key account management", "Customer management", "Customer services"]),
]

CAPS = ["Nationwide retail distribution network", "Integrated import and freight coordination", "ATF-approved transitional facility support", "B2B and retail fulfilment", "Direct-store-delivery and DC distribution", "Regulatory support and quality controls", "Field sales and key account management", "Scalable logistics for growing brands"]


def img(src, alt, cls="", lazy=True):
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy"' if lazy else ""
    return f'<img{c} src="{src}" alt="{e(alt)}"{l} onerror="imgFail(this)">'


def page(fname, title, desc, body, active, extra=""):
    def nav(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    doc = f"""<!doctype html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=Rubik:wght@400;500;600&display=swap">
<link rel="stylesheet" href="css/styles.css">
<script>function imgFail(i){{var s=document.createElement('span');s.className='img-fallback '+i.className;s.textContent=i.alt;i.replaceWith(s)}}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
<div class="announce">Now wholesale-only. <span>Retail customers: our new online store is launching soon.</span></div>
<div class="wrap bar">
<a class="logo" href="index.html" aria-label="ANZ Pharma home"><img src="{live('/images/anzpharma-logo.svg')}" alt="ANZ Pharma" width="181" height="20" onerror="this.replaceWith(Object.assign(document.createElement('span'),{{className:'wordmark',innerHTML:'<b>ANZ</b>PHARMA'}}))"></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<nav id="nav" aria-label="Main">
{nav('brands.html', 'Brands', 'brands')}
{nav('index.html#services', 'Services', 'services')}
{nav('about.html', 'About', 'about')}
{nav('partner.html', 'Contact', 'partner')}
<a href="https://wholesale.anzpharma.co.nz/login.php" class="signin">Wholesale sign in</a>
<a href="partner.html" class="btn btn-dark">Become a partner</a>
</nav>
</div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
<div class="wrap">
<div class="foot-grid">
<div><div class="wordmark light"><b>ANZ</b>PHARMA</div>
<p>ANZPharma Wholesalers Ltd<br>27E Smales Road, East Tamaki,<br>Auckland 2013, New Zealand</p>
<p><a href="tel:+6495712550">+64 9 571 2550</a><br><a href="mailto:sales@anzpharma.co.nz">sales@anzpharma.co.nz</a></p></div>
<div><h2>Information</h2><ul>
<li><a href="partner.html">Wholesale registration</a></li>
<li><a href="https://app.smartsheet.com/b/form/b973d35e5c6442339b9a19ecd824c3bc">Credit claim</a></li>
<li><a href="{LIVE}/privacy-policy/">Privacy policy</a></li>
<li><a href="{LIVE}/terms-conditions/">Terms and conditions</a></li>
<li><a href="{LIVE}/disclaimer/">Disclaimer</a></li></ul></div>
<div><h2>Shop by category</h2><ul>
{"".join(f'<li><a href="brands.html#{k}">{e(n)}</a></li>' for k, n in CATS)}</ul></div>
<div><h2>Follow us</h2><ul>
<li><a href="https://www.facebook.com/ANZPharmaNZ/">Facebook</a></li>
<li><a href="https://www.instagram.com/anzpharma/">Instagram</a></li>
<li><a href="https://nz.linkedin.com/in/anz-pharma-027b20361">LinkedIn</a></li>
<li><a href="https://www.tiktok.com/@anzpharmanz">TikTok</a></li></ul></div>
</div>
<div class="foot-base"><span>&copy; 2026 ANZPharma Wholesalers Ltd. All rights reserved.</span><span>Quality brands. Trusted partners. Reliable supply.</span></div>
</div>
</footer>
{extra}
<script src="js/main.js"></script>
</body>
</html>
"""
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(doc)


def retailer_items():
    return "".join(f'<li>{img(live("/images/customers/" + f), n)}</li>' for n, f in RETAILERS)


# ---------- HOME ----------
slides = "".join(
    f'<a class="slide c-{B[s][2]}{" on" if i == 0 else ""}" href="brands.html#{s}" data-i="{i}">'
    f'{img(UP + B[s][7], B[s][1] + " products", "slide-img", lazy=i > 0)}'
    f'<span class="slide-cap"><span class="slide-logo">{img(UP + B[s][8], B[s][1] + " logo", lazy=i > 0)}</span>'
    f'<span><b>{e(B[s][1])}</b><small>{e(B[s][3])}</small></span></span></a>'
    for i, s in enumerate(SHOWCASE))
dots = "".join(f'<button type="button" class="dot{" on" if i == 0 else ""}" data-i="{i}" aria-label="Show {e(B[s][1])}"></button>' for i, s in enumerate(SHOWCASE))

cat_tiles = "".join(
    f'<a class="cat c-{k}" href="brands.html#{k}"><span class="cat-n">{sum(1 for b in BRANDS if b[2] == k)}</span>'
    f'<span class="cat-name">{e(n)}</span><span class="cat-brands">{e(", ".join(b[1] for b in BRANDS if b[2] == k))}</span></a>'
    for k, n in CATS)

wall = "".join(
    f'<a class="wall-tile c-{b[2]}" href="brands.html#{b[0]}" title="{e(b[1])}">{img(UP + b[8], b[1])}<span>{e(b[3])}</span></a>'
    for b in BRANDS)

svc_tabs = "".join(
    f'<button type="button" role="tab" class="jtab" id="jt-{k}" aria-controls="jp-{k}" aria-selected="{"true" if i == 0 else "false"}"><span class="jnum">{i + 1}</span>{e(n)}</button>'
    for i, (k, n, _, _) in enumerate(SERVICES))
svc_panels = "".join(
    f'<div role="tabpanel" class="jpanel" id="jp-{k}" aria-labelledby="jt-{k}"{"" if i == 0 else " hidden"}><p class="jlead">{e(lead)}</p><ul>'
    + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul></div>"
    for i, (k, n, lead, items) in enumerate(SERVICES))

home = f"""
<section class="hero"><div class="wrap hero-grid">
<div class="hero-copy">
<h1>The brands New Zealand reaches for, <mark>on your shelf.</mark></h1>
<p class="lead">ANZ Pharma markets and distributes 100+ healthcare and everyday brands to pharmacies, supermarkets and retailers across New Zealand and the Pacific.</p>
<div class="row"><a class="btn btn-dark" href="partner.html">Become a partner</a><a class="btn btn-line" href="brands.html">Browse our brands</a></div>
<dl class="hero-stats"><div><dt data-count="100" data-suffix="+">100+</dt><dd>brands</dd></div><div><dt data-count="7800">7,800</dt><dd>sqm warehouse</dd></div><div><dt data-count="14000">14,000</dt><dd>pallet spaces</dd></div></dl>
</div>
<div class="showcase" aria-roledescription="carousel" aria-label="Featured brands">
<div class="slides">{slides}</div>
<div class="show-ctl"><button type="button" class="arrow" data-dir="-1" aria-label="Previous brand">&#8592;</button><div class="dots">{dots}</div><button type="button" class="arrow" data-dir="1" aria-label="Next brand">&#8594;</button></div>
</div>
</div></section>

<section class="marquee-band" aria-label="Retail partners">
<p class="wrap marquee-label">On the shelf at 20 of New Zealand's retail groups</p>
<div class="marquee"><ul class="track">{retailer_items()}</ul><ul class="track" aria-hidden="true">{retailer_items()}</ul></div>
</section>

<section class="band"><div class="wrap">
<div class="head-row"><h2>Shop the range by category</h2><a class="more" href="brands.html">All 20 brands &#8594;</a></div>
<div class="cats">{cat_tiles}</div>
</div></section>

<section class="band band-paper"><div class="wrap aud">
<div class="aud-head"><h2>How can we help?</h2>
<div class="seg" role="tablist" aria-label="Choose your business type">
<button type="button" role="tab" id="at-stock" aria-controls="ap-stock" aria-selected="true">I run a pharmacy or store</button>
<button type="button" role="tab" id="at-sell" aria-controls="ap-sell" aria-selected="false">I own a brand</button></div></div>
<div role="tabpanel" id="ap-stock" aria-labelledby="at-stock" class="aud-panel">
<div><h3>Stock our products</h3><p>Open a wholesale account for access to a broad brand range, bulk purchasing and priority phone or email support.</p>
<a class="btn btn-dark" href="partner.html?interest=stock">Open a wholesale account</a></div>
<ul class="checks"><li>Healthcare, baby, oral care, wellness and FMCG ranges</li><li>Online ordering through the wholesale portal</li><li>Fast account onboarding</li></ul></div>
<div role="tabpanel" id="ap-sell" aria-labelledby="at-sell" class="aud-panel" hidden>
<div><h3>Sell your brand in New Zealand</h3><p>We take brands with real consumer benefits from port to shelf: import, storage, field sales and key accounts handled by one team.</p>
<a class="btn btn-dark" href="partner.html?interest=sell">Talk to us about distribution</a></div>
<ul class="checks"><li>Nationwide retail and pharmacy relationships</li><li>Integrated import and freight coordination</li><li>Scalable logistics for growing brands</li></ul></div>
</div></section>

<section class="band band-navy" id="services"><div class="wrap journey">
<div class="journey-copy">
<h2>From port to shelf, all in-house</h2>
<div class="jtabs" role="tablist" aria-label="Our services">{svc_tabs}</div>
{svc_panels}
<p class="atf">ATF-approved transitional facility support, plus B2B and retail fulfilment.</p>
</div>
<div class="journey-media"><video autoplay muted loop playsinline preload="metadata" aria-label="Aerial view of the ANZ Pharma distribution centre in East Tamaki"><source src="{live('/videos/anzpharma.webm')}" type="video/webm"></video></div>
</div></section>

<section class="band"><div class="wrap">
<div class="head-row"><h2>Every brand we distribute</h2><a class="more" href="brands.html">Explore the catalogue &#8594;</a></div>
<div class="wall">{wall}</div>
</div></section>

<section class="band band-sun"><div class="wrap">
<div class="head-row"><h2>Getting started takes three steps</h2><a class="btn btn-dark" href="partner.html">Start now</a></div>
<ol class="steps">
<li><b>1</b><div><h3>Tell us about your business</h3><p>Your company, your business type and the brands you are interested in.</p></div></li>
<li><b>2</b><div><h3>We connect you with the right person</h3><p>Our sales team sets up your wholesale account or distribution conversation.</p></div></li>
<li><b>3</b><div><h3>Order through the wholesale portal</h3><p>Sign in, order in bulk and get priority phone or email support.</p></div></li>
</ol></div></section>

<section class="band"><div class="wrap team">
{img(live('/images/home/home-team-v2.webp'), 'The ANZ Pharma team', 'photo')}
<div><h2>One team, three functions</h2>
<dl class="rows"><div><dt>Sales and marketing</dt><dd>Promotes products, identifies customer needs and builds client relationships.</dd></div>
<div><dt>Operations and warehouse</dt><dd>Handles inventory, logistics and distribution.</dd></div>
<div><dt>Finance</dt><dd>Manages budgeting, financial analysis and reporting.</dd></div></dl>
<a class="more" href="about.html">More about ANZ Pharma &#8594;</a></div>
</div></section>
"""

# ---------- BRANDS ----------
pills = '<button type="button" class="pill" data-cat="all" aria-pressed="true">All</button>' + "".join(
    f'<button type="button" class="pill c-{k}" data-cat="{k}" aria-pressed="false"><i></i>{e(n)}</button>' for k, n in CATS)
bcards = "".join(
    f'<button type="button" class="brand c-{b[2]}" data-cat="{b[2]}" data-slug="{b[0]}" data-q="{e((b[1] + " " + b[3] + " " + CATNAME[b[2]] + " " + b[5]).lower())}">'
    f'<span class="brand-pic">{img(UP + b[7], b[1] + " products")}<span class="brand-logo">{img(UP + b[8], b[1] + " logo")}</span></span>'
    f'<span class="brand-body"><span class="brand-name">{e(b[1])}</span><span class="tag">{e(b[3])}</span>'
    f'<span class="brand-desc">{e(b[5])}</span><span class="brand-more">View brand &#8594;</span></span></button>'
    for b in BRANDS)
bdata = json.dumps({b[0]: {"name": b[1], "cat": b[2], "catName": CATNAME[b[2]], "type": b[3], "fact": b[4], "about": b[6],
                           "hero": UP + b[7], "logo": UP + b[8], "gallery": [UP + g for g in b[9]]} for b in BRANDS}, ensure_ascii=False).replace("</", "<\\/")
brands = f"""
<section class="page-head"><div class="wrap">
<h1>Trusted by <mark>100+</mark> healthcare and FMCG brands</h1>
<p class="lead">Healthcare, supplements, personal care and household brands, distributed to pharmacies, supermarkets and specialty retailers nationwide.</p>
</div></section>
<section class="band tight-top"><div class="wrap">
<div class="filterbar">
<div class="search"><label for="q" class="sr">Search brands</label><input id="q" type="search" placeholder="Search brands or products" autocomplete="off"></div>
<div class="pills" role="group" aria-label="Filter brands by category">{pills}</div>
<p id="count" aria-live="polite">{len(BRANDS)} brands</p>
</div>
<div class="brand-grid" id="brand-grid">{bcards}</div>
<p class="empty" id="empty" hidden>No brands match. <button type="button" class="linkbtn" id="reset">Clear filters</button></p>
</div></section>
<section class="band band-sun"><div class="wrap cta">
<div><h2>Want your brand on this page?</h2><p>Import, storage, field sales and key accounts, handled by one team in Auckland.</p></div>
<a class="btn btn-dark" href="partner.html?interest=sell">Talk to us about distribution</a>
</div></section>
"""
dialog = f"""<dialog id="brand-dialog" aria-labelledby="bd-name">
<button type="button" class="bd-close" aria-label="Close">&#10005;</button>
<div class="bd-hero"><img id="bd-hero" alt=""></div>
<div class="bd-body">
<div class="bd-top"><span class="bd-logo"><img id="bd-logo" alt=""></span><div><h2 id="bd-name"></h2><p class="bd-tags"><span class="tag" id="bd-type"></span><span class="tag tag-plain" id="bd-fact"></span></p></div></div>
<p id="bd-about"></p>
<div class="bd-gallery" id="bd-gallery"></div>
<div class="row"><a class="btn btn-dark" id="bd-enquire" href="partner.html">Enquire about this brand</a><button type="button" class="btn btn-line" id="bd-next">Next brand &#8594;</button></div>
</div></dialog>
<script type="application/json" id="brand-data">{bdata}</script>"""

# ---------- ABOUT ----------
caps = "".join(f"<li>{e(c)}</li>" for c in CAPS)
about = f"""
<section class="page-head"><div class="wrap team">
<div><h1>A privately owned wholesaler that keeps your business <mark>moving</mark></h1>
<p class="lead">ANZPharma Wholesalers Ltd sells and markets pharmaceutical and FMCG brands with tangible consumer benefits. We focus on what customers feel every day: service, stock levels, delivery and easy ordering.</p>
<p>We source organic, sustainable and reliable pharmaceutical and healthcare products from global names including Unilever, Mustela, Carmex and Bondi Sands.</p></div>
{img(live('/images/about-team.png'), 'ANZ Pharma team and operations', 'photo', lazy=False)}
</div></section>
<section class="band band-navy"><div class="wrap">
<h2>What drives us</h2>
<div class="drive">
<div><h3>Core values</h3><ul class="values"><li class="c-baby">Integrity</li><li class="c-oral">Trust</li><li class="c-skin">Commitment to customers</li><li class="c-health">Innovation</li><li class="c-home">Teamwork</li></ul>
<p>We aim for long-term relationships built on honesty and mutual respect.</p></div>
<div><h3>What we do</h3><p>We supply pharmaceutical, healthcare, wellness and beauty products, so our customers' shelves stay full and their businesses run smoothly.</p></div>
<div><h3>Our strategy</h3><p>Promote and distribute organic, sustainable and reliable products, and give each brand an education platform.</p></div>
</div></div></section>
<section class="band"><div class="wrap team top">
<div><h2>From port to shelf, under one roof</h2>
<p class="lead">Freight, warehousing and sales sit in the same building in East Tamaki, so a brand deals with one team from import to store delivery.</p>
<dl class="hero-stats"><div><dt data-count="7800">7,800</dt><dd>sqm warehouse</dd></div><div><dt data-count="14000">14,000</dt><dd>pallet spaces</dd></div><div><dt data-count="100" data-suffix="+">100+</dt><dd>brands</dd></div></dl></div>
<ul class="checks two">{caps}</ul>
</div></section>
<section class="band band-paper"><div class="wrap">
<h2>Our retail partners</h2>
<ul class="logos">{retailer_items()}</ul>
</div></section>
<section class="band band-sun"><div class="wrap cta">
<div><h2>Ready to partner with us?</h2></div>
<div class="row"><a class="btn btn-dark" href="partner.html">Become a partner</a><a class="more" href="tel:+6495712550">+64 9 571 2550</a></div>
</div></section>
"""

# ---------- PARTNER ----------
def field(i, label, typ="text", ac="", req=True):
    r = " required" if req else ""
    a = f' autocomplete="{ac}"' if ac else ""
    return f'<div class="field"><label for="{i}">{label}{" *" if req else ""}</label><input id="{i}" name="{i}" type="{typ}"{a}{r}></div>'

chips = "".join(f'<button type="button" class="chip c-{b[2]}" data-brand="{e(b[1])}" aria-pressed="false">{e(b[1])}</button>' for b in BRANDS)
partner = f"""
<section class="page-head partner"><div class="wrap team top">
<div>
<h1>Partner with <mark>ANZ Pharma</mark></h1>
<p class="lead">Whether you are a brand expanding across New Zealand or a retailer looking for healthcare and FMCG supply, share a few details and we will connect you with the right person.</p>
<ul class="checks"><li>Nationwide retail relationships</li><li>Healthcare channel access</li><li>Import and distribution capability</li><li>Trusted supplier network</li><li>Fast account onboarding</li></ul>
<div class="talk"><strong>Prefer to talk?</strong><a class="big" href="tel:+6495712550">+64 9 571 2550</a><a href="mailto:sales@anzpharma.co.nz">sales@anzpharma.co.nz</a><span>27E Smales Road, East Tamaki, Auckland 2013</span>
<a href="https://www.google.com/maps/search/?api=1&query=27E+Smales+Road+East+Tamaki+Auckland+2013">Open in Google Maps &#8594;</a></div>
<p class="small">Existing customer with a credit claim? <a href="https://app.smartsheet.com/b/form/b973d35e5c6442339b9a19ecd824c3bc">Use the credit claim form</a>.</p>
</div>
<form id="partner-form" class="form" novalidate>
<fieldset><legend>I am interested in *</legend><div class="seg seg-form">
<label><input type="radio" name="interest" value="Stocking your products" checked><span>Stocking your products</span></label>
<label><input type="radio" name="interest" value="Selling my brand through ANZ Pharma"><span>Selling my brand</span></label>
</div></fieldset>
<div class="two-col">{field('first', 'First name', ac='given-name')}{field('last', 'Last name', ac='family-name')}</div>
<div class="two-col">{field('company', 'Company', ac='organization')}{field('email', 'Email address', 'email', 'email')}</div>
{field('address', 'Address', ac='street-address')}
<div class="field"><label for="btype">Business type *</label><select id="btype" name="btype" required>
<option value="">Select an option</option><option>Pharmacy</option><option>Supermarket or grocery</option><option>Specialty or health retailer</option><option>Online retailer</option><option>Brand owner or manufacturer</option><option>Others</option></select></div>
<div class="field" id="brand-pick"><span class="lbl" id="chips-label">Brands you are interested in (optional, tap to select)</span><div class="chips" role="group" aria-labelledby="chips-label">{chips}</div></div>
<div class="field"><label for="brands">Anything else we should know? (optional)</label><textarea id="brands" name="brands" rows="2"></textarea></div>
<p class="form-msg" id="form-msg" role="status"></p>
<button class="btn btn-dark" type="submit">Submit</button>
<p class="small">Fields marked * are required. Submitting opens your email app with the details addressed to sales@anzpharma.co.nz. See our <a href="{LIVE}/privacy-policy/">privacy policy</a>.</p>
</form>
</div></section>
"""

page("index.html", "ANZ Pharma | Wholesale pharmaceutical, healthcare and FMCG distribution in New Zealand",
     "ANZ Pharma markets and distributes 100+ healthcare and everyday brands to pharmacies, supermarkets and retailers across New Zealand and the Pacific.", home, "home")
page("brands.html", "Our brands | ANZ Pharma", "Healthcare, baby, oral care, wellness and FMCG brands distributed in New Zealand by ANZ Pharma.", brands, "brands", dialog)
page("about.html", "About ANZ Pharma | Freight, warehousing and sales under one roof", "ANZPharma Wholesalers Ltd is a privately owned New Zealand wholesaler of pharmaceutical, healthcare and FMCG brands.", about, "about")
page("partner.html", "Become a partner | ANZ Pharma wholesale registration and contact", "Open a wholesale account or talk to ANZ Pharma about distributing your brand in New Zealand.", partner, "partner")
print("built", sorted(f for f in os.listdir(OUT) if f.endswith(".html")))
