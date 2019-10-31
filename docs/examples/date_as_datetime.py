from cbor2 import dumps
from datetime import date, timezone

# Serialize dates as datetimes
encoded = dumps(date(2019, 10, 28),
                timezone=timezone.utc, date_as_datetime=True)
