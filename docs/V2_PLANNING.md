# Fylum V2.0.0 Planning Document

## Vision

Transform Fylum from a CLI-only tool into a user-friendly desktop application with a graphical interface, making file organization accessible to non-technical users while maintaining all CLI functionality.

## Target Users

- **Primary**: Non-technical users who want file organization without CLI
- **Secondary**: Power users who want both GUI convenience and CLI automation
- **Tertiary**: Users who need scheduling and automation features

## Core V2.0.0 Features (from Roadmap)

### 1. Graphical User Interface (GUI)
Desktop application wrapping core CLI logic

**Options to Consider:**
- **tkinter** (built-in, lightweight, cross-platform)
- **PyQt6/PySide6** (professional, feature-rich, larger)
- **Electron + Python** (modern web UI, larger bundle)
- **Web-based (Flask/FastAPI + Local Server)** (accessible, modern)

### 2. Interactive Mode
Preview and approve file operations before execution

**Requirements:**
- Show list of pending file operations
- Allow user to approve/reject individual operations
- Bulk approve/reject options
- Visual preview of before/after state

### 3. Scheduling
Automatic cleaning at specified intervals

**Requirements:**
- Cron-like scheduling interface
- One-time, daily, weekly, monthly schedules
- Background service or task scheduler integration
- Notification when scheduled task runs

### 4. System Notifications
Native desktop notifications on task completion

**Requirements:**
- Cross-platform notification support
- Summary of operations performed
- Error notifications
- Clickable to open results/manifest

### 5. Simple Installer
Easy OS integration

**Requirements:**
- Windows: MSI/NSIS installer
- macOS: DMG with drag-to-Applications
- Linux: AppImage or .deb package
- Desktop shortcuts and file associations

---

## Proposed Architecture

### Option A: Hybrid CLI + Embedded Web UI
- Keep existing CLI fully functional
- Add Flask/FastAPI backend
- Modern web UI (React/Vue/Svelte) served locally
- Best of both worlds: web tech + desktop app

**Pros:**
- Modern, responsive UI
- Easy to develop and maintain
- Cross-platform consistency
- Can reuse for future web version

**Cons:**
- Larger bundle size
- More complex architecture
- Need to bundle web assets

### Option B: Native Desktop GUI (PyQt6)
- Professional native GUI
- Qt Designer for UI layout
- Full desktop integration

**Pros:**
- Native look and feel
- Excellent desktop features
- Mature ecosystem
- Good documentation

**Cons:**
- Steeper learning curve
- Larger dependencies
- License considerations (LGPL)

### Option C: Lightweight tkinter
- Python's built-in GUI library
- Simple and lightweight

**Pros:**
- No extra dependencies
- Small bundle size
- Easy to learn
- Cross-platform

**Cons:**
- Less modern appearance
- Limited UI components
- More manual styling needed

---

## Recommended Approach: **Option A - Hybrid CLI + Web UI**

### Technology Stack
- **Backend**: FastAPI (async, modern, fast)
- **Frontend**: Svelte (lightweight, reactive)
- **Desktop Wrapper**: PyWebView (native window without Electron bloat)
- **Scheduling**: APScheduler (Python-based job scheduling)
- **Notifications**: plyer (cross-platform notifications)

### Benefits
1. Keeps CLI fully functional (backward compatible)
2. Modern, responsive web UI
3. Smaller than Electron (uses OS webview)
4. Easy to add web-hosted version later
5. Familiar web dev tools and patterns

---

## V2.0.0 Development Phases

### Phase 1: Backend API (2-3 weeks)
**Goal**: Create REST API wrapping existing CLI functionality

**Tasks:**
- [ ] Set up FastAPI project structure
- [ ] Create API endpoints for:
  - GET `/config` - Load configuration
  - POST `/config` - Update configuration
  - POST `/scan` - Scan directories (dry run)
  - POST `/clean` - Execute file operations
  - POST `/undo` - Revert last operation
  - GET `/history` - View operation history
  - GET `/rules` - List available rules
- [ ] WebSocket support for real-time updates
- [ ] API authentication (optional for local use)
- [ ] API documentation with Swagger/OpenAPI

### Phase 2: Frontend UI (3-4 weeks)
**Goal**: Build interactive web interface

