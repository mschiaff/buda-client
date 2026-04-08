#!/usr/bin/env bash
set -euo pipefail

# ─── Release Script ───────────────────────────────────────────────────────────
# Usage: ./scripts/release.sh [patch|minor|major|auto]
#
# Bumps the version, updates the changelog, commits, tags, and pushes.
# The tag push triggers the release workflow on GitHub Actions.
# ──────────────────────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

info()  { echo -e "${CYAN}ℹ ${NC}$1"; }
ok()    { echo -e "${GREEN}✔ ${NC}$1"; }
warn()  { echo -e "${YELLOW}⚠ ${NC}$1"; }
error() { echo -e "${RED}✖ ${NC}$1" >&2; exit 1; }

# ─── Preflight checks ────────────────────────────────────────────────────────

command -v git-cliff >/dev/null 2>&1 || error "git-cliff is not installed. Run: brew install git-cliff"
command -v uv >/dev/null 2>&1        || error "uv is not installed. See: https://docs.astral.sh/uv/"

BUMP_TYPE="${1:-}"
if [[ -z "$BUMP_TYPE" ]]; then
    echo "Usage: ./scripts/release.sh [patch|minor|major|auto]"
    echo ""
    echo "  patch  — Bug fixes (0.1.0 → 0.1.1)"
    echo "  minor  — New features (0.1.0 → 0.2.0)"
    echo "  major  — Breaking changes (0.1.0 → 1.0.0)"
    echo "  auto   — Infer from conventional commits"
    exit 1
fi

if [[ "$BUMP_TYPE" != "patch" && "$BUMP_TYPE" != "minor" && "$BUMP_TYPE" != "major" && "$BUMP_TYPE" != "auto" ]]; then
    error "Invalid bump type: $BUMP_TYPE (must be patch, minor, major, or auto)"
fi

BRANCH=$(git branch --show-current)
if [[ "$BRANCH" != "main" ]]; then
    error "Must be on 'main' branch (currently on '$BRANCH')"
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
    error "Working tree is not clean. Commit or stash changes first."
fi

# Pull latest to avoid conflicts
info "Pulling latest from origin/main..."
git pull --rebase origin main
ok "Up to date"

# ─── Determine versions ──────────────────────────────────────────────────────

CURRENT_VERSION=$(grep '^version' pyproject.toml | head -1 | sed 's/.*"\(.*\)"/\1/')
info "Current version: ${CYAN}${CURRENT_VERSION}${NC}"

if [[ "$BUMP_TYPE" == "auto" ]]; then
    NEW_VERSION=$(git cliff --bumped-version | sed 's/^v//')
    if [[ -z "$NEW_VERSION" || "$NEW_VERSION" == "$CURRENT_VERSION" ]]; then
        error "No version bump detected from commits. Use a manual bump type instead."
    fi
else
    uv version --bump "$BUMP_TYPE"
    NEW_VERSION=$(grep '^version' pyproject.toml | head -1 | sed 's/.*"\(.*\)"/\1/')
fi

# For auto mode, we still need to set the version in pyproject.toml
if [[ "$BUMP_TYPE" == "auto" ]]; then
    uv version "$NEW_VERSION"
fi

ok "New version: ${GREEN}${NEW_VERSION}${NC}"

# ─── Update lockfile ─────────────────────────────────────────────────────────

info "Updating lockfile..."
uv lock
ok "Lockfile updated"

# ─── Generate changelog ──────────────────────────────────────────────────────

info "Generating changelog..."
git cliff --tag "v${NEW_VERSION}" --output CHANGELOG.md
ok "Changelog updated"

# ─── Review and confirm ──────────────────────────────────────────────────────

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}  Release Summary${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  Version:  ${CURRENT_VERSION} → ${GREEN}${NEW_VERSION}${NC}"
echo -e "  Tag:      ${GREEN}v${NEW_VERSION}${NC}"
echo -e "  Bump:     ${BUMP_TYPE}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

info "Changed files:"
git diff --stat
echo ""

read -rp "$(echo -e "${YELLOW}Proceed with release? [y/N] ${NC}")" CONFIRM
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    warn "Aborted. Restoring files..."
    git checkout -- pyproject.toml CHANGELOG.md
    git checkout -- uv.lock 2>/dev/null || true
    exit 0
fi

# ─── Commit, tag, push ───────────────────────────────────────────────────────

info "Committing..."
git add pyproject.toml uv.lock CHANGELOG.md
git commit -m "chore(release): v${NEW_VERSION}"
ok "Committed"

info "Tagging v${NEW_VERSION}..."
git tag "v${NEW_VERSION}"
ok "Tagged"

info "Pushing to origin..."
git push origin main --tags
ok "Pushed"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  Release v${NEW_VERSION} is on its way!${NC}"
echo -e "${GREEN}  GitHub Actions will handle build, release, and publish.${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
