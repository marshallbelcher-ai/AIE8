# Troubleshooting git pull issues
_Exported on 9/18/2025 at 17:36:19 PDT from Cursor (1.5.11)_

---

**User**

why am I not pulling updates from git@github.com:AI-Maker-Space/AIE8.git?

---

**Cursor**

I can see from your terminal output that you have divergent branches - your local branch has commits that differ from the upstream main branch. Let me help you understand what's happening and resolve this.

Now I understand the issue! Here's what's happening:

## The Problem

You have **divergent branches**. Your local repository has commits that are different from the upstream repository:

1. **Your local branch**: `s01-assignment` is currently checked out and has commit `65f91ed`
2. **Upstream main**: Has newer commits (up to `44fc8ee`) that your local repository doesn't have
3. **Your local main**: Is at commit `807a353`, which is behind the upstream main

## Why the Pull Failed

When you ran `git pull upstream main`, Git detected that:
- Your current branch (`s01-assignment`) has commits that upstream doesn't have
- Upstream has commits that you don't have
- Git doesn't know how to automatically reconcile these differences

## Solutions

You have a few options depending on what you want to achieve:

### Option 1: Update your local main branch (Recommended)
If you want to get the latest updates on your main branch:

