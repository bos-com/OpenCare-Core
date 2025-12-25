# RBAC Implementation Plan for Issue #6

## 1. Objective
Establish role-based access control (RBAC) across the OpenCare-Core APIs so that patient, provider, and administrator personas have clearly defined capabilities aligned with least-privilege principles. This work addresses issue #6 by introducing role metadata on users, central permission enforcement, automated verification, and developer-facing documentation.

## 2. Current State Assessment
- Authentication: Django + DRF using JWT (SimpleJWT) and session auth; default permission class is `IsAuthenticated`.
- Authorization: API viewsets currently rely solely on authentication with no role checks. Function-based JSON views perform no RBAC validation.
- User model: Custom `apps.core.models.User` extends `AbstractUser` with a `user_type` field describing clinician disciplines but not top-level personas (patient/provider/admin).
- Documentation/tests: No RBAC design doc or automated tests validating authorization pathways.

These gaps mean any authenticated user can call every API which conflicts with compliance requirements.

## 3. Role Model & Terminology
| Role Key | Description | Typical Actors |
|----------|-------------|----------------|
| `admin`  | Platform administrators responsible for configuration, workforce, and auditing. Equivalent to system staff or superusers. |
| `provider` | Licensed healthcare staff (doctors, nurses, allied health) interacting with patient data for clinical workflows. Maps to existing `user_type` specialisations. |
| `patient` | Individuals accessing their own health information through the API. |

Implementation details:
- Introduce a new `role` field on `User` backed by a `TextChoices` enumeration with values `ADMIN`, `PROVIDER`, `PATIENT`.
- Default newly created users to `provider` to preserve current behaviour while tests cover explicit assignments.
- Provide convenience helpers (`is_admin_role`, `is_provider_role`, `is_patient_role`) for readability.
- Data migration will backfill `admin` role for `is_superuser=True` accounts; all others default to `provider` until explicitly changed by administrators.

## 4. API Permission Matrix (Phase 1)
| Endpoint | Allowed Roles | Notes |
|----------|---------------|-------|
| `/api/v1/patients/` (ViewSet) | `admin`, `provider` | Patient records CRUD reserved for clinical staff and admins. |
| `/api/v1/health-workers/` (ViewSet) | `admin` | Only admins manage workforce rosters. |
| `/api/v1/facilities/` (ViewSet) | `admin`, `provider` | Operational data relevant to providers and admins. |
| `/api/v1/visits/` (ViewSet) | `admin`, `provider` | Visit management restricted to staff roles. |
| `/api/v1/records/` (ViewSet) | `admin`, `provider` | Clinical records currently staff-only. (Future work may grant patients scoped access to their own data.) |
| `/api/v1/stats/` | `admin` | System metrics contain sensitive operational insights. |
| `/api/v1/export/` | `admin` | Bulk data exports restricted to admins. |
| `/api/v1/health/` | Public | Health ping remains unauthenticated to support infrastructure probes. |

The plan intentionally defers granular, object-level rules (e.g., providers limited to facilities) to future iterations once domain logic stabilises.

## 5. Enforcement Strategy
1. **Central permission utility**: Add `RoleRequired` DRF permission class that:
   - Reads `view.required_roles` (set per viewset/function) and checks the requesting user.
   - Grants admins universal access (fallback for emergency support).
2. **Function-based view decorator**: Expose `@require_roles(...)` helper built on the same logic for non-DRF endpoints, ensuring a single enforcement path.
3. **Settings integration**: Keep `IsAuthenticated` as the global default and append role checks per endpoint to avoid backwards-incompatible changes elsewhere.
4. **Error responses**: Return standardised 403 JSON using existing exception handler patterns (DRF automatically handles this for viewsets; decorator will return `JsonResponse` with error payload for FBVs).

## 6. Implementation Tasks
1. **Model & migrations**
   - Update `apps.core.models.User` with the `Role` enumeration, field, and helper properties.
   - Create schema migration for the new field and data migration to backfill roles.
   - Update admin registration (if necessary) to expose the new field.
2. **Permission utilities**
   - Add `apps.api.permissions` module housing `RoleRequired` and decorator `require_roles`.
   - Implement shared checker to keep logic consistent.
3. **API wiring**
   - Update each DRF viewset to include `RoleRequired` and declare `required_roles` constants.
   - Wrap `/api/v1/stats/` and `/api/v1/export/` with the decorator for runtime enforcement.
   - Maintain open access to the health check endpoint.
4. **Automated tests**
   - Create `apps/api/tests/test_rbac.py` verifying:
     - Providers and admins access permitted endpoints.
     - Patients receive 403 responses where blocked.
     - Admins override restrictions.
     - Stats/export endpoints respect role checks.
   - Ensure fixtures cover the three role archetypes.
5. **Documentation updates**
   - Produce developer-focused RBAC guide summarising roles, API matrix, and how to assign roles.
   - Reference the guide from `README.md` quick-start or docs index.
6. **Developer ergonomics**
   - Provide Django shell snippet in docs for assigning roles.
   - Confirm linters/tests pass (`python manage.py test apps.api.tests.test_rbac`).

## 7. Testing & Validation Plan
- Run targeted unit tests for the new suite plus existing API tests to guard regressions.
- Exercise token authentication in tests to ensure JWT + RBAC interplay.
- Validate unauthenticated requests continue returning 401.
- Manually verify decorator handles JSON responses for FBVs (covered by tests).

## 8. Risks & Mitigations
- **Migration defaulting all users to provider**: Mitigated by data migration elevating superusers to admin.
- **Patient-facing endpoints not yet scoped**: Documented as future enhancement; ensures current surface stays secure.
- **Auth integrations outside API app**: Plan confines changes to API layer; highlight follow-up work for other Django apps if needed.

## 9. Deliverables Checklist
- [x] Migrations introducing `User.role` with data backfill.
- [x] Permission utilities shared between DRF and function views.
- [x] Updated viewsets/endpoints with `required_roles` metadata.
- [x] New RBAC tests.
- [x] Documentation: implementation guide + README pointer.
- [ ] Pull request referencing issue #6 with summary of behavioural changes and testing evidence.