**Tasks:**
- [ ] Set up Svelte project
- [ ] Design UI mockups/wireframes
- [ ] Implement main views:
  - Dashboard (overview, quick actions)
  - Configuration editor (visual YAML editor)
  - Preview mode (interactive file list)
  - History/Manifest viewer
  - Scheduling interface
  - Settings panel
- [ ] Real-time progress indicators
- [ ] Drag-and-drop support for folders
- [ ] Dark/light theme

### Phase 3: Desktop Integration (1-2 weeks)
**Goal**: Package as native desktop app

**Tasks:**
- [ ] Integrate PyWebView for native window
- [ ] System tray integration
- [ ] Auto-start on login (optional)
- [ ] File system watchers for live monitoring
- [ ] Native file/folder pickers
- [ ] Menu bar integration

### Phase 4: Scheduling & Automation (1-2 weeks)
**Goal**: Add scheduling capabilities

**Tasks:**
- [ ] Integrate APScheduler
- [ ] UI for schedule creation/editing
- [ ] Background service/daemon mode
- [ ] Schedule persistence (SQLite or JSON)
- [ ] Manual trigger vs. scheduled runs

### Phase 5: Notifications (1 week)
**Goal**: Desktop notification system

**Tasks:**
- [ ] Integrate plyer for notifications
- [ ] Notification templates
- [ ] User preferences for notifications
- [ ] Actionable notifications (open results, undo)

### Phase 6: Installer & Distribution (1-2 weeks)
**Goal**: Easy installation across platforms

**Tasks:**
- [ ] Windows: NSIS or Inno Setup installer
- [ ] macOS: DMG with background image
- [ ] Linux: AppImage or Flatpak
- [ ] Auto-update mechanism (optional)
- [ ] Code signing (Windows/macOS)

### Phase 7: Testing & Polish (2 weeks)
**Goal**: Comprehensive testing and refinement

**Tasks:**
- [ ] E2E testing with Playwright/Selenium
- [ ] Cross-platform testing
- [ ] UAT with real users
- [ ] Performance optimization
- [ ] Accessibility improvements
- [ ] Documentation updates

---

## Technical Requirements

### Dependencies (New for V2.0.0)
```txt
# Backend
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
apscheduler>=3.10.0
plyer>=2.1.0
pywebview>=4.4.0

# Frontend (bundled)
# Svelte build artifacts will be bundled
```

### File Structure
```
fylum/
├── app.py                  # CLI entry point (existing)
├── gui.py                  # GUI entry point (new)
├── src/
│   ├── api/               # FastAPI backend (new)
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes/
│   │   └── models/
│   ├── scheduler/         # Scheduling logic (new)
│   ├── config.py          # Existing
│   ├── engine.py          # Existing
│   ├── processor.py       # Existing
│   └── undo.py            # Existing
├── web/                   # Frontend (new)
│   ├── src/
│   ├── public/
│   └── package.json
└── installers/            # Packaging scripts (new)
```

---

## Success Criteria

V2.0.0 will be considered successful when:

1. ✅ GUI provides all CLI functionality
2. ✅ Users can preview and approve operations interactively
3. ✅ Scheduling works reliably across platforms
4. ✅ Notifications appear on all platforms
5. ✅ Installers work on Windows, macOS, Linux
6. ✅ All V1.0.0 features remain functional via CLI
7. ✅ Performance is acceptable (UI responsive, operations fast)
8. ✅ Documentation complete for GUI features

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| GUI framework learning curve | Medium | Start with simple prototype, iterate |
| Cross-platform compatibility | High | Test early and often on all platforms |
| Bundle size too large | Medium | Use PyWebView instead of Electron |
| Scheduling reliability | Medium | Use proven library (APScheduler) |
| Backward compatibility | High | Keep CLI separate, maintain API contract |

---

## Questions to Resolve

1. **GUI Framework**: Confirm Option A (PyWebView + Svelte) vs. other options
2. **Authentication**: Do we need API auth for local-only use?
3. **Multi-user**: Should GUI support multiple user profiles?
4. **Cloud Sync**: Future feature or out of scope for V2?
5. **Mobile**: Companion mobile app for V3.0.0?

---

## Next Steps

1. **Create ADR** for GUI framework decision
2. **Prototype** minimal FastAPI + Svelte + PyWebView setup
3. **Design mockups** for main UI screens
4. **Set up project board** for V2.0.0 tasks
5. **Create development branch** `develop/v2.0.0`

---

**Last Updated:** October 10, 2025
**Status:** Planning Phase
**Target Release:** Q2 2026
