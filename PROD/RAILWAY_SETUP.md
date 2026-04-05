# Atlas Railway Setup Guide

## Overview

Atlas runs as a second Railway service in the KmUnity project. KmUnity's Express server proxies `/api/atlas/*` requests to this service via Railway internal networking.

## Step 1: Create the Railway Service

1. Open your KmUnity project in the Railway dashboard
2. Click **"+ New"** → **"Service"** → **"GitHub Repo"**
3. Select the Atlas repo (or the Atlas subdirectory if monorepo)
4. Name it `atlas-backend`
5. Railway will detect the Dockerfile and build automatically

## Step 2: Configure Environment Variables

Set these env vars on the `atlas-backend` service in Railway:

| Variable | Value | Notes |
|----------|-------|-------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Same key as KmUnity Express |
| `STORAGE_BACKEND` | `supabase` | Switches from file-based to Supabase storage |
| `SUPABASE_URL` | `https://your-project.supabase.co` | Same as KmUnity's `VITE_SUPABASE_URL` |
| `SUPABASE_SERVICE_ROLE_KEY` | Your service role key | Same as KmUnity's `SUPABASE_SERVICE_ROLE_KEY` |
| `PORT` | `8000` | Railway sets this automatically, but explicit is fine |

## Step 3: Internal Networking

1. In Railway, go to `atlas-backend` → **Settings** → **Networking**
2. Enable **Private Networking** (internal)
3. Note the internal URL — it will be something like `atlas-backend.railway.internal:8000`
4. **Do NOT** enable a public domain (Atlas is accessed through the KmUnity proxy)

## Step 4: Configure KmUnity Express

On the `kmunity-app` service, add this env var:

| Variable | Value |
|----------|-------|
| `ATLAS_BACKEND_URL` | `http://atlas-backend.railway.internal:8000` |

This tells the Express proxy where to forward Atlas API calls.

## Step 5: Install Proxy Dependency

In the KmUnity app, install the HTTP proxy middleware:

```bash
cd kmunity-app
npm install http-proxy-middleware
```

## Step 6: Run Supabase Migration

Run `supabase/migrations/007_atlas_tables.sql` in the Supabase SQL Editor. This creates all Atlas data tables and activates the Atlas tool.

## Step 7: Verify

1. Deploy both services
2. Visit `https://app.kmunity.tech/api/atlas/health` — should return Atlas health status
3. Check the KmUnity dashboard — Atlas tool card should appear
4. Railway logs for `atlas-backend` should show `SupabaseStorage initialized`

## Local Development

For local dev, run Atlas standalone on port 8000 as usual:

```bash
# Terminal 1: Atlas Python backend (file-based storage)
cd ~/Desktop/AI\ Tutor\ Platform
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: KmUnity (proxies to Atlas on localhost:8000)
cd ~/Desktop/KmUnity/kmunity-app
ATLAS_BACKEND_URL=http://localhost:8000 npm run dev
```

The `STORAGE_BACKEND` defaults to `file` when not set, so local dev uses the existing JSON files.
