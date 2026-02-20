# Documentation Site

This directory contains the source files for the GitHub Pages documentation site.

## Structure

- `_config.yml` - Jekyll configuration
- `index.md` - Homepage
- `security.md` - Security policy and practices
- `contributing.md` - Contribution guidelines
- `Gemfile` - Ruby dependencies for local development

## Local Development

To preview the site locally:

```bash
cd docs

# Install dependencies (first time only)
bundle install

# Serve the site locally
bundle exec jekyll serve

# Visit http://localhost:4000/.github/ in your browser
```

## Building the Site

GitHub Actions automatically builds and deploys the site when changes are pushed to the `main` branch. The workflow is defined in `.github/workflows/pages.yml`.

## Adding New Pages

1. Create a new markdown file in this directory
2. Add front matter at the top:
   ```yaml
   ---
   layout: default
   title: Page Title
   ---
   ```
3. Write your content in Markdown
4. Link to it from `index.md` or other pages

## Theme

The site uses the `jekyll-theme-minimal` theme. You can customize the appearance by:

- Modifying `_config.yml`
- Creating custom layouts in `_layouts/`
- Adding custom CSS in `assets/css/`

## Links to Main Repository

Most documentation is stored in the root of the repository as `.md` files. The docs site provides:

- A user-friendly index page
- Navigation structure
- Links back to the full documentation in the repository

## Deployment

The site is automatically deployed to: https://kushmanmb-org.github.io/.github/

Deployment is handled by the GitHub Pages workflow which:
1. Checks out the code
2. Builds the Jekyll site from this directory
3. Deploys to GitHub Pages

## Troubleshooting

If the site doesn't build:

1. Check the Actions tab for build errors
2. Verify Jekyll syntax in markdown files
3. Ensure front matter is properly formatted
4. Test locally with `bundle exec jekyll build`
