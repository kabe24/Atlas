#!/usr/bin/env python3
"""
Atlas Migration: JSON Files → Supabase Tables

Reads all Atlas data from the file-based storage (data/ directory) and
inserts it into Supabase tables for production use on KmUnity/Railway.

IMPORTANT: This script must be run AFTER:
  1. 007_atlas_tables.sql has been applied in Supabase SQL Editor
  2. KmUnity families and profiles exist (for foreign key references)

Usage:
  # Dry run — count records, no writes
  python migrations/migrate_json_to_supabase.py --dry-run

  # Full migration
  python migrations/migrate_json_to_supabase.py

  # Migrate a single instance
  python migrations/migrate_json_to_supabase.py --instance default

Environment Variables:
  SUPABASE_URL              — Supabase project URL
  SUPABASE_SERVICE_ROLE_KEY — Service role key (full access)
  ATLAS_DATA_DIR            — Path to Atlas data/ directory (default: "data")
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ─── Setup ──────────────────────────────────────────────────────

try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

DATA_DIR = Path(os.getenv("ATLAS_DATA_DIR", "data"))
INSTANCES_DIR = DATA_DIR / "instances"
STUDENTS_DIR = DATA_DIR / "students"

SUBJECTS = ["math", "science", "ela", "social_studies"]


# ─── Supabase Client ───────────────────────────────────────────

def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set.")
        sys.exit(1)
    from supabase import create_client
    return create_client(url, key)


# ─── Helpers ────────────────────────────────────────────────────

def safe_json_load(path: Path, default=None):
    if default is None:
        default = {}
    try:
        if not path.exists():
            return default
        text = path.read_text().strip()
        if not text:
            return default
        return json.loads(text)
    except (json.JSONDecodeError, OSError) as e:
        print(f"  ⚠  Bad JSON in {path}: {e}")
        return default


def now_iso():
    return datetime.now().isoformat()


# ─── ID Mapping ────────────────────────────────────────────────
#
# Atlas file-based storage uses short string IDs (e.g., "b0f6cfda").
# KmUnity Supabase uses UUIDs for profile_id and family_id.
#
# Two strategies:
#   A. If KmUnity profiles already exist (onboarded families), we look up
#      the mapping by atlas_student_id stored in profile metadata.
#   B. If migrating standalone Atlas (no KmUnity profiles yet), we create
#      atlas_students rows with profile_id = student_id (string UUIDs
#      will be needed, or we bridge after KmUnity onboarding).
#
# This script supports both modes via --id-mode flag.


class IdMapper:
    """Maps Atlas file-based IDs to Supabase UUIDs."""

    def __init__(self, supabase, mode="standalone"):
        self.sb = supabase
        self.mode = mode
        self._student_map = {}   # atlas_id → supabase profile_id
        self._instance_map = {}  # atlas instance_id → supabase family_id

    def build_maps(self):
        """Pre-load mappings from Supabase if in 'bridge' mode."""
        if self.mode == "bridge":
            # Look for existing atlas_students to find profile_id mappings
            result = self.sb.table("atlas_students").select("profile_id, data").execute()
            for row in (result.data or []):
                atlas_id = row.get("data", {}).get("student_id")
                if atlas_id:
                    self._student_map[atlas_id] = row["profile_id"]

            # Look for KmUnity families
            result = self.sb.table("families").select("id, name").execute()
            for row in (result.data or []):
                name = row.get("name", "")
                self._instance_map[name.lower()] = row["id"]

    def student_id(self, atlas_id: str) -> str:
        """Map an Atlas student ID to a Supabase profile_id."""
        if self.mode == "bridge" and atlas_id in self._student_map:
            return self._student_map[atlas_id]
        # Standalone: use the Atlas ID directly (will be text, not UUID)
        return atlas_id

    def family_id(self, instance_id: str) -> str | None:
        """Map an Atlas instance_id to a Supabase family_id."""
        if self.mode == "bridge":
            return self._instance_map.get(instance_id)
        # Standalone: use instance_id as-is
        return instance_id if instance_id else None


# ─── Migration Functions ────────────────────────────────────────

class MigrationStats:
    def __init__(self):
        self.counts = {}
        self.errors = []

    def inc(self, table: str, count: int = 1):
        self.counts[table] = self.counts.get(table, 0) + count

    def error(self, msg: str):
        self.errors.append(msg)
        print(f"  ✗ {msg}")

    def summary(self):
        print("\n═══ Migration Summary ═══")
        total = 0
        for table, count in sorted(self.counts.items()):
            print(f"  {table}: {count} rows")
            total += count
        print(f"  ─────────────────────")
        print(f"  Total: {total} rows")
        if self.errors:
            print(f"\n  ⚠ {len(self.errors)} errors:")
            for e in self.errors[:20]:
                print(f"    - {e}")
            if len(self.errors) > 20:
                print(f"    ... and {len(self.errors) - 20} more")


def migrate_instance_config(sb, mapper, instance_id: str, stats: MigrationStats, dry_run: bool):
    """Migrate instance_config.json → atlas_instance_config."""
    path = INSTANCES_DIR / instance_id / "instance_config.json"
    data = safe_json_load(path)
    if not data:
        return

    fam_id = mapper.family_id(instance_id)
    stats.inc("atlas_instance_config")

    if not dry_run:
        try:
            sb.table("atlas_instance_config").upsert({
                "family_id": fam_id,
                "data": data,
                "updated_at": now_iso(),
            }, on_conflict="family_id").execute()
        except Exception as e:
            stats.error(f"instance_config [{instance_id}]: {e}")


def migrate_parent_config(sb, mapper, instance_id: str, stats: MigrationStats, dry_run: bool):
    """Migrate parent_config.json → atlas_parent_config."""
    path = INSTANCES_DIR / instance_id / "parent_config.json"
    data = safe_json_load(path)
    if not data:
        return

    fam_id = mapper.family_id(instance_id)
    stats.inc("atlas_parent_config")

    if not dry_run:
        try:
            sb.table("atlas_parent_config").upsert({
                "family_id": fam_id,
                "data": data,
                "updated_at": now_iso(),
            }, on_conflict="family_id").execute()
        except Exception as e:
            stats.error(f"parent_config [{instance_id}]: {e}")


def migrate_diagnostics_pending(sb, mapper, instance_id: str, stats: MigrationStats, dry_run: bool):
    """Migrate diagnostics_pending.json → atlas_diagnostics_pending."""
    path = INSTANCES_DIR / instance_id / "diagnostics_pending.json"
    data = safe_json_load(path)
    if not data:
        return

    fam_id = mapper.family_id(instance_id)
    stats.inc("atlas_diagnostics_pending")

    if not dry_run:
        try:
            sb.table("atlas_diagnostics_pending").upsert({
                "family_id": fam_id,
                "data": data,
                "updated_at": now_iso(),
            }, on_conflict="family_id").execute()
        except Exception as e:
            stats.error(f"diagnostics_pending [{instance_id}]: {e}")


def migrate_student(sb, mapper, instance_id: str, student_id: str,
                    student_data: dict, stats: MigrationStats, dry_run: bool):
    """Migrate a single student and all their subject data."""
    pid = mapper.student_id(student_id)
    fam_id = mapper.family_id(instance_id)

    # 1. Student metadata → atlas_students
    stats.inc("atlas_students")
    if not dry_run:
        try:
            sb.table("atlas_students").upsert({
                "profile_id": pid,
                "family_id": fam_id,
                "data": student_data,
                "updated_at": now_iso(),
            }, on_conflict="profile_id").execute()
        except Exception as e:
            stats.error(f"student [{student_id}]: {e}")
            return  # skip subject data if student fails

    # Determine student data directory
    student_dir = INSTANCES_DIR / instance_id / "students" / student_id
    if not student_dir.exists():
        # Try legacy flat directory
        student_dir = STUDENTS_DIR / student_id

    if not student_dir.exists():
        return

    # 2. Subject profiles → atlas_profiles
    profiles_dir = student_dir / "profiles"
    if profiles_dir.exists():
        for pf in profiles_dir.glob("*.json"):
            subject = pf.stem
            profile_data = safe_json_load(pf)
            if not profile_data:
                continue
            stats.inc("atlas_profiles")
            if not dry_run:
                try:
                    sb.table("atlas_profiles").upsert({
                        "profile_id": pid,
                        "family_id": fam_id,
                        "subject": subject,
                        "grade": profile_data.get("grade"),
                        "topics": profile_data.get("topics", {}),
                        "proficiency": profile_data.get("proficiency", {}),
                        "current_lesson": profile_data.get("current_lesson", {}),
                        "preferences": profile_data.get("preferences", {}),
                        "extra_data": {k: v for k, v in profile_data.items()
                                       if k not in ("grade", "topics", "proficiency",
                                                     "current_lesson", "preferences", "subject")},
                        "updated_at": now_iso(),
                    }, on_conflict="profile_id,subject").execute()
                except Exception as e:
                    stats.error(f"profile [{student_id}/{subject}]: {e}")

    # 3. Diagnostics → atlas_diagnostics
    diag_dir = student_dir / "diagnostics"
    if diag_dir.exists():
        for df in diag_dir.glob("*.json"):
            subject = df.stem
            diag_data = safe_json_load(df)
            if not diag_data:
                continue
            stats.inc("atlas_diagnostics")
            if not dry_run:
                try:
                    sb.table("atlas_diagnostics").upsert({
                        "profile_id": pid,
                        "subject": subject,
                        "status": diag_data.get("status", "completed"),
                        "data": diag_data,
                        "updated_at": now_iso(),
                    }, on_conflict="profile_id,subject").execute()
                except Exception as e:
                    stats.error(f"diagnostic [{student_id}/{subject}]: {e}")

    # 4. Sessions → atlas_sessions
    sessions_dir = student_dir / "sessions"
    if sessions_dir.exists():
        for sf in sessions_dir.glob("*.json"):
            subject = sf.stem
            messages = safe_json_load(sf, default=[])
            if not messages:
                continue
            stats.inc("atlas_sessions")
            if not dry_run:
                try:
                    sb.table("atlas_sessions").upsert({
                        "profile_id": pid,
                        "subject": subject,
                        "messages": messages,
                        "updated_at": now_iso(),
                    }, on_conflict="profile_id,subject").execute()
                except Exception as e:
                    stats.error(f"session [{student_id}/{subject}]: {e}")

    # 5. Lessons → atlas_lessons + atlas_lesson_log
    lessons_dir = student_dir / "lessons"
    if lessons_dir.exists():
        for subj_dir in lessons_dir.iterdir():
            if not subj_dir.is_dir():
                continue
            subject = subj_dir.name

            # Lesson log
            log_path = subj_dir / "_log.json"
            log_data = safe_json_load(log_path, default=[])
            if log_data:
                stats.inc("atlas_lesson_log")
                if not dry_run:
                    try:
                        sb.table("atlas_lesson_log").upsert({
                            "profile_id": pid,
                            "subject": subject,
                            "data": log_data,
                            "updated_at": now_iso(),
                        }, on_conflict="profile_id,subject").execute()
                    except Exception as e:
                        stats.error(f"lesson_log [{student_id}/{subject}]: {e}")

            # Individual lessons
            for lf in subj_dir.glob("*.json"):
                if lf.name == "_log.json":
                    continue
                lesson_id = lf.stem
                lesson_data = safe_json_load(lf)
                if not lesson_data:
                    continue
                stats.inc("atlas_lessons")
                if not dry_run:
                    try:
                        sb.table("atlas_lessons").upsert({
                            "profile_id": pid,
                            "subject": subject,
                            "lesson_id": lesson_id,
                            "data": lesson_data,
                            "updated_at": now_iso(),
                        }, on_conflict="profile_id,subject,lesson_id").execute()
                    except Exception as e:
                        stats.error(f"lesson [{student_id}/{subject}/{lesson_id}]: {e}")

    # 6. Practice → atlas_practice_sessions + atlas_practice_log
    practice_dir = student_dir / "practice"
    if practice_dir.exists():
        for subj_dir in practice_dir.iterdir():
            if not subj_dir.is_dir():
                continue
            subject = subj_dir.name

            # Practice log
            log_path = subj_dir / "_log.json"
            log_data = safe_json_load(log_path, default=[])
            if log_data:
                stats.inc("atlas_practice_log")
                if not dry_run:
                    try:
                        sb.table("atlas_practice_log").upsert({
                            "profile_id": pid,
                            "subject": subject,
                            "data": log_data,
                            "updated_at": now_iso(),
                        }, on_conflict="profile_id,subject").execute()
                    except Exception as e:
                        stats.error(f"practice_log [{student_id}/{subject}]: {e}")

            # Individual practice sessions
            for pf in subj_dir.glob("*.json"):
                if pf.name == "_log.json":
                    continue
                practice_id = pf.stem
                practice_data = safe_json_load(pf)
                if not practice_data:
                    continue
                stats.inc("atlas_practice_sessions")
                if not dry_run:
                    try:
                        sb.table("atlas_practice_sessions").upsert({
                            "profile_id": pid,
                            "subject": subject,
                            "practice_id": practice_id,
                            "data": practice_data,
                            "updated_at": now_iso(),
                        }, on_conflict="profile_id,subject,practice_id").execute()
                    except Exception as e:
                        stats.error(f"practice [{student_id}/{subject}/{practice_id}]: {e}")

    # 7. Reassessment meta → atlas_reassessment_meta
    reassess_path = student_dir / "reassessments" / "_meta.json"
    if reassess_path.exists():
        meta = safe_json_load(reassess_path)
        if meta:
            stats.inc("atlas_reassessment_meta")
            if not dry_run:
                try:
                    sb.table("atlas_reassessment_meta").upsert({
                        "profile_id": pid,
                        "data": meta,
                        "updated_at": now_iso(),
                    }, on_conflict="profile_id").execute()
                except Exception as e:
                    stats.error(f"reassessment_meta [{student_id}]: {e}")


def migrate_admin_data(sb, stats: MigrationStats, dry_run: bool):
    """Migrate admin safety notes and invites → atlas_admin_data."""
    # Admin safety notes
    notes_path = DATA_DIR / "admin_safety_notes.json"
    if notes_path.exists():
        notes = safe_json_load(notes_path)
        if notes:
            stats.inc("atlas_admin_data")
            if not dry_run:
                try:
                    sb.table("atlas_admin_data").upsert({
                        "key": "admin_safety_notes",
                        "data": notes,
                        "updated_at": now_iso(),
                    }, on_conflict="key").execute()
                except Exception as e:
                    stats.error(f"admin_safety_notes: {e}")

    # Also check admin/ subdirectory
    alt_notes = DATA_DIR / "admin" / "safety_notes.json"
    if alt_notes.exists():
        notes = safe_json_load(alt_notes)
        if notes:
            stats.inc("atlas_admin_data")
            if not dry_run:
                try:
                    sb.table("atlas_admin_data").upsert({
                        "key": "admin_safety_notes_alt",
                        "data": notes,
                        "updated_at": now_iso(),
                    }, on_conflict="key").execute()
                except Exception as e:
                    stats.error(f"admin_safety_notes_alt: {e}")

    # Invites
    invites_path = DATA_DIR / "invites.json"
    if invites_path.exists():
        invites = safe_json_load(invites_path, default=[])
        if invites:
            stats.inc("atlas_admin_data")
            if not dry_run:
                try:
                    sb.table("atlas_admin_data").upsert({
                        "key": "invites",
                        "data": {"invites": invites},
                        "updated_at": now_iso(),
                    }, on_conflict="key").execute()
                except Exception as e:
                    stats.error(f"invites: {e}")


def migrate_instances_registry(sb, stats: MigrationStats, dry_run: bool):
    """Migrate instances.json registry → atlas_admin_data."""
    reg_path = INSTANCES_DIR / "instances.json"
    data = safe_json_load(reg_path)
    if not data:
        return

    stats.inc("atlas_admin_data")
    if not dry_run:
        try:
            sb.table("atlas_admin_data").upsert({
                "key": "instances_registry",
                "data": data,
                "updated_at": now_iso(),
            }, on_conflict="key").execute()
        except Exception as e:
            stats.error(f"instances_registry: {e}")


# ─── Main Orchestrator ──────────────────────────────────────────

def discover_instances() -> list[str]:
    """Find all instance IDs from the instances directory."""
    if not INSTANCES_DIR.exists():
        return []
    instances = []
    for d in INSTANCES_DIR.iterdir():
        if d.is_dir() and d.name != "__pycache__":
            instances.append(d.name)
    return sorted(instances)


def discover_students(instance_id: str) -> list[tuple[str, dict]]:
    """Find all students for an instance. Returns [(student_id, student_data)]."""
    students = []

    # Instance-scoped students
    students_dir = INSTANCES_DIR / instance_id / "students"
    if students_dir.exists():
        for f in students_dir.glob("*.json"):
            data = safe_json_load(f)
            if isinstance(data, dict):
                sid = data.get("student_id", f.stem)
                students.append((sid, data))

    return students


def discover_legacy_students() -> list[tuple[str, dict]]:
    """Find students in the legacy flat data/students/ directory."""
    students = []
    if not STUDENTS_DIR.exists():
        return students
    for f in STUDENTS_DIR.glob("*.json"):
        data = safe_json_load(f)
        if isinstance(data, dict):
            sid = data.get("student_id", f.stem)
            students.append((sid, data))
    return students


def run_migration(args):
    mode_label = "DRY RUN" if args.dry_run else "LIVE"
    print(f"\n{'═' * 50}")
    print(f"  Atlas JSON → Supabase Migration ({mode_label})")
    print(f"  Data dir: {DATA_DIR}")
    print(f"  ID mode:  {args.id_mode}")
    print(f"{'═' * 50}\n")

    sb = None if args.dry_run else get_supabase()
    mapper = IdMapper(sb, mode=args.id_mode)

    if not args.dry_run and args.id_mode == "bridge":
        print("Building ID mappings from Supabase...")
        mapper.build_maps()

    stats = MigrationStats()

    # 1. Discover instances
    if args.instance:
        instances = [args.instance]
    else:
        instances = discover_instances()

    if not instances:
        print("No instances found. Checking legacy flat structure...")

    print(f"Found {len(instances)} instance(s): {', '.join(instances)}\n")

    # 2. Migrate instances registry
    print("─── Instances Registry ───")
    migrate_instances_registry(sb, stats, args.dry_run)

    # 3. Migrate admin data (invites, safety notes)
    print("─── Admin Data ───")
    migrate_admin_data(sb, stats, args.dry_run)

    # 4. Migrate each instance
    for inst_id in instances:
        print(f"\n─── Instance: {inst_id} ───")

        migrate_instance_config(sb, mapper, inst_id, stats, args.dry_run)
        migrate_parent_config(sb, mapper, inst_id, stats, args.dry_run)
        migrate_diagnostics_pending(sb, mapper, inst_id, stats, args.dry_run)

        students = discover_students(inst_id)
        print(f"  Found {len(students)} student(s)")

        for sid, sdata in students:
            print(f"  → Migrating student: {sdata.get('name', sid)} ({sid})")
            migrate_student(sb, mapper, inst_id, sid, sdata, stats, args.dry_run)

    # 5. Migrate legacy flat students (not in any instance)
    legacy = discover_legacy_students()
    if legacy:
        print(f"\n─── Legacy Students (flat) ───")
        print(f"  Found {len(legacy)} legacy student(s)")
        for sid, sdata in legacy:
            print(f"  → Migrating legacy student: {sdata.get('name', sid)} ({sid})")
            migrate_student(sb, mapper, "default", sid, sdata, stats, args.dry_run)

    # 6. Summary
    stats.summary()

    if args.dry_run:
        print(f"\n  ℹ  This was a DRY RUN. No data was written.")
        print(f"  ℹ  Run without --dry-run to perform the migration.\n")
    else:
        print(f"\n  ✓  Migration complete!\n")

    return 0 if not stats.errors else 1


# ─── CLI ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Migrate Atlas JSON data to Supabase")
    parser.add_argument("--dry-run", action="store_true",
                        help="Count records without writing to Supabase")
    parser.add_argument("--instance", type=str, default=None,
                        help="Migrate a single instance (e.g., 'default')")
    parser.add_argument("--id-mode", choices=["standalone", "bridge"], default="standalone",
                        help="ID mapping mode: 'standalone' uses Atlas IDs as-is, "
                             "'bridge' looks up KmUnity profile UUIDs")
    args = parser.parse_args()
    sys.exit(run_migration(args))


if __name__ == "__main__":
    main()
