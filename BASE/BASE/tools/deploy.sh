#!/bin/bash
# ══════════════════════════════════════════════════════════
# Atlas Deployment Script
# Safe code-only migration between environments
# ══════════════════════════════════════════════════════════
#
# Usage:
#   ./tools/deploy.sh <source> <target> [--dry-run]
#
# Examples:
#   ./tools/deploy.sh BASE DEV         # Start new feature
#   ./tools/deploy.sh DEV SB           # Promote to sandbox
#   ./tools/deploy.sh SB DEPLOY        # Stage for deployment
#   ./tools/deploy.sh DEPLOY PROD      # Go live
#   ./tools/deploy.sh PROD BASE        # Update golden copy (post-soak)
#   ./tools/deploy.sh PROD HOTFIX      # Start hotfix from prod
#
# Options:
#   --dry-run    Show what would be copied without making changes
#
# ══════════════════════════════════════════════════════════

set -euo pipefail

# ── Configuration ──────────────────────────────────────────
# Adjust ROOT to your actual parent directory
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Deployable code files (relative to environment root)
DEPLOYABLE_FILES=(
    "app.py"
    "requirements.txt"
    ".env.example"
    "VERSION"
    "static/index.html"
    "static/parent.html"
    "static/admin.html"
    "static/guide.html"
    "static/setup.html"
    "static/atlas-theme.css"
    "static/atlas-parent-theme.css"
)

# Deployable directories (copied recursively)
DEPLOYABLE_DIRS=(
    "data/diagnostics"
    "data/state_standards"
    "tools"
    "migrations"
)

# Deployable glob patterns (individual files in data/)
DEPLOYABLE_DATA_FILES=(
    "data/common_core_standards.json"
    "data/ngss_standards.json"
)

# Files that must NEVER be copied
PROTECTED_FILES=(
    ".env"
    "server.log"
    "data/instances/instances.json"
    "data/instances/registry.json"
    "data/admin_safety_notes.json"
    "data/invites.json"
    "data/api_calls.jsonl"
    "data/parent_config.json"
)

# Directories that must NEVER be copied
PROTECTED_DIRS=(
    "data/instances"
    "data/students"
    "data/profiles"
    "data/sessions"
    "data/lessons"
    "data/practice"
    "data/safety_logs"
    "data/platform_feedback"
)

