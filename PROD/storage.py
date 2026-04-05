"""
Atlas Storage Abstraction Layer

Provides a unified interface for Atlas data persistence with two implementations:
  - FileStorage: File-based JSON (standalone dev, default)
  - SupabaseStorage: Supabase tables (production on KmUnity/Railway)

Switch via STORAGE_BACKEND env var: "file" (default) or "supabase"

Usage in app.py:
    from storage import get_storage
    storage = get_storage()
    profile = storage.load_profile("math", student_id, instance_id)
"""

import json
import os
import shutil
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path


# ─── Base Interface ─────────────────────────────────────────────


class StorageBackend(ABC):
    """Abstract interface for Atlas data persistence."""

    # ── Student metadata ──

    @abstractmethod
    def load_student(self, student_id: str, instance_id: str = None) -> dict | None:
        """Load student metadata (name, grade, avatar, badges, XP, etc.)."""

    @abstractmethod
    def save_student(self, student_id: str, data: dict, instance_id: str = None):
        """Save student metadata."""

    @abstractmethod
    def list_students(self, instance_id: str = None) -> list:
        """List all students (without PINs)."""

    # ── Subject profiles (per-student per-subject learning state) ──

    @abstractmethod
    def load_profile(self, subject: str, student_id: str = None, instance_id: str = None) -> dict | None:
        """Load a student's learning profile for a subject."""

    @abstractmethod
    def save_profile(self, subject: str, profile: dict, student_id: str = None, instance_id: str = None):
        """Save a student's learning profile for a subject."""

    # ── Diagnostics ──

    @abstractmethod
    def load_diagnostic(self, subject: str, student_id: str = None, instance_id: str = None) -> dict | None:
        """Load diagnostic state for a subject."""

    @abstractmethod
    def save_diagnostic(self, subject: str, state: dict, student_id: str = None, instance_id: str = None):
        """Save diagnostic state for a subject."""

    # ── Conversation sessions ──

    @abstractmethod
    def load_session(self, subject: str, student_id: str = None, instance_id: str = None) -> list:
        """Load conversation messages for a subject."""

    @abstractmethod
    def save_session(self, subject: str, messages: list, student_id: str = None, instance_id: str = None):
        """Save conversation messages for a subject."""

    # ── Lessons ──

    @abstractmethod
    def load_lesson(self, subject: str, lesson_id: str, student_id: str = None, instance_id: str = None) -> dict | None:
        """Load a specific lesson state."""

    @abstractmethod
    def save_lesson(self, subject: str, lesson_id: str, state: dict, student_id: str = None, instance_id: str = None):
        """Save a specific lesson state."""

    @abstractmethod
    def load_lesson_log(self, subject: str, student_id: str = None, instance_id: str = None) -> list:
        """Load the lesson log (list of all lessons taken for a subject)."""

    @abstractmethod
    def save_lesson_log(self, subject: str, log: list, student_id: str = None, instance_id: str = None):
        """Save the lesson log for a subject."""

    # ── Practice ──

    @abstractmethod
    def load_practice(self, subject: str, practice_id: str, student_id: str = None, instance_id: str = None) -> dict | None:
        """Load a specific practice session state."""

    @abstractmethod
    def save_practice(self, subject: str, practice_id: str, state: dict, student_id: str = None, instance_id: str = None):
        """Save a specific practice session state."""

    @abstractmethod
    def load_practice_log(self, subject: str, student_id: str = None, instance_id: str = None) -> list:
        """Load the practice log (list of all practice sessions for a subject)."""

    @abstractmethod
    def save_practice_log(self, subject: str, log: list, student_id: str = None, instance_id: str = None):
        """Save the practice log for a subject."""

    # ── Instance config ──

    @abstractmethod
    def load_instance_config(self, instance_id: str) -> dict:
        """Load instance configuration."""

    @abstractmethod
    def save_instance_config(self, instance_id: str, config: dict):
        """Save instance configuration."""

    @abstractmethod
    def load_instance_parent_config(self, instance_id: str) -> dict:
        """Load parent configuration for an instance."""

    @abstractmethod
    def save_instance_parent_config(self, instance_id: str, config: dict):
        """Save parent configuration for an instance."""

    @abstractmethod
    def load_instances_registry(self) -> list:
        """Load the registry of all instances."""

    @abstractmethod
    def save_instances_registry(self, instances: list):
        """Save the registry of all instances."""

    # ── Diagnostics pending (instance-level) ──

    @abstractmethod
    def load_diagnostics_pending(self, instance_id: str) -> dict:
        """Load pending diagnostics for an instance."""

    @abstractmethod
    def save_diagnostics_pending(self, instance_id: str, data: dict):
        """Save pending diagnostics for an instance."""

    # ── Reassessment ──

    @abstractmethod
    def load_reassessment_meta(self, student_id: str, instance_id: str = None) -> dict:
        """Load reassessment scheduling metadata."""

    @abstractmethod
    def save_reassessment_meta(self, student_id: str, meta: dict, instance_id: str = None):
        """Save reassessment scheduling metadata."""

    # ── Admin / safety ──

    @abstractmethod
    def load_admin_safety_notes(self) -> dict:
        """Load admin safety notes."""

    @abstractmethod
    def save_admin_safety_notes(self, notes: dict):
        """Save admin safety notes."""

    # ── Invites ──

    @abstractmethod
    def load_invites(self) -> list:
        """Load invite list."""

    @abstractmethod
    def save_invites(self, invites: list):
        """Save invite list."""

    # ── Complexity tiers ──

    @abstractmethod
    def save_complexity_tier(self, student_id: str, subject: str, tier: int, instance_id: str = None):
        """Save a student's complexity tier for a subject."""

    # ── Parent config (legacy flat) ──

    @abstractmethod
    def load_parent_config(self) -> dict:
        """Load legacy parent config."""

    @abstractmethod
    def save_parent_config(self, config: dict):
        """Save legacy parent config."""


