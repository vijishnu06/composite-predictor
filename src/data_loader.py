import io
import uuid
from pathlib import Path
import pandas as pd
from .physics_model import ROOT


def read_csv(source):
    try:
        return pd.read_csv(source)
    except pd.errors.EmptyDataError as exc:
        raise ValueError("Empty CSV file.") from exc
    except (pd.errors.ParserError, UnicodeDecodeError) as exc:
        raise ValueError("Cannot parse CSV; use a UTF-8 comma-separated file.") from exc


def save_upload(payload: bytes):
    """Validate parseability, then create a unique file without overwriting."""
    read_csv(io.BytesIO(payload))
    path = ROOT / "data/uploads" / f"upload_{uuid.uuid4().hex}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(payload)
    return path