# ── Color output ───────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info()  { echo -e "${BLUE}[INFO]${NC}  $1"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ── Parse arguments ────────────────────────────────────────
if [ $# -lt 2 ]; then
    echo "Usage: $0 <source> <target> [--dry-run]"
    echo ""
    echo "Environments: BASE, DEV, SB, SB-*, DEPLOY, PROD, HOTFIX"
    exit 1
fi

SOURCE="$1"
TARGET="$2"
DRY_RUN=false
if [ "${3:-}" = "--dry-run" ]; then
    DRY_RUN=true
fi

# Resolve paths
# If source/target is "PROD" and we're running from the current ai-tutor dir,
# treat the current directory as PROD. Otherwise look for named subdirs.
resolve_path() {
    local env_name="$1"
    # Check if a subfolder exists with this name
    if [ -d "$ROOT/$env_name" ]; then
        echo "$ROOT/$env_name"
    elif [ "$env_name" = "PROD" ] && [ -f "$ROOT/app.py" ]; then
        # Current directory IS prod
        echo "$ROOT"
    else
        echo "$ROOT/$env_name"
    fi
}

SOURCE_PATH=$(resolve_path "$SOURCE")
TARGET_PATH=$(resolve_path "$TARGET")

# ── Validation ─────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════"
echo "  Atlas Deployment: ${SOURCE} → ${TARGET}"
echo "═══════════════════════════════════════════════════"
echo ""

# Check source exists
if [ ! -d "$SOURCE_PATH" ] || [ ! -f "$SOURCE_PATH/app.py" ]; then
    error "Source environment not found or invalid: $SOURCE_PATH"
    error "Expected app.py at: $SOURCE_PATH/app.py"
    exit 1
fi
info "Source: $SOURCE_PATH"

# If targeting PROD, require backup first
if [ "$TARGET" = "PROD" ]; then
    BACKUP_DIR="$ROOT/PROD_BACKUP/$(date +%Y-%m-%d_%H%M%S)"
    warn "Target is PROD. Creating backup first..."
    if [ "$DRY_RUN" = true ]; then
        info "[DRY RUN] Would create backup at: $BACKUP_DIR"
    else
        mkdir -p "$BACKUP_DIR"
        # Backup only code files from PROD
        for f in "${DEPLOYABLE_FILES[@]}"; do
            if [ -f "$TARGET_PATH/$f" ]; then
                mkdir -p "$BACKUP_DIR/$(dirname "$f")"
                cp "$TARGET_PATH/$f" "$BACKUP_DIR/$f"
            fi
        done
        for d in "${DEPLOYABLE_DIRS[@]}"; do
            if [ -d "$TARGET_PATH/$d" ]; then
                mkdir -p "$BACKUP_DIR/$d"
                cp -r "$TARGET_PATH/$d/." "$BACKUP_DIR/$d/"
            fi
        done
        for f in "${DEPLOYABLE_DATA_FILES[@]}"; do
            if [ -f "$TARGET_PATH/$f" ]; then
                mkdir -p "$BACKUP_DIR/$(dirname "$f")"
                cp "$TARGET_PATH/$f" "$BACKUP_DIR/$f"
            fi
        done
        ok "Backup created at: $BACKUP_DIR"
    fi
    echo ""
fi

info "Target: $TARGET_PATH"
echo ""

# ── Safety check: ensure no protected files in source staging ──
info "Checking for protected files in deployment..."
VIOLATIONS=0
for f in "${PROTECTED_FILES[@]}"; do
    if [ "$DRY_RUN" = false ] && [ -f "$SOURCE_PATH/$f" ] && [ "$SOURCE" != "PROD" ] && [ "$TARGET" = "PROD" ]; then
        # Not an error — we just won't copy these
        info "Protected file exists in source (will NOT be copied): $f"
    fi
done

# ── Create target directory structure ──────────────────────
if [ "$DRY_RUN" = true ]; then
    info "[DRY RUN] Would create target directory: $TARGET_PATH"
else
    mkdir -p "$TARGET_PATH"
    mkdir -p "$TARGET_PATH/static"
    mkdir -p "$TARGET_PATH/data"
fi

# ── Copy deployable files ──────────────────────────────────
info "Copying deployable code files..."
echo ""

COPIED=0
SKIPPED=0

for f in "${DEPLOYABLE_FILES[@]}"; do
    if [ -f "$SOURCE_PATH/$f" ]; then
        if [ "$DRY_RUN" = true ]; then
            echo "  [COPY] $f"
        else
            mkdir -p "$TARGET_PATH/$(dirname "$f")"
            cp "$SOURCE_PATH/$f" "$TARGET_PATH/$f"
        fi
        COPIED=$((COPIED + 1))
    else
        echo "  [SKIP] $f (not in source)"
        SKIPPED=$((SKIPPED + 1))
    fi
done

# Copy deployable directories
for d in "${DEPLOYABLE_DIRS[@]}"; do
    if [ -d "$SOURCE_PATH/$d" ]; then
        if [ "$DRY_RUN" = true ]; then
            echo "  [COPY] $d/ (recursive)"
        else
            mkdir -p "$TARGET_PATH/$d"
            cp -r "$SOURCE_PATH/$d/." "$TARGET_PATH/$d/"
        fi
        COPIED=$((COPIED + 1))
    else
        echo "  [SKIP] $d/ (not in source)"
        SKIPPED=$((SKIPPED + 1))
    fi
done

# Copy deployable data files
for f in "${DEPLOYABLE_DATA_FILES[@]}"; do
    if [ -f "$SOURCE_PATH/$f" ]; then
        if [ "$DRY_RUN" = true ]; then
            echo "  [COPY] $f"
        else
            mkdir -p "$TARGET_PATH/$(dirname "$f")"
            cp "$SOURCE_PATH/$f" "$TARGET_PATH/$f"
        fi
        COPIED=$((COPIED + 1))
    else
        echo "  [SKIP] $f (not in source)"
        SKIPPED=$((SKIPPED + 1))
    fi
done

echo ""
ok "Copied: $COPIED items"
if [ $SKIPPED -gt 0 ]; then
    warn "Skipped: $SKIPPED items (not present in source)"
fi

# ── Check for migrations ──────────────────────────────────
if [ -d "$SOURCE_PATH/migrations" ] && [ "$TARGET" = "PROD" ]; then
    echo ""
    MIGRATION_COUNT=$(find "$SOURCE_PATH/migrations" -name "*.py" -type f 2>/dev/null | wc -l)
    if [ "$MIGRATION_COUNT" -gt 0 ]; then
        warn "Found $MIGRATION_COUNT migration script(s) in source."
        warn "Run migrations AFTER this script completes but BEFORE starting the server:"
        find "$SOURCE_PATH/migrations" -name "*.py" -type f | sort | while read m; do
            echo "    python3 $m"
        done
    fi
fi

# ── Version check ──────────────────────────────────────────
if [ -f "$TARGET_PATH/VERSION" ]; then
    echo ""
    info "Deployed version: $(cat "$TARGET_PATH/VERSION")"
fi

# ── Summary ────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════"
if [ "$DRY_RUN" = true ]; then
    warn "DRY RUN complete. No files were modified."
else
    ok "Deployment ${SOURCE} → ${TARGET} complete!"
fi
echo "═══════════════════════════════════════════════════"

# Post-deployment reminders
if [ "$TARGET" = "PROD" ] && [ "$DRY_RUN" = false ]; then
    echo ""
    warn "Post-deployment reminders:"
    echo "  1. Run any pending data migrations"
    echo "  2. Start the PROD server"
    echo "  3. Verify all family instances load correctly"
    echo "  4. Re-establish Cloudflare tunnel if needed"
    echo "  5. Monitor for 24 hours before updating BASE"
fi

if [ "$TARGET" = "DEV" ] && [ "$DRY_RUN" = false ]; then
    echo ""
    info "Next steps:"
    echo "  1. Create .env with your development API key"
    echo "  2. Seed data/ with a synthetic Demo Family instance"
    echo "  3. Start developing!"
fi