# ─── File-based Implementation ─────────────────────────────────


class FileStorage(StorageBackend):
    """File-based JSON storage — wraps the existing Atlas file I/O pattern.

    This is the default storage backend for standalone development.
    It preserves the exact directory structure and file format Atlas has always used.
    """

    def __init__(self, base_dir: str = "data"):
        self.base = Path(base_dir)
        self.students_dir = self.base / "students"
        self.sessions_dir = self.base / "sessions"
        self.profiles_dir = self.base / "profiles"
        self.diagnostics_dir = self.base / "diagnostics"
        self.lessons_dir = self.base / "lessons"
        self.practice_dir = self.base / "practice"
        self.instances_dir = self.base / "instances"
        self.instances_registry_path = self.instances_dir / "instances.json"
        self.admin_dir = self.base / "admin"

        # Ensure directories exist
        for d in [self.students_dir, self.sessions_dir, self.profiles_dir,
                  self.diagnostics_dir, self.lessons_dir, self.practice_dir,
                  self.instances_dir, self.admin_dir]:
            d.mkdir(parents=True, exist_ok=True)

    # ── Helpers ──

    def _safe_json_load(self, path: Path, default=None):
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
            print(f"⚠️  Corrupted JSON in {path}: {e} — returning default")
            try:
                backup = path.with_suffix(path.suffix + ".corrupt")
                if path.exists():
                    shutil.copy2(path, backup)
            except OSError:
                pass
            return default

    def _atomic_write(self, path: Path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        try:
            tmp.write_text(json.dumps(data, indent=2))
            tmp.rename(path)
        except IOError:
            if tmp.exists():
                tmp.unlink()

    def _students_base(self, instance_id: str = None) -> Path:
        if instance_id:
            d = self.instances_dir / instance_id / "students"
            d.mkdir(parents=True, exist_ok=True)
            return d
        return self.students_dir

    def _student_data_dir(self, student_id: str, instance_id: str = None) -> Path:
        d = self._students_base(instance_id) / student_id
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _get_student_dirs(self, student_id: str | None, instance_id: str = None) -> dict:
        if student_id:
            base = self._student_data_dir(student_id, instance_id)
            dirs = {
                "sessions": base / "sessions",
                "profiles": base / "profiles",
                "diagnostics": base / "diagnostics",
                "lessons": base / "lessons",
                "practice": base / "practice",
            }
            for d in dirs.values():
                d.mkdir(parents=True, exist_ok=True)
            return dirs
        return {
            "sessions": self.sessions_dir,
            "profiles": self.profiles_dir,
            "diagnostics": self.diagnostics_dir,
            "lessons": self.lessons_dir,
            "practice": self.practice_dir,
        }

    def _instance_path(self, instance_id: str) -> Path:
        d = self.instances_dir / instance_id
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _reassessment_dir(self, student_id: str, instance_id: str = None) -> Path:
        d = self._student_data_dir(student_id, instance_id) / "reassessments"
        d.mkdir(parents=True, exist_ok=True)
        return d

    # ── Student metadata ──

    def load_student(self, student_id: str, instance_id: str = None) -> dict | None:
        base = self._students_base(instance_id)
        path = base / f"{student_id}.json"
        data = self._safe_json_load(path, default=None)
        return data if isinstance(data, dict) else None

    def save_student(self, student_id: str, data: dict, instance_id: str = None):
        base = self._students_base(instance_id)
        self._atomic_write(base / f"{student_id}.json", data)

    def list_students(self, instance_id: str = None) -> list:
        base = self._students_base(instance_id)
        students = []
        for f in base.glob("*.json"):
            data = self._safe_json_load(f, default=None)
            if isinstance(data, dict):
                students.append({
                    "student_id": data.get("student_id", f.stem),
                    "name": data.get("name", "Student"),
                    "avatar": data.get("avatar", "\U0001f393"),
                    "grade": data.get("grade", 8),
                    "created_at": data.get("created_at"),
                })
        return students

    # ── Subject profiles ──

    def load_profile(self, subject: str, student_id: str = None, instance_id: str = None) -> dict | None:
        dirs = self._get_student_dirs(student_id, instance_id)
        path = dirs["profiles"] / f"{subject}.json"
        if not path.exists():
            return None
        data = self._safe_json_load(path, default=None)
        if not data or not isinstance(data, dict):
            return None
        return data

    def save_profile(self, subject: str, profile: dict, student_id: str = None, instance_id: str = None):
        dirs = self._get_student_dirs(student_id, instance_id)
        self._atomic_write(dirs["profiles"] / f"{subject}.json", profile)

    # ── Diagnostics ──

    def load_diagnostic(self, subject: str, student_id: str = None, instance_id: str = None) -> dict | None:
        dirs = self._get_student_dirs(student_id, instance_id)
        data = self._safe_json_load(dirs["diagnostics"] / f"{subject}.json", default=None)
        return data if isinstance(data, dict) else None

    def save_diagnostic(self, subject: str, state: dict, student_id: str = None, instance_id: str = None):
        dirs = self._get_student_dirs(student_id, instance_id)
        self._atomic_write(dirs["diagnostics"] / f"{subject}.json", state)

    # ── Sessions ──

    def load_session(self, subject: str, student_id: str = None, instance_id: str = None) -> list:
        dirs = self._get_student_dirs(student_id, instance_id)
        data = self._safe_json_load(dirs["sessions"] / f"{subject}.json", default=[])
        return data if isinstance(data, list) else []

    def save_session(self, subject: str, messages: list, student_id: str = None, instance_id: str = None):
        dirs = self._get_student_dirs(student_id, instance_id)
        self._atomic_write(dirs["sessions"] / f"{subject}.json", messages)

    # ── Lessons ──

    def _lesson_dir(self, subject: str, student_id: str = None, instance_id: str = None) -> Path:
        dirs = self._get_student_dirs(student_id, instance_id)
        d = dirs["lessons"] / subject
        d.mkdir(parents=True, exist_ok=True)
        return d

    def load_lesson(self, subject: str, lesson_id: str, student_id: str = None, instance_id: str = None) -> dict | None:
        path = self._lesson_dir(subject, student_id, instance_id) / f"{lesson_id}.json"
        data = self._safe_json_load(path, default=None)
        return data if isinstance(data, dict) else None

    def save_lesson(self, subject: str, lesson_id: str, state: dict, student_id: str = None, instance_id: str = None):
        self._atomic_write(
            self._lesson_dir(subject, student_id, instance_id) / f"{lesson_id}.json", state
        )

    def load_lesson_log(self, subject: str, student_id: str = None, instance_id: str = None) -> list:
        path = self._lesson_dir(subject, student_id, instance_id) / "_log.json"
        data = self._safe_json_load(path, default=[])
        return data if isinstance(data, list) else []

    def save_lesson_log(self, subject: str, log: list, student_id: str = None, instance_id: str = None):
        self._atomic_write(
            self._lesson_dir(subject, student_id, instance_id) / "_log.json", log
        )

    # ── Practice ──

    def _practice_dir(self, subject: str, student_id: str = None, instance_id: str = None) -> Path:
        dirs = self._get_student_dirs(student_id, instance_id)
        d = dirs["practice"] / subject
        d.mkdir(parents=True, exist_ok=True)
        return d

    def load_practice(self, subject: str, practice_id: str, student_id: str = None, instance_id: str = None) -> dict | None:
        path = self._practice_dir(subject, student_id, instance_id) / f"{practice_id}.json"
        data = self._safe_json_load(path, default=None)
        return data if isinstance(data, dict) else None

    def save_practice(self, subject: str, practice_id: str, state: dict, student_id: str = None, instance_id: str = None):
        self._atomic_write(
            self._practice_dir(subject, student_id, instance_id) / f"{practice_id}.json", state
        )

    def load_practice_log(self, subject: str, student_id: str = None, instance_id: str = None) -> list:
        path = self._practice_dir(subject, student_id, instance_id) / "_log.json"
        data = self._safe_json_load(path, default=[])
        return data if isinstance(data, list) else []

    def save_practice_log(self, subject: str, log: list, student_id: str = None, instance_id: str = None):
        self._atomic_write(
            self._practice_dir(subject, student_id, instance_id) / "_log.json", log
        )

    # ── Instance config ──

    def load_instance_config(self, instance_id: str) -> dict:
        path = self._instance_path(instance_id) / "instance_config.json"
        return self._safe_json_load(path, default={})

    def save_instance_config(self, instance_id: str, config: dict):
        self._atomic_write(self._instance_path(instance_id) / "instance_config.json", config)

    def load_instance_parent_config(self, instance_id: str) -> dict:
        path = self._instance_path(instance_id) / "parent_config.json"
        return self._safe_json_load(path, default={})

    def save_instance_parent_config(self, instance_id: str, config: dict):
        self._atomic_write(self._instance_path(instance_id) / "parent_config.json", config)

    def load_instances_registry(self) -> list:
        data = self._safe_json_load(self.instances_registry_path, default={"instances": []})
        return data.get("instances", [])

    def save_instances_registry(self, instances: list):
        self._atomic_write(self.instances_registry_path, {"instances": instances})

    # ── Diagnostics pending ──

    def load_diagnostics_pending(self, instance_id: str) -> dict:
        path = self._instance_path(instance_id) / "diagnostics_pending.json"
        return self._safe_json_load(path, default={})

    def save_diagnostics_pending(self, instance_id: str, data: dict):
        self._atomic_write(self._instance_path(instance_id) / "diagnostics_pending.json", data)

    # ── Reassessment ──

    def load_reassessment_meta(self, student_id: str, instance_id: str = None) -> dict:
        path = self._reassessment_dir(student_id, instance_id) / "_meta.json"
        default = {
            "interval_weeks": 4,
            "enabled": True,
            "snoozed_until": None,
            "history": [],
        }
        data = self._safe_json_load(path, default=default)
        for k, v in default.items():
            if k not in data:
                data[k] = v
        return data

    def save_reassessment_meta(self, student_id: str, meta: dict, instance_id: str = None):
        self._atomic_write(self._reassessment_dir(student_id, instance_id) / "_meta.json", meta)

    # ── Admin / safety ──

    def load_admin_safety_notes(self) -> dict:
        path = self.admin_dir / "safety_notes.json"
        return self._safe_json_load(path, default={})

    def save_admin_safety_notes(self, notes: dict):
        self._atomic_write(self.admin_dir / "safety_notes.json", notes)

    # ── Invites ──

    def load_invites(self) -> list:
        path = self.base / "invites.json"
        data = self._safe_json_load(path, default=[])
        return data if isinstance(data, list) else []

    def save_invites(self, invites: list):
        self._atomic_write(self.base / "invites.json", invites)

    # ── Complexity tiers ──

    def save_complexity_tier(self, student_id: str, subject: str, tier: int, instance_id: str = None):
        student = self.load_student(student_id, instance_id)
        if student:
            ct = student.get("complexity_tiers", {})
            ct[subject] = tier
            student["complexity_tiers"] = ct
            self.save_student(student_id, student, instance_id)

    # ── Parent config (legacy flat) ──

    def load_parent_config(self) -> dict:
        path = self.base / "parent_config.json"
        return self._safe_json_load(path, default={})

    def save_parent_config(self, config: dict):
        self._atomic_write(self.base / "parent_config.json", config)


# ─── Supabase Implementation ──────────────────────────────────


class SupabaseStorage(StorageBackend):
    """Supabase-backed storage for production (KmUnity platform).

    Uses the Supabase service role client to read/write Atlas data tables.
    This backend is used when STORAGE_BACKEND=supabase.

    Table mapping:
      - Student metadata → profiles table (KmUnity) + atlas_students
      - Subject profiles → atlas_profiles
      - Diagnostics → atlas_diagnostics
      - Practice → atlas_practice_history + atlas_practice_sessions
      - Lessons → atlas_lessons + atlas_lesson_log
      - Sessions → atlas_sessions
      - Instance config → families + atlas_instance_config
      - Focus → atlas_focus_overrides
      - Reassessment → atlas_reassessment_meta
    """

    def __init__(self, url: str, key: str):
        try:
            from supabase import create_client
            self.client = create_client(url, key)
            print("✓ SupabaseStorage initialized")
        except ImportError:
            raise ImportError(
                "supabase-py is required for SupabaseStorage. "
                "Install with: pip install supabase"
            )

    def _table(self, name: str):
        return self.client.table(name)

    # ── Student metadata ──

    def load_student(self, student_id: str, instance_id: str = None) -> dict | None:
        try:
            result = self._table("atlas_students").select("*").eq("profile_id", student_id).maybe_single().execute()
            return result.data if result.data else None
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_student error: {e}")
            return None

    def save_student(self, student_id: str, data: dict, instance_id: str = None):
        try:
            row = {
                "profile_id": student_id,
                "family_id": instance_id,
                "data": data,
                "updated_at": datetime.now().isoformat(),
            }
            self._table("atlas_students").upsert(row, on_conflict="profile_id").execute()
        except Exception as e:
            print(f"⚠ SupabaseStorage.save_student error: {e}")

    def list_students(self, instance_id: str = None) -> list:
        try:
            query = self._table("atlas_students").select("profile_id, data")
            if instance_id:
                query = query.eq("family_id", instance_id)
            result = query.execute()
            students = []
            for row in (result.data or []):
                d = row.get("data", {})
                students.append({
                    "student_id": row["profile_id"],
                    "name": d.get("name", "Student"),
                    "avatar": d.get("avatar", "\U0001f393"),
                    "grade": d.get("grade", 8),
                    "created_at": d.get("created_at"),
                })
            return students
        except Exception as e:
            print(f"⚠ SupabaseStorage.list_students error: {e}")
            return []

    # ── Subject profiles ──

    def load_profile(self, subject: str, student_id: str = None, instance_id: str = None) -> dict | None:
        if not student_id:
            return None
        try:
            result = (self._table("atlas_profiles")
                      .select("*")
                      .eq("profile_id", student_id)
                      .eq("subject", subject)
                      .maybe_single()
                      .execute())
            if result.data:
                # Reconstruct the profile dict from Supabase columns
                row = result.data
                return {
                    "subject": row["subject"],
                    "grade": row.get("grade"),
                    "topics": row.get("topics", {}),
                    "proficiency": row.get("proficiency", {}),
                    "current_lesson": row.get("current_lesson", {}),
                    "preferences": row.get("preferences", {}),
                    **(row.get("extra_data", {}) or {}),
                }
            return None
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_profile error: {e}")
            return None

    def save_profile(self, subject: str, profile: dict, student_id: str = None, instance_id: str = None):
        if not student_id:
            return
        try:
            # Separate known columns from extra data
            known_keys = {"subject", "grade", "topics", "proficiency", "current_lesson", "preferences"}
            extra = {k: v for k, v in profile.items() if k not in known_keys}
            row = {
                "profile_id": student_id,
                "family_id": instance_id,
                "subject": subject,
                "grade": profile.get("grade"),
                "topics": profile.get("topics", {}),
                "proficiency": profile.get("proficiency", {}),
                "current_lesson": profile.get("current_lesson", {}),
                "preferences": profile.get("preferences", {}),
                "extra_data": extra if extra else None,
                "updated_at": datetime.now().isoformat(),
            }
            self._table("atlas_profiles").upsert(row, on_conflict="profile_id,subject").execute()
        except Exception as e:
            print(f"⚠ SupabaseStorage.save_profile error: {e}")

    # ── Diagnostics ──

    def load_diagnostic(self, subject: str, student_id: str = None, instance_id: str = None) -> dict | None:
        if not student_id:
            return None
        try:
            result = (self._table("atlas_diagnostics")
                      .select("data")
                      .eq("profile_id", student_id)
                      .eq("subject", subject)
                      .order("created_at", desc=True)
                      .limit(1)
                      .maybe_single()
                      .execute())
            return result.data["data"] if result.data else None
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_diagnostic error: {e}")
            return None

    def save_diagnostic(self, subject: str, state: dict, student_id: str = None, instance_id: str = None):
        if not student_id:
            return
        try:
            # Upsert by profile_id + subject (most recent)
            row = {
                "profile_id": student_id,
                "subject": subject,
                "data": state,
                "status": state.get("status", "in_progress"),
                "updated_at": datetime.now().isoformat(),
            }
            self._table("atlas_diagnostics").upsert(row, on_conflict="profile_id,subject").execute()
        except Exception as e:
            print(f"⚠ SupabaseStorage.save_diagnostic error: {e}")

    # ── Sessions ──

    def load_session(self, subject: str, student_id: str = None, instance_id: str = None) -> list:
        if not student_id:
            return []
        try:
            result = (self._table("atlas_sessions")
                      .select("messages")
                      .eq("profile_id", student_id)
                      .eq("subject", subject)
                      .maybe_single()
                      .execute())
            return result.data["messages"] if result.data else []
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_session error: {e}")
            return []

    def save_session(self, subject: str, messages: list, student_id: str = None, instance_id: str = None):
        if not student_id:
            return
        try:
            row = {
                "profile_id": student_id,
                "subject": subject,
                "messages": messages,
                "updated_at": datetime.now().isoformat(),
            }
            self._table("atlas_sessions").upsert(row, on_conflict="profile_id,subject").execute()
        except Exception as e:
            print(f"⚠ SupabaseStorage.save_session error: {e}")

    # ── Lessons ──

    def load_lesson(self, subject: str, lesson_id: str, student_id: str = None, instance_id: str = None) -> dict | None:
        if not student_id:
            return None
        try:
            result = (self._table("atlas_lessons")
                      .select("data")
                      .eq("profile_id", student_id)
                      .eq("subject", subject)
                      .eq("lesson_id", lesson_id)
                      .maybe_single()
                      .execute())
            return result.data["data"] if result.data else None
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_lesson error: {e}")
            return None

    def save_lesson(self, subject: str, lesson_id: str, state: dict, student_id: str = None, instance_id: str = None):
        if not student_id:
            return
        try:
            row = {
                "profile_id": student_id,
                "subject": subject,
                "lesson_id": lesson_id,
                "data": state,
                "updated_at": datetime.now().isoformat(),
            }
            self._table("atlas_lessons").upsert(row, on_conflict="profile_id,subject,lesson_id").execute()
        except Exception as e:
            print(f"⚠ SupabaseStorage.save_lesson error: {e}")

    def load_lesson_log(self, subject: str, student_id: str = None, instance_id: str = None) -> list:
        if not student_id:
            return []
        try:
            result = (self._table("atlas_lesson_log")
                      .select("data")
                      .eq("profile_id", student_id)
                      .eq("subject", subject)
                      .maybe_single()
                      .execute())
            return result.data["data"] if result.data else []
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_lesson_log error: {e}")
            return []

    def save_lesson_log(self, subject: str, log: list, student_id: str = None, instance_id: str = None):
        if not student_id:
            return
        try:
            row = {
                "profile_id": student_id,
                "subject": subject,
                "data": log,
                "updated_at": datetime.now().isoformat(),
            }
            self._table("atlas_lesson_log").upsert(row, on_conflict="profile_id,subject").execute()
        except Exception as e:
            print(f"⚠ SupabaseStorage.save_lesson_log error: {e}")

    # ── Practice ──

    def load_practice(self, subject: str, practice_id: str, student_id: str = None, instance_id: str = None) -> dict | None:
        if not student_id:
            return None
        try:
            result = (self._table("atlas_practice_sessions")
                      .select("data")
                      .eq("profile_id", student_id)
                      .eq("subject", subject)
                      .eq("practice_id", practice_id)
                      .maybe_single()
                      .execute())
            return result.data["data"] if result.data else None
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_practice error: {e}")
            return None

    def save_practice(self, subject: str, practice_id: str, state: dict, student_id: str = None, instance_id: str = None):
        if not student_id:
            return
        try:
            row = {
                "profile_id": student_id,
                "subject": subject,
                "practice_id": practice_id,
                "data": state,
                "updated_at": datetime.now().isoformat(),
            }
            self._table("atlas_practice_sessions").upsert(row, on_conflict="profile_id,subject,practice_id").execute()
        except Exception as e:
            print(f"⚠ SupabaseStorage.save_practice error: {e}")

    def load_practice_log(self, subject: str, student_id: str = None, instance_id: str = None) -> list:
        if not student_id:
            return []
        try:
            result = (self._table("atlas_practice_log")
                      .select("data")
                      .eq("profile_id", student_id)
                      .eq("subject", subject)
                      .maybe_single()
                      .execute())
            return result.data["data"] if result.data else []
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_practice_log error: {e}")
            return []

    def save_practice_log(self, subject: str, log: list, student_id: str = None, instance_id: str = None):
        if not student_id:
            return
        try:
            row = {
                "profile_id": student_id,
                "subject": subject,
                "data": log,
                "updated_at": datetime.now().isoformat(),
            }
            self._table("atlas_practice_log").upsert(row, on_conflict="profile_id,subject").execute()
        except Exception as e:
            print(f"⚠ SupabaseStorage.save_practice_log error: {e}")

    # ── Instance config ──
    # In Supabase mode, instance_id maps to family_id in KmUnity

    def load_instance_config(self, instance_id: str) -> dict:
        try:
            result = (self._table("atlas_instance_config")
                      .select("data")
                      .eq("family_id", instance_id)
                      .maybe_single()
                      .execute())
            return result.data["data"] if result.data else {}
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_instance_config error: {e}")
            return {}

    def save_instance_config(self, instance_id: str, config: dict):
        try:
            row = {
                "family_id": instance_id,
                "data": config,
                "updated_at": datetime.now().isoformat(),
            }
            self._table("atlas_instance_config").upsert(row, on_conflict="family_id").execute()
        except Exception as e:
            print(f"⚠ SupabaseStorage.save_instance_config error: {e}")

    def load_instance_parent_config(self, instance_id: str) -> dict:
        try:
            result = (self._table("atlas_parent_config")
                      .select("data")
                      .eq("family_id", instance_id)
                      .maybe_single()
                      .execute())
            return result.data["data"] if result.data else {}
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_instance_parent_config error: {e}")
            return {}

    def save_instance_parent_config(self, instance_id: str, config: dict):
        try:
            row = {
                "family_id": instance_id,
                "data": config,
                "updated_at": datetime.now().isoformat(),
            }
            self._table("atlas_parent_config").upsert(row, on_conflict="family_id").execute()
        except Exception as e:
            print(f"⚠ SupabaseStorage.save_instance_parent_config error: {e}")

    def load_instances_registry(self) -> list:
        # In Supabase mode, instances = families. Pull from families table.
        try:
            result = self._table("families").select("id, name, created_by, created_at").execute()
            instances = []
            for row in (result.data or []):
                instances.append({
                    "instance_id": row["id"],
                    "family_name": row.get("name", "Family"),
                    "created_at": row.get("created_at"),
                })
            return instances
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_instances_registry error: {e}")
            return []

    def save_instances_registry(self, instances: list):
        # In Supabase mode, the families table IS the registry. No-op.
        pass

    # ── Diagnostics pending ──

    def load_diagnostics_pending(self, instance_id: str) -> dict:
        try:
            result = (self._table("atlas_diagnostics_pending")
                      .select("data")
                      .eq("family_id", instance_id)
                      .maybe_single()
                      .execute())
            return result.data["data"] if result.data else {}
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_diagnostics_pending error: {e}")
            return {}

    def save_diagnostics_pending(self, instance_id: str, data: dict):
        try:
            row = {
                "family_id": instance_id,
                "data": data,
                "updated_at": datetime.now().isoformat(),
            }
            self._table("atlas_diagnostics_pending").upsert(row, on_conflict="family_id").execute()
        except Exception as e:
            print(f"⚠ SupabaseStorage.save_diagnostics_pending error: {e}")

    # ── Reassessment ──

    def load_reassessment_meta(self, student_id: str, instance_id: str = None) -> dict:
        try:
            result = (self._table("atlas_reassessment_meta")
                      .select("data")
                      .eq("profile_id", student_id)
                      .maybe_single()
                      .execute())
            default = {
                "interval_weeks": 4,
                "enabled": True,
                "snoozed_until": None,
                "history": [],
            }
            if result.data:
                data = result.data["data"]
                for k, v in default.items():
                    if k not in data:
                        data[k] = v
                return data
            return default
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_reassessment_meta error: {e}")
            return {
                "interval_weeks": 4,
                "enabled": True,
                "snoozed_until": None,
                "history": [],
            }

    def save_reassessment_meta(self, student_id: str, meta: dict, instance_id: str = None):
        try:
            row = {
                "profile_id": student_id,
                "data": meta,
                "updated_at": datetime.now().isoformat(),
            }
            self._table("atlas_reassessment_meta").upsert(row, on_conflict="profile_id").execute()
        except Exception as e:
            print(f"⚠ SupabaseStorage.save_reassessment_meta error: {e}")

    # ── Admin / safety ──

    def load_admin_safety_notes(self) -> dict:
        try:
            result = (self._table("atlas_admin_data")
                      .select("data")
                      .eq("key", "safety_notes")
                      .maybe_single()
                      .execute())
            return result.data["data"] if result.data else {}
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_admin_safety_notes error: {e}")
            return {}

    def save_admin_safety_notes(self, notes: dict):
        try:
            row = {
                "key": "safety_notes",
                "data": notes,
                "updated_at": datetime.now().isoformat(),
            }
            self._table("atlas_admin_data").upsert(row, on_conflict="key").execute()
        except Exception as e:
            print(f"⚠ SupabaseStorage.save_admin_safety_notes error: {e}")

    # ── Invites ──

    def load_invites(self) -> list:
        try:
            result = (self._table("atlas_admin_data")
                      .select("data")
                      .eq("key", "invites")
                      .maybe_single()
                      .execute())
            data = result.data["data"] if result.data else []
            return data if isinstance(data, list) else []
        except Exception as e:
            print(f"⚠ SupabaseStorage.load_invites error: {e}")
            return []

    def save_invites(self, invites: list):
        try:
            row = {
                "key": "invites",
                "data": invites,
                "updated_at": datetime.now().isoformat(),
            }
            self._table("atlas_admin_data").upsert(row, on_conflict="key").execute()
        except Exception as e:
            print(f"⚠ SupabaseStorage.save_invites error: {e}")

    # ── Complexity tiers ──

    def save_complexity_tier(self, student_id: str, subject: str, tier: int, instance_id: str = None):
        student = self.load_student(student_id, instance_id)
        if student:
            data = student.get("data", student)
            ct = data.get("complexity_tiers", {})
            ct[subject] = tier
            data["complexity_tiers"] = ct
            self.save_student(student_id, data, instance_id)

    # ── Parent config (legacy flat) ──

    def load_parent_config(self) -> dict:
        # In Supabase mode, parent config is per-instance. Use default instance.
        return self.load_instance_parent_config("default")

    def save_parent_config(self, config: dict):
        self.save_instance_parent_config("default", config)


# ─── Factory Function ──────────────────────────────────────────


def get_storage() -> StorageBackend:
    """Create and return the appropriate storage backend based on STORAGE_BACKEND env var."""
    backend = os.getenv("STORAGE_BACKEND", "file").lower()

    if backend == "supabase":
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not key:
            raise ValueError(
                "STORAGE_BACKEND=supabase requires SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY"
            )
        return SupabaseStorage(url, key)
    else:
        base_dir = os.getenv("ATLAS_DATA_DIR", "data")
        return FileStorage(base_dir)
