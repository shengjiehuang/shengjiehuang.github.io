# shengjiehuang.github.io

Personal website of Sheng-Jie Huang, built with [al-folio](https://github.com/alshedivat/al-folio) (Jekyll) and hosted on GitHub Pages.

## Where things live

| To change…                    | Edit                                                                         |
| ----------------------------- | ---------------------------------------------------------------------------- |
| Home page (bio, positions)    | `_pages/about.md`                                                            |
| Research page                 | `_pages/research.md`                                                         |
| Talks                         | `_data/talks.yml`                                                            |
| Courses                       | add a file to `_teachings/` (template in `_pages/teaching.md`)               |
| Group / prospective students  | `_pages/group.md`                                                            |
| News on the home page         | add a file to `_news/` (copy an existing one, change the date and text)     |
| Email / Scholar / ORCID icons | `_data/socials.yml`                                                          |
| Profile photo                 | put it at `assets/img/prof_pic.jpg`, then uncomment `image:` in `_pages/about.md` |
| Site name, URL, features      | `_config.yml`                                                                |

Any change pushed to `main` rebuilds the site automatically (GitHub Actions → "Deploy site").

## Publications update themselves

`scripts/update_pubs.py` downloads your papers from arXiv and writes `_bibliography/papers.bib`.
The "Update publications" workflow runs it every Monday, commits any change, and redeploys.
You can also run it by hand from the repository's **Actions** tab, or locally with `python3 scripts/update_pubs.py`.

- **Don't edit `papers.bib` by hand.** It is overwritten on every run.
- **Corrections** (missing journal reference, published title, equal-contribution marks, hiding a paper) go in `_bibliography/manual.bib`. The comments at the top explain how.
- **Which papers are fetched** is set in `scripts/publications.json`. Right now it searches arXiv for the author "Sheng-Jie Huang", plus two 2011 papers listed under "S. -J. Huang".
  After you [claim your papers on arXiv](https://info.arxiv.org/help/authority.html) you get an author ID (e.g. `huang_s_1`). Put it in `arxiv_author_id` and the list will come from your arXiv author page instead, which rules out namesakes.
- **When a paper is published,** add the journal reference and DOI on arXiv (arXiv → your paper → "Replace" / "Add journal ref"). The site picks them up within a week. Until then, you can add an override in `manual.bib`.

## Preview on your Mac

```bash
export PATH=/usr/local/opt/ruby/bin:$PATH LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000.
