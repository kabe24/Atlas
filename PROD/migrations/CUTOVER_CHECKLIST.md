# Atlas Production Cutover Checklist

## Pre-Migration

- [ ] Run `007_atlas_tables.sql` in Supabase SQL Editor (creates 14 tables + RLS)
- [ ] Verify tables exist: `SELECT tablename FROM pg_tables WHERE tablename LIKE 'atlas_%';`
- [ ] Confirm KmUnity families and profiles tables have data
- [ ] Add `ATLAS_BACKEND_URL=http://atlas.railway.internal:8000` to KmUnity Railway vars
- [ ] Add `supabase` to Atlas `requirements.txt` if not already present

## Migration

- [ ] SSH into Atlas container or run locally with prod env vars
- [ ] Dry run: `python migrations/migrate_json_to_supabase.py --dry-run`
- [ ] Review counts — should match file-based data
- [ ] Live run: `python migrations/migrate_json_to_supabase.py`
- [ ] Verify zero errors in summary

## Post-Migration Verification

- [ ] Check row counts in Supabase:
  ```sql
  SELECT 'atlas_students' AS t, count(*) FROM atlas_students
  UNION ALL SELECT 'atlas_profiles', count(*) FROM atlas_profiles
  UNION ALL SELECT 'atlas_diagnostics', count(*) FROM atlas_diagnostics
  UNION ALL SELECT 'atlas_sessions', count(*) FROM atlas_sessions
  UNION ALL SELECT 'atlas_lessons', count(*) FROM atlas_lessons
  UNION ALL SELECT 'atlas_lesson_log', count(*) FROM atlas_lesson_log
  UNION ALL SELECT 'atlas_practice_sessions', count(*) FROM atlas_practice_sessions
  UNION ALL SELECT 'atlas_practice_log', count(*) FROM atlas_practice_log
  UNION ALL SELECT 'atlas_instance_config', count(*) FROM atlas_instance_config
  UNION ALL SELECT 'atlas_parent_config', count(*) FROM atlas_parent_config;
  ```
- [ ] Spot-check a student: compare JSON file vs Supabase row
- [ ] Spot-check a diagnostic: compare JSON file vs Supabase row

## Production Switch

- [ ] Set `STORAGE_BACKEND=supabase` in Atlas Railway variables
- [ ] Redeploy Atlas on Railway
- [ ] Test: hit `/api/version` — should return app version
- [ ] Test: create a test student via API — verify it appears in Supabase
- [ ] Test: run a diagnostic — verify state persists in Supabase
- [ ] Test: parent dashboard loads student data from Supabase

## Rollback Plan

If issues arise after switching to Supabase:
1. Set `STORAGE_BACKEND=file` in Railway
2. Redeploy — Atlas reverts to file-based storage immediately
3. File data is still intact (migration is read-only, doesn't delete files)
