-- Migration 007b: Change Atlas tables from UUID to TEXT IDs
-- Atlas uses short hex IDs (e.g., "b0f6cfda", "aea9b4fb3810") that aren't
-- valid UUIDs. This migration drops FK constraints, RLS policies that
-- reference the columns, converts to TEXT, then recreates the RLS policies.
--
-- Run in Supabase SQL Editor AFTER 007_atlas_tables.sql
-- ============================================================

BEGIN;

-- ══════════════════════════════════════════════════
-- 1. Drop RLS policies that reference profile_id or family_id
-- ══════════════════════════════════════════════════

DROP POLICY IF EXISTS "Students read own atlas_profiles" ON atlas_profiles;
DROP POLICY IF EXISTS "Students read own atlas_diagnostics" ON atlas_diagnostics;
DROP POLICY IF EXISTS "Students read own atlas_sessions" ON atlas_sessions;
DROP POLICY IF EXISTS "Parents read family atlas_profiles" ON atlas_profiles;
DROP POLICY IF EXISTS "Parents read family atlas_students" ON atlas_students;

-- Also drop service role policies (they reference the table, safe to recreate)
DROP POLICY IF EXISTS "Service role atlas_students" ON atlas_students;
DROP POLICY IF EXISTS "Service role atlas_profiles" ON atlas_profiles;
DROP POLICY IF EXISTS "Service role atlas_diagnostics" ON atlas_diagnostics;
DROP POLICY IF EXISTS "Service role atlas_sessions" ON atlas_sessions;
DROP POLICY IF EXISTS "Service role atlas_lessons" ON atlas_lessons;
DROP POLICY IF EXISTS "Service role atlas_lesson_log" ON atlas_lesson_log;
DROP POLICY IF EXISTS "Service role atlas_practice_sessions" ON atlas_practice_sessions;
DROP POLICY IF EXISTS "Service role atlas_practice_log" ON atlas_practice_log;
DROP POLICY IF EXISTS "Service role atlas_instance_config" ON atlas_instance_config;
DROP POLICY IF EXISTS "Service role atlas_parent_config" ON atlas_parent_config;
DROP POLICY IF EXISTS "Service role atlas_diagnostics_pending" ON atlas_diagnostics_pending;
DROP POLICY IF EXISTS "Service role atlas_reassessment_meta" ON atlas_reassessment_meta;
DROP POLICY IF EXISTS "Service role atlas_admin_data" ON atlas_admin_data;
DROP POLICY IF EXISTS "Service role atlas_focus_overrides" ON atlas_focus_overrides;

-- ══════════════════════════════════════════════════
-- 2. Drop foreign key constraints
-- ══════════════════════════════════════════════════

ALTER TABLE atlas_students DROP CONSTRAINT IF EXISTS atlas_students_profile_id_fkey;
ALTER TABLE atlas_students DROP CONSTRAINT IF EXISTS atlas_students_family_id_fkey;
ALTER TABLE atlas_profiles DROP CONSTRAINT IF EXISTS atlas_profiles_profile_id_fkey;
ALTER TABLE atlas_profiles DROP CONSTRAINT IF EXISTS atlas_profiles_family_id_fkey;
ALTER TABLE atlas_diagnostics DROP CONSTRAINT IF EXISTS atlas_diagnostics_profile_id_fkey;
ALTER TABLE atlas_sessions DROP CONSTRAINT IF EXISTS atlas_sessions_profile_id_fkey;
ALTER TABLE atlas_lessons DROP CONSTRAINT IF EXISTS atlas_lessons_profile_id_fkey;
ALTER TABLE atlas_lesson_log DROP CONSTRAINT IF EXISTS atlas_lesson_log_profile_id_fkey;
ALTER TABLE atlas_practice_sessions DROP CONSTRAINT IF EXISTS atlas_practice_sessions_profile_id_fkey;
ALTER TABLE atlas_practice_log DROP CONSTRAINT IF EXISTS atlas_practice_log_profile_id_fkey;
ALTER TABLE atlas_instance_config DROP CONSTRAINT IF EXISTS atlas_instance_config_family_id_fkey;
ALTER TABLE atlas_parent_config DROP CONSTRAINT IF EXISTS atlas_parent_config_family_id_fkey;
ALTER TABLE atlas_diagnostics_pending DROP CONSTRAINT IF EXISTS atlas_diagnostics_pending_family_id_fkey;
ALTER TABLE atlas_reassessment_meta DROP CONSTRAINT IF EXISTS atlas_reassessment_meta_profile_id_fkey;
ALTER TABLE atlas_focus_overrides DROP CONSTRAINT IF EXISTS atlas_focus_overrides_profile_id_fkey;
ALTER TABLE atlas_focus_overrides DROP CONSTRAINT IF EXISTS atlas_focus_overrides_family_id_fkey;
ALTER TABLE atlas_focus_overrides DROP CONSTRAINT IF EXISTS atlas_focus_overrides_set_by_fkey;

