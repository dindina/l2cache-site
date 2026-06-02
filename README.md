# L2cache — GitHub Pages Site

## Setup (10 minutes)

### 1. Create the GitHub repository
- Go to github.com/dindina
- New repository → name it exactly: `l2cache-site`
- Set to **Public**
- Don't add README (you have this one)

### 2. Push these files
```bash
cd /path/to/this/folder
git init
git add .
git commit -m "Initial site"
git remote add origin https://github.com/dindina/l2cache-site.git
git push -u origin main
```

### 3. Enable GitHub Pages
- Go to repo → Settings → Pages
- Source: **Deploy from a branch**
- Branch: `main` / `/(root)`
- Click Save

### 4. Your URLs (live in ~2 minutes)
- Landing page:    https://dindina.github.io/l2cache-site/
- Privacy policy:  https://dindina.github.io/l2cache-site/privacy.html
- Support page:    https://dindina.github.io/l2cache-site/support.html

### 5. Paste into App Store Connect
- **Privacy Policy URL:** https://dindina.github.io/l2cache-site/privacy.html
- **Support URL:**        https://dindina.github.io/l2cache-site/support.html
- **Marketing URL:**      https://dindina.github.io/l2cache-site/

## Later — custom domain (amvo.io)
1. Buy amvo.io on Namecheap
2. In repo Settings → Pages → Custom domain → enter amvo.io
3. Add CNAME record in Namecheap DNS pointing to dindina.github.io
4. URLs become: amvo.io, amvo.io/privacy.html, amvo.io/support.html
5. Zero changes to HTML needed — same files, new domain

## TODO before App Store submission
- [ ] Replace "#" download button href with real App Store URL
- [ ] Add real screenshot to hero (optional — mockup works fine)
- [ ] Update support email if different from support@amvo.io
