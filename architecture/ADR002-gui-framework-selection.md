# ADR 002: GUI Framework Selection for V2.0.0

**Status:** Accepted  
**Date:** 2025-10-10  
**Deciders:** Development Team  
**Context:** Selecting the GUI framework for Fylum V2.0.0

---

## Context and Problem Statement

Fylum V2.0.0 requires a graphical user interface to make file organization accessible to non-technical users. We need to choose a GUI framework that:

- Provides a modern, responsive user interface
- Works across platforms (Windows, macOS, Linux)
- Maintains the existing CLI functionality
- Allows for future web-based deployment
- Has reasonable bundle size and performance
- Is maintainable by the current development team

## Decision Drivers

- **User Experience**: Modern, intuitive interface
- **Cross-platform**: Windows, macOS, Linux support
- **Development Speed**: Rapid prototyping and iteration
- **Bundle Size**: Reasonable executable size
- **Maintainability**: Clear architecture, good documentation
- **Future-proof**: Ability to adapt for web hosting later
- **Performance**: Responsive UI, efficient operations

## Considered Options

### Option 1: PyQt6/PySide6 (Native Desktop)
Native Qt-based GUI framework for Python.

**Pros:**
- Professional, native look and feel
- Excellent desktop integration
- Mature ecosystem with Qt Designer
- Rich widget set
- Good performance

**Cons:**
- Larger bundle size (~50-80 MB)
- Steeper learning curve
- LGPL licensing considerations
- Desktop-only (no web path)
- More complex to style/theme

### Option 2: tkinter (Lightweight Native)
Python's built-in GUI library.

**Pros:**
- No extra dependencies
- Very small bundle size
- Cross-platform
- Simple to learn

**Cons:**
- Limited widgets
- Outdated appearance
- Manual styling required
- Not suitable for modern web-like UIs
- Limited community momentum

### Option 3: Electron + Python (Web Technologies)
Full Electron framework with Python backend.

**Pros:**
- Modern web UI (React/Vue/Svelte)
- Extensive ecosystem
- Great developer tools
- Familiar web development

**Cons:**
- Very large bundle size (100-200 MB)
- High memory usage
- Includes full Chromium
- Overkill for desktop-only app
- Complex architecture

### Option 4: **PyWebView + FastAPI + Svelte (Hybrid - SELECTED)**
Lightweight native window using OS webview with web UI.

**Pros:**
- Modern web UI capabilities
- Uses OS native webview (no Chromium)
- Reasonable bundle size (20-30 MB)
- Familiar web development tools
- Easy to add web hosting later
- Good performance
- Clear separation: backend API + frontend UI

**Cons:**
- Less mature than Qt/Electron
- Webview differences between OSs
- Need to bundle web assets
- Two-part architecture

---

## Decision Outcome

**Chosen Option:** **Option 4 - PyWebView + FastAPI + Svelte**

### Rationale

1. **Best of Both Worlds**: Combines native desktop integration with modern web UI
2. **Smaller Bundle**: Uses OS webview instead of bundling Chromium (vs Electron)
3. **Future-proof**: Backend API can be exposed for web hosting in future
4. **Development Experience**: Svelte provides excellent DX with minimal boilerplate
5. **Performance**: FastAPI is high-performance async framework
6. **Maintainability**: Clear separation between backend and frontend

### Architecture

```
┌─────────────────────────────────────┐
│  Desktop Window (PyWebView)         │
│  ┌───────────────────────────────┐  │
│  │   Svelte Frontend (Web UI)    │  │
│  │   - Components                │  │
│  │   - State management          │  │
│  │   - UI logic                  │  │
│  └───────────┬───────────────────┘  │
│              │ HTTP/WebSocket       │
│  ┌───────────▼───────────────────┐  │
│  │   FastAPI Backend (REST API)  │  │
│  │   - Routes                    │  │
│  │   - Business logic wrapper    │  │
│  │   - Real-time updates         │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│  ┌───────────▼───────────────────┐  │
│  │   Core Logic (V1.0.0)         │  │
│  │   - config.py                 │  │
│  │   - engine.py                 │  │
│  │   - processor.py              │  │
│  │   - undo.py                   │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## Technology Stack

### Backend
- **FastAPI** 0.104+: Modern async web framework
- **Uvicorn**: ASGI server
- **APScheduler**: Job scheduling
- **plyer**: Cross-platform notifications

### Frontend
- **Svelte** 4.x: Reactive UI framework
- **SvelteKit** (optional): Full-stack framework
- **Vite**: Build tool
- **TailwindCSS**: Utility-first CSS

### Desktop Wrapper
- **PyWebView** 4.4+: Lightweight webview wrapper

### Build & Package
- **PyInstaller**: Executable packaging
- **Vite**: Frontend bundling

---

## Consequences

### Positive

- ✅ Modern, responsive UI with Svelte
- ✅ Smaller bundle than Electron
- ✅ Backend API reusable for future web version
- ✅ Clear architecture with separation of concerns
- ✅ Excellent developer experience
- ✅ Good performance characteristics

### Negative

- ⚠️ Need to maintain both Python and JavaScript codebases
- ⚠️ Webview rendering differences between OSs (testing required)
- ⚠️ Two build processes (Python + Vite)
- ⚠️ Less mature than Qt/Electron ecosystems

### Neutral

- ℹ️ Requires web development knowledge
- ℹ️ API-first architecture (good practice)
- ℹ️ Two-step deployment process

---

## Implementation Plan

1. **Phase 1**: Set up FastAPI backend with basic endpoints
2. **Phase 2**: Create Svelte frontend with initial views
3. **Phase 3**: Integrate PyWebView for desktop window
4. **Phase 4**: Build and package executable
5. **Phase 5**: Test across platforms

---

## Validation

Success criteria:
- [ ] Bundle size < 40 MB
- [ ] UI renders correctly on Windows, macOS, Linux
- [ ] Performance: API responses < 100ms
- [ ] All V1.0.0 features accessible via GUI
- [ ] Executable builds successfully on all platforms

---

## References

- PyWebView: https://pywebview.flowrl.com/
- FastAPI: https://fastapi.tiangolo.com/
- Svelte: https://svelte.dev/
- Comparison of Python GUI frameworks: [Internal research doc]

---

## Notes

- CLI remains fully functional and unchanged
- GUI wraps existing core logic, no duplication
- Can run in "headless" mode (API only) for future use cases
- Consider adding `--gui` flag to CLI for launching GUI mode
