# Private-original and public-copy register

Private screenshot originals remain outside Git because some frames contain account, organization, local-path, clipped prior-terminal, or session identifiers. Public copies either preserve the original bytes or cover only declared rectangles with opaque black pixels.

The original SHA-256 values provide a later comparison anchor; they are not public proof by themselves. The public images, rectangles, public hashes, dimensions, and pixel-difference checks are listed in the [redaction audit](redaction-audit.txt).

| Private artifact | Original SHA-256 | Public handling |
| --- | --- | --- |
| shared-batch/environment-and-auth.raw.png | `5ae88c8067881a0861a2e17a6597f1345c6d0f6d6ee1d23965ae4558d34b7dd9` | Reuses the preceding Fable sample's audited [environment.redacted.png](environment.redacted.png) |
| r1/status.raw.png | `7a6b8aea6852047abfdbd9e6406c8f4ebc04eab3947ef05b3d4651f0b28efd0c` | Published as [status.redacted.png](status.redacted.png) with deterministic opaque redactions |
| r1/response.raw.png | `45e06bc9ec063096b792f0ab827722268f118047079a66ff13922e04984b2504` | Published byte-for-byte as [R1 response](../attempts/r1/response.png) |
| r2/response.raw.png | `9d4912c0346395792fe7113327915a1939d2823510df977214583e47ebbaa4d7` | Published as [R2 response](../attempts/r2/response.png) with deterministic opaque redactions |
| r3/response.raw.png | `43f4466beefa311fc9224d7386c10192229278480387c13b367abfbe04b0a3d4` | Published as [R3 response](../attempts/r3/response.png) with deterministic opaque redactions |

The original transcript files remain private to the contributor account and were not read or hashed by the maintainer. Public event files reproduce the contributor's post-exit, deduplicated `jq` results and omit private message IDs and local-environment identifiers.
