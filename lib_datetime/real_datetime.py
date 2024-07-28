
from datetime import datetime
from datetime import timezone

def now() -> datetime:
    return datetime.now(timezone.utc)
