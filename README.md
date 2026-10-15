# Mengbing Zhou — Academic Homepage

A lightweight, responsive English academic homepage. Plain HTML and CSS; no build step or external JavaScript dependencies.

## Preview locally

From this directory, run `python3 -m http.server 8000`, then open http://localhost:8000.

## Update content

- Edit `index.html` to update the biography, publications, and news. The initial biography, education, experience, honors, six publications, and dated news are based on the supplied CV. Publication years and complete author lists were not supplied; add them when verified.
- Replace `figures/mengbing.jpg` to change the portrait.
- Edit `style.css` to change the appearance.
- Add news entries to `#news-list` in `index.html`, each with a `<time datetime="YYYY-MM">` (or `YYYY-MM-DD`). `news.js` sorts entries newest first and shows five by default, with a “View all news” toggle only when more exist. Without JavaScript, all entries remain readable.
- The academic email is included. Add verified Google Scholar, ORCID, and an updated public CV link when available.
- The Chinese name 周梦兵 is included as a search alias in metadata; visible content is English.

## Publish at the requested address

The target URL is **https://zhou-mb.github.io/**. This requires the repository `Zhou-MB/zhou-mb.github.io` (one user site per account).

1. In the current repository’s **Settings → General**, rename `homepage` to `zhou-mb.github.io` if that repository name is not already in use.
2. In **Settings → Pages**, keep the intended publishing branch and **/ (root)** source (or the existing GitHub Actions deployment).
3. Update the local remote with `git remote set-url origin git@github.com:Zhou-MB/zhou-mb.github.io.git` after renaming.
4. Push these files and check the Pages deployment, then visit https://zhou-mb.github.io/.

The `.nojekyll` file enables direct static-file publishing. No custom-domain CNAME is needed. If publishing at a different URL, update the canonical URL, Open Graph URLs, JSON-LD URLs, `robots.txt`, and `sitemap.xml` before deploying.

## Search visibility

The page includes a descriptive title, English/Chinese name metadata, a canonical URL, ProfilePage/Person structured data, a sitemap, and crawler access. After publishing:

1. Verify the live URL in Google Search Console.
2. Submit `sitemap.xml` and request indexing of the homepage.
3. Link to the homepage from your university profile and other authentic academic profiles.

Indexing and ranking for “Mengbing Zhou” or “周梦兵” are controlled by search engines and cannot be guaranteed. This first version has not been published by creating these files.

References: [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), [Google indexing requests](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl).

Teaching and supervision entries in `#teaching-list` use `data-sort-date="YYYY-MM"` for the end date. They are sorted newest first, with five shown initially and a Show more / Show less button when needed.

## Publication badges

Each paper displays year, Bib, and PDF badges before its venue. Fill `publicationResources` in `publications.js` with the verified year, BibTeX string, and a repository-relative PDF path. Until supplied, the year shows “Year —” and Bib/PDF controls are disabled. Bib opens the exact text inline (and closes on a second click). PDFs use the browser's download attribute; host them in this repository for reliable same-origin downloads. Keep resource keys matched to each publication's HTML ID.
