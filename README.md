# ANZ Pharma website (redesign build)

Static site: `index.html`, `brands.html`, `about.html`, `partner.html`, `css/styles.css`, `js/main.js`.
Open `index.html` in a browser, or run `python3 -m http.server 3000` here and visit http://localhost:3000.

Edit content in `build.py` (brands, retailers, copy) and run `python3 build.py` to regenerate the four pages. Styles and scripts are edited directly.

## Before going live
- Images, logo and video load from the current live site (www.anzpharma.co.nz/images, /videos) and brand photos/logos from brand.anzpharma.co.nz/uploads. Copy them into an `assets/` folder and repoint the URLs in `build.py` (`live(...)` and `UP`), or they break when the old site is replaced.
- The partner form opens the visitor's email app addressed to sales@anzpharma.co.nz. Replace with a real form endpoint (see `js/main.js`).
- Brand descriptions are short rewrites of the live brand pages: have the client approve them. Opening hours are not published.
- Double A is no longer listed on the live Brands page, so it is not in this build (20 brands).
- Privacy, terms and disclaimer links point at the current live pages.

Design canvas: https://claude.ai/artifact/AreQ9xGSTihPySB6Btyp8G . Audit: `SITE-AUDIT.md`. Old folder contents: `_backup_daily-cleaning-website/`.
