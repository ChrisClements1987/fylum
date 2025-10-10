# Fylum Web Frontend

Svelte-based frontend for Fylum V2.0.0 GUI.

## Development

### Prerequisites
- Node.js 16+ and npm

### Setup
```bash
npm install
```

### Development Server
```bash
npm run dev
```

Then access at: http://localhost:5173

Make sure the FastAPI backend is running on port 8000:
```bash
# In the project root
python -m src.api.main
```

### Build for Production
```bash
npm run build
```

Built files will be in `dist/` directory.

## Project Structure

```
web/
├── src/
│   ├── App.svelte          # Main application component
│   ├── main.js             # Entry point
│   └── app.css             # Global styles
├── public/                 # Static assets
├── package.json            # Dependencies
└── vite.config.js          # Build configuration
```

## Features

- **Dashboard**: Quick actions for common operations
- **Configuration**: View and edit Fylum configuration
- **Preview**: Preview file operations before executing
- **History**: View past operations

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000/api`.

Endpoints used:
- `GET /api/config/` - Load configuration
- `POST /api/operations/scan` - Scan for files (dry run)
- `POST /api/operations/clean` - Execute file organization
- `POST /api/operations/undo` - Undo last operation
- `GET /api/history/` - Get operation history
