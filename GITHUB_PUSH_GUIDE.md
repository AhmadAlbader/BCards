# Quick Start: Push Project to GitHub

## Prerequisites

- GitHub account
- Git installed locally
- This project cloned/ready

## Step 1: Create Private Repository on GitHub

1. Go to https://github.com/new
2. **Repository name**: `digital-business-cards`
3. **Description**: `Full-stack digital business cards with QR code generation`
4. **Privacy**: Select **Private** (recommended for closed projects)
5. **Do NOT** initialize with README, .gitignore, or license (we already have them)
6. Click **Create repository**

## Step 2: Add GitHub Remote & Push

```bash
# Replace YOUR_USERNAME with your GitHub username
cd /Users/mac/New\ AI\ Projects/Digital\ Business\ Cards

# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/digital-business-cards.git

# Rename branch to main (if not already)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Verify on GitHub

Visit: `https://github.com/YOUR_USERNAME/digital-business-cards`

You should see:
- ✅ All project files
- ✅ Commit history
- ✅ `.env.development` file (configurations)
- ✅ `.env.production.template` file (template only)
- ❌ `.env.local` (not committed - personal)
- ❌ `.env.production` (not committed - server only)
- ✅ Complete documentation
- ✅ Docker files
- ✅ Frontend and Backend code

## Step 4: Update Git Config (Optional)

```bash
# Set global git config
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Or for this project only
cd /Users/mac/New\ AI\ Projects/Digital\ Business\ Cards
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/feature-name
```

### 2. Make Changes

Edit files as needed

### 3. Commit Changes

```bash
git add .
git commit -m "Description of changes"
```

### 4. Push to GitHub

```bash
git push origin feature/feature-name
```

### 5. Merge to Main

On GitHub:
1. Create Pull Request
2. Review changes
3. Click "Merge pull request"
4. Click "Confirm merge"

Or locally:

```bash
git checkout main
git pull origin main
git merge feature/feature-name
git push origin main
```

---

## Testing Locally Before Pushing

```bash
# Make sure everything works locally
cd /Users/mac/New\ AI\ Projects/Digital\ Business\ Cards

# Start services
docker-compose up -d

# Test frontend
curl http://192.168.1.123:3000

# Test backend API
curl http://192.168.1.123:8000/docs

# Stop services
docker-compose down

# Then commit and push
git add .
git commit -m "Your commit message"
git push origin main
```

---

## Commands Reference

| Task | Command |
|------|---------|
| Clone | `git clone https://github.com/USERNAME/digital-business-cards.git` |
| Status | `git status` |
| Add files | `git add .` |
| Commit | `git commit -m "message"` |
| Push | `git push origin main` |
| Pull | `git pull origin main` |
| Create branch | `git checkout -b feature-name` |
| Switch branch | `git checkout branch-name` |
| List branches | `git branch -a` |
| Delete branch | `git branch -d branch-name` |
| View logs | `git log --oneline` |
| View changes | `git diff` |

---

## Troubleshooting

### "Permission denied (publickey)"

SSH key issue. Use HTTPS instead:

```bash
git remote set-url origin https://github.com/USERNAME/digital-business-cards.git
```

### ".env.local was committed accidentally"

```bash
git rm --cached .env.local
git commit -m "Remove .env.local from tracking"
git push origin main
```

### "Cannot push - repository is public"

Create a **private** repository on GitHub if you don't want code visible to everyone.

### "Remote origin already exists"

```bash
git remote rm origin
git remote add origin https://github.com/USERNAME/digital-business-cards.git
```

---

## Next Steps

After pushing to GitHub:

1. ✅ Code is backed up
2. ✅ Easy to pull on DigitalOcean server
3. ✅ Ready for team collaboration
4. ✅ Version history preserved
5. 📍 Deploy to DigitalOcean using DEPLOYMENT_GUIDE.md
