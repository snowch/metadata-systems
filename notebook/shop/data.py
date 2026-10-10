# Copyright © 2026 Christopher Snow

"""The shop's own data: what its checkout and its catalogue hold.

Invented for the course: the shop, its customers, its staff and its products are not real, and
every email address is at the reserved domains example.net and example.org. Money is whole pence
throughout, so every sum is exact; a value is shown in pounds only where a person reads it.

The shop opened its online store on Monday 7 September 2026. Its orders are written out by hand,
so every property the chapter relies on is deliberate: plain days whose raw orders add up to their
revenue; a cancelled order on Tuesday and on Saturday; an order on Wednesday that the export writes
twice; orders on Thursday that the checkout sent with no customer id; and no order with a quantity
of 0 or less. No number derived from these rows is written here: the engine computes them, and the
facts test pins the ones the chapter states.
"""

# The seven days of the week, Monday to Sunday, and the morning the learner starts work.
DAYS = (
    "2026-09-07",
    "2026-09-08",
    "2026-09-09",
    "2026-09-10",
    "2026-09-11",
    "2026-09-12",
    "2026-09-13",
)
ARRIVAL = "2026-09-14T09:00:00Z"

# The catalogue: id, name, category, list price in pence, and the member of staff who last edited
# the product (data about the product, not a record about the file).
PRODUCT_FIELDS = ("product_id", "name", "category", "list_price_pence", "updated_by")
PRODUCTS = (
    (1, "Inner tube, 700x25c", "tyres and tubes", 650, "k.adeyemi"),
    (2, "Brake pads, pair", "brakes", 1200, "k.adeyemi"),
    (3, "Chain, 11-speed", "drivetrain", 3200, "r.novak"),
    (4, "Folding tyre, 700x28c", "tyres and tubes", 3850, "k.adeyemi"),
    (5, "Saddle", "contact points", 4500, "s.lund"),
    (6, "Rear light", "lights", 1875, "r.novak"),
    (7, "Floor pump", "tools", 2999, "s.lund"),
    (8, "Bar tape", "contact points", 1425, "s.lund"),
)

CUSTOMER_FIELDS = ("customer_id", "name", "email", "country", "signed_up")
CUSTOMERS = (
    (101, "Amara Okafor", "amara.okafor@example.net", "GB", "2025-11-02"),
    (102, "Liam Byrne", "liam.byrne@example.org", "IE", "2026-01-15"),
    (103, "Sofia Marino", "SOFIA.MARINO@example.net", "IT", "2026-02-20"),
    (104, "Jonas Weber", "jonas.weber@example.org", "DE", "2025-08-30"),
    (105, "Chloe Martin", "chloe.martin@example.net", "FR", "2026-03-04"),
    (106, "Ravi Patel", "ravi.patel@example.org", "GB", "2026-04-11"),
    (107, "Emma de Vries", "emma.devries@example.net", "NL", "2025-12-01"),
    (108, "Tom Hughes", None, "GB", "2026-05-19"),
    (109, "Hana Novak", "hana.novak@example.org", "CZ", "2026-06-23"),
    (110, "Ben Carter", "ben.carter@example.net", "GB", "2026-06-07"),
)

ORDER_FIELDS = (
    "order_id",
    "customer_id",
    "product_id",
    "quantity",
    "price_pence",
    "status",
    "ordered_at",
)

