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

The target URL is **https://mengbingzhou.github.io/**. GitHub requires a user or organization named `mengbingzhou` with a repository named `mengbingzhou.github.io` for this default address. Confirm ownership/availability first. Merely renaming a repository under another account does not provide this address.

This checkout currently points to `Zhou-MB/homepage`; publishing it as a project site would normally use `https://zhou-mb.github.io/homepage/`.

1. Under the intended `mengbingzhou` account or organization, create the public repository `mengbingzhou.github.io`.
2. Push these files to its default branch, with `index.html` at the repository root.
3. In **Settings → Pages**, choose **Deploy from a branch**, select the default branch and **/ (root)**, and save.
4. Check the Pages deployment and visit https://mengbingzhou.github.io/.

The `.nojekyll` file enables direct static-file publishing. No custom-domain CNAME is needed. If publishing at a different URL, update the canonical URL, Open Graph URLs, JSON-LD URLs, `robots.txt`, and `sitemap.xml` before deploying.

## Search visibility

The page includes a descriptive title, English/Chinese name metadata, a canonical URL, ProfilePage/Person structured data, a sitemap, and crawler access. After publishing:

1. Verify the live URL in Google Search Console.
2. Submit `sitemap.xml` and request indexing of the homepage.
3. Link to the homepage from your university profile and other authentic academic profiles.

Indexing and ranking for “Mengbing Zhou” or “周梦兵” are controlled by search engines and cannot be guaranteed. This first version has not been published by creating these files.

References: [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), [Google indexing requests](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl).

Teaching and supervision entries in `#teaching-list` use `data-sort-date="YYYY-MM"` for the end date. They are sorted newest first, with five shown initially and a Show more / Show less button when needed.
