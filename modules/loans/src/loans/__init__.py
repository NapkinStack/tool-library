"""Who holds which tool, between which dates, and what came back.

This module reads the catalogue through contracts/catalog-api/v1/openapi.yaml and through
a double built from that schema. It never imports catalog, and it never reads catalog's
data (ADR-0001; fitness rules B1, B2 and B5).
"""

__all__: list[str] = []
