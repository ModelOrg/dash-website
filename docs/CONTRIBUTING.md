
# Dash Website: Quick Contributing Guide

## 1. Setting up local environment
All contributors must use linters and formatters. Please see these guides for setting up:
- [Black](https://black.readthedocs.io/en/stable/integrations/editors.html)
- [Ruff](https://docs.astral.sh/ruff/editors/)

## 2. Using development branches
All changes must be made on development branches and merged as pull requests before making it into `main`.

```bash
# Create a new branch for your work
git checkout -b my-feature-name

# Make your changes, then stage and commit them
git add .
git commit -m "Describe your changes"

# Push your branch to GitHub
git push origin my-feature-name

# Open a pull request from your branch to main on GitHub
```

## 2. Add/Edit a Page

Copy the template:
```bash
cp pages/_template.py pages/my_page.py
```
Edit your new file and register the page with a unique path and name.
For more in-depth examples of how to use `_template.py`, please see [USAGE_GUIDE.md](USAGE_GUIDE.md)

## 3. Test Locally

Start the app:
```bash
python app.py
```
Visit `http://localhost:8050/your-path` to check your page.

## 4. Mark Ready for Review

Commit and push your changes:
```bash
git add pages/my_page.py
git commit -m "Add my page"
git push origin my-feature-name
```
Open a pull request (PR) on GitHub.

---

**Tips:**
- Use clear variable names and comments
- Keep callbacks simple
- Don't commit data, .env, or IDE files

For help, see `pages/_template.py` or ask in chat.