-- ══════════════════════════════════════════════════
-- 3. Convert profile_id columns from UUID to TEXT
-- ══════════════════════════════════════════════════

ALTER TABLE atlas_students ALTER COLUMN profile_id TYPE TEXT USING profile_id::TEXT;
ALTER TABLE atlas_profiles ALTER COLUMN profile_id TYPE TEXT USING profile_id::TEXT;
ALTER TABLE atlas_diagnostics ALTER COLUMN profile_id TYPE TEXT USING profile_id::TEXT;
ALTER TABLE atlas_sessions ALTER COLUMN profile_id TYPE TEXT USING profile_id::TEXT;
ALTER TABLE atlas_lessons ALTER COLUMN profile_id TYPE TEXT USING profile_id::TEXT;
ALTER TABLE atlas_lesson_log ALTER COLUMN profile_id TYPE TEXT USING profile_id::TEXT;
ALTER TABLE atlas_practice_sessions ALTER COLUMN profile_id TYPE TEXT USING profile_id::TEXT;
ALTER TABLE atlas_practice_log ALTER COLUMN profile_id TYPE TEXT USING profile_id::TEXT;
ALTER TABLE atlas_reassessment_meta ALTER COLUMN profile_id TYPE TEXT USING profile_id::TEXT;
ALTER TABLE atlas_focus_overrides ALTER COLUMN profile_id TYPE TEXT USING profile_id::TEXT;
ALTER TABLE atlas_focus_overrides ALTER COLUMN set_by TYPE TEXT USING set_by::TEXT;

-- ══════════════════════════════════════════════════
-- 4. Convert family_id columns from UUID to TEXT
-- ══════════════════════════════════════════════════

ALTER TABLE atlas_students ALTER COLUMN family_id TYPE TEXT USING family_id::TEXT;
ALTER TABLE atlas_profiles ALTER COLUMN family_id TYPE TEXT USING family_id::TEXT;
ALTER TABLE atlas_instance_config ALTER COLUMN family_id TYPE TEXT USING family_id::TEXT;
ALTER TABLE atlas_parent_config ALTER COLUMN family_id TYPE TEXT USING family_id::TEXT;
ALTER TABLE atlas_diagnostics_pending ALTER COLUMN family_id TYPE TEXT USING family_id::TEXT;
ALTER TABLE atlas_focus_overrides ALTER COLUMN family_id TYPE TEXT USING family_id::TEXT;

-- ══════════════════════════════════════════════════
-- 5. Recreate service role policies (full access)
-- ══════════════════════════════════════════════════

CREATE POLICY "Service role atlas_students" ON atlas_students FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas_profiles" ON atlas_profiles FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas_diagnostics" ON atlas_diagnostics FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas_sessions" ON atlas_sessions FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas_lessons" ON atlas_lessons FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas_lesson_log" ON atlas_lesson_log FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas_practice_sessions" ON atlas_practice_sessions FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas_practice_log" ON atlas_practice_log FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas_instance_config" ON atlas_instance_config FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas_parent_config" ON atlas_parent_config FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas_diagnostics_pending" ON atlas_diagnostics_pending FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas_reassessment_meta" ON atlas_reassessment_meta FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas_admin_data" ON atlas_admin_data FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas_focus_overrides" ON atlas_focus_overrides FOR ALL USING (auth.role() = 'service_role');

-- Note: The parent/student read policies that used auth.uid() with UUID
-- comparison are removed. Access control is now handled by the Express
-- proxy layer (atlas-proxy.js) which enforces family membership before
-- forwarding requests to Atlas. These can be re-added later if needed
-- with TEXT comparison when KmUnity profile IDs are mapped to Atlas IDs.

COMMIT;
