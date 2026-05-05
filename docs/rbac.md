# Role-Based Access Control Guide

This guide describes how role-based access control (RBAC) is implemented in OpenCare-Core and how to work with the role metadata introduced for [issue #6](https://github.com/bos-com/OpenCare-Core/issues/6).

## Personas & Capabilities

| Role | Description | Example capabilities |
|------|-------------|----------------------|
| `admin` | Platform administrators with broad configuration rights. | Workforce management, system exports, metrics, any provider action. |
| `provider` | Clinicians and allied health staff interacting with patient data. | Patient CRUD, visit coordination, facility lookup. |
| `patient` | Individuals accessing their personal health data. | Future-facing patient portal access. Currently blocked from staff endpoints. |

`admin` users implicitly inherit all provider privileges. Patients are intentionally restricted until patient-facing endpoints are introduced.

## API Permission Matrix

| Endpoint | Allowed roles | Notes |
|----------|---------------|-------|
| `/api/v1/patients/` | `admin`, `provider` | Patient management reserved for staff. |
| `/api/v1/health-workers/` | `admin` | Workforce administration only. |
| `/api/v1/facilities/` | `admin`, `provider` | Operational facility data. |
| `/api/v1/visits/` | `admin`, `provider` | Visit scheduling and tracking. |
| `/api/v1/records/` | `admin`, `provider` | Clinical records. Patient self-access is future work. |
| `/api/v1/audit-logs/` | `admin` | Audit trail access. |
| `/api/v1/stats/` | `admin` | Operational metrics. |
| `/api/v1/export/` | `admin` | Bulk data export. |
| `/api/v1/health/` | Public | Health check kept open for infra probes. |

Additional viewsets should set a `required_roles` frozenset and include `RoleRequired` in `permission_classes` to join the RBAC system.

## Assigning Roles

Users now expose a `role` field on the Django admin and `User` model:

- Admin UI: update the **Role** dropdown when editing a user.
- Shell example:

```python
from django.contrib.auth import get_user_model
User = get_user_model()

User.objects.filter(username="alice").update(role=User.Role.ADMIN)
```

Newly created users default to `provider`. A data migration upgrades existing superusers to `admin` automatically.

## Enforcement Helpers

- `apps.api.permissions.RoleRequired` checks the authenticated user's `role` against the target view's `required_roles` attribute (admins always pass).
- `apps.api.permissions.require_roles(*roles)` decorator attaches metadata for function-based views (e.g., `@require_roles(User.Role.ADMIN)` on `/api/v1/stats/`).
- For DRF viewsets, set `permission_classes = [IsAuthenticated, RoleRequired]` and define `required_roles`.

## Testing

Automated coverage lives in `apps/api/tests/test_rbac.py`:
- Confirms patients receive 403s on staff endpoints.
- Blocks providers from admin-only metrics.
- Allows admins to reach restricted APIs.
- Exercises the permission utility directly for provider access.

Run the RBAC suite with:

```bash
DJANGO_SETTINGS_MODULE=config.settings.development python3 manage.py test apps.api.tests.test_rbac
```

## Extending RBAC

When introducing new endpoints:
1. Decide which personas should access the route.
2. Add `required_roles` and include `RoleRequired`.
3. Update this matrix if the endpoint is public or custom.
4. Add tests covering both successful and forbidden flows.

For finer-grained object-level rules (e.g., patient-specific record access), extend the permissions module with object checks once domain models solidify.