# One order as the checkout recorded it: id, time (UTC), customer or None, product, quantity, and
# its status when it is not "completed".
_LINES = (
    # Monday 7: every order completed.
    (7001, "2026-09-07T08:14:00Z", 101, 1, 2),
    (7002, "2026-09-07T09:52:00Z", 104, 3, 1),
    (7003, "2026-09-07T12:30:00Z", 102, 6, 1),
    (7004, "2026-09-07T15:07:00Z", 107, 2, 2),
    (7005, "2026-09-07T18:45:00Z", 110, 8, 1),
    (7006, "2026-09-07T20:31:00Z", 103, 5, 1),
    # Tuesday 8: one order cancelled.
    (7007, "2026-09-08T07:58:00Z", 105, 4, 2),
    (7008, "2026-09-08T10:16:00Z", 106, 1, 3),
    (7009, "2026-09-08T11:42:00Z", 101, 7, 1, "cancelled"),
    (7010, "2026-09-08T13:25:00Z", 109, 2, 1),
    (7011, "2026-09-08T16:03:00Z", 102, 8, 2),
    (7012, "2026-09-08T19:18:00Z", 108, 6, 1),
    (7013, "2026-09-08T21:47:00Z", 104, 1, 1),
    # Wednesday 9: the export writes order 7015 twice (see DUPLICATED).
    (7014, "2026-09-09T08:33:00Z", 107, 3, 1),
    (7015, "2026-09-09T10:58:00Z", 110, 5, 1),
    (7016, "2026-09-09T13:12:00Z", 103, 1, 2),
    (7017, "2026-09-09T15:40:00Z", 105, 6, 2),
    (7018, "2026-09-09T17:29:00Z", 106, 8, 1),
    (7019, "2026-09-09T20:05:00Z", 101, 2, 1),
    # Thursday 10: the checkout sends three orders with no customer id.
    (7020, "2026-09-10T08:21:00Z", 102, 1, 1),
    (7021, "2026-09-10T09:47:00Z", None, 4, 2),
    (7022, "2026-09-10T11:36:00Z", 109, 6, 1),
    (7023, "2026-09-10T13:58:00Z", None, 5, 1),
    (7024, "2026-09-10T16:12:00Z", 104, 8, 1),
    (7025, "2026-09-10T18:40:00Z", None, 3, 1),
    (7026, "2026-09-10T21:05:00Z", 107, 2, 1),
    # Friday 11: every order completed.
    (7027, "2026-09-11T08:05:00Z", 105, 7, 1),
    (7028, "2026-09-11T09:30:00Z", 101, 1, 2),
    (7029, "2026-09-11T11:11:00Z", 110, 6, 1),
    (7030, "2026-09-11T12:48:00Z", 103, 8, 2),
    (7031, "2026-09-11T14:22:00Z", 106, 2, 2),
    (7032, "2026-09-11T16:55:00Z", 108, 4, 1),
    (7033, "2026-09-11T19:03:00Z", 102, 1, 1),
    (7034, "2026-09-11T21:39:00Z", 109, 5, 1),
    # Saturday 12: one order cancelled.
    (7035, "2026-09-12T09:12:00Z", 104, 3, 1),
    (7036, "2026-09-12T10:37:00Z", 107, 1, 2),
    (7037, "2026-09-12T12:04:00Z", 110, 2, 2, "cancelled"),
    (7038, "2026-09-12T13:50:00Z", 101, 6, 1),
    (7039, "2026-09-12T15:21:00Z", 105, 8, 1),
    (7040, "2026-09-12T17:08:00Z", 103, 4, 1),
    (7041, "2026-09-12T18:44:00Z", 106, 7, 1),
    (7042, "2026-09-12T20:26:00Z", 102, 5, 1),
    # Sunday 13: every order completed.
    (7043, "2026-09-13T10:02:00Z", 109, 1, 1),
    (7044, "2026-09-13T11:47:00Z", 108, 8, 2),
    (7045, "2026-09-13T14:15:00Z", 104, 6, 1),
    (7046, "2026-09-13T16:33:00Z", 107, 3, 1),
    (7047, "2026-09-13T19:58:00Z", 110, 2, 1),
)

# The order the export writes twice, from the first export that includes it.
DUPLICATED = 7015

_PRICE = {p[0]: p[3] for p in PRODUCTS}

# Every order the checkout recorded, as the export writes it, without the export's repeat.
ORDERS = tuple(
    (order_id, customer, product, quantity, _PRICE[product], (rest or ("completed",))[0], at)
    for order_id, at, customer, product, quantity, *rest in _LINES
)


def day_of(timestamp: str) -> str:
    """The UTC date of an ISO timestamp."""
    return timestamp[:10]
