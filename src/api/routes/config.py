"""
Configuration endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from src import config as config_module

router = APIRouter()


class RuleUpdate(BaseModel):
    name: str
    extensions: List[str]
    destination: str


class ConfigUpdate(BaseModel):
    target_directories: List[str]
    ignore_patterns: List[str]
    rename_format: str
    rules: List[RuleUpdate]


@router.get("/")
async def get_config():
    """Get current configuration"""
    try:
        cfg = config_module.load_config()
        return {
            "target_directories": cfg.target_directories,
            "ignore_patterns": cfg.ignore_patterns,
            "rename_format": cfg.rename_format,
            "rules": [
                {
                    "name": rule.name,
                    "extensions": rule.extensions,
                    "destination": rule.destination
                }
                for rule in cfg.rules
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def update_config(config_data: ConfigUpdate):
    """Update configuration"""
    try:
        # TODO: Implement config update logic
        # For now, return success
        return {"success": True, "message": "Configuration updated (not yet implemented)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/validate")
async def validate_config():
    """Validate current configuration"""
    try:
        cfg = config_module.load_config()
        # If load_config succeeds, config is valid
        return {
            "valid": True,
            "message": "Configuration is valid",
            "rule_count": len(cfg.rules),
            "target_count": len(cfg.target_directories)
        }
    except Exception as e:
        return {
            "valid": False,
            "message": str(e)
        }
