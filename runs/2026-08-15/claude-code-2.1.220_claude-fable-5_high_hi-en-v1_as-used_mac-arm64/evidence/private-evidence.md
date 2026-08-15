# Private evidence register

The maintainer reviewed the raw screenshots listed below. They are withheld because the relevant frames also contain an account email, organization name or identifier, local path, username, or private session identifier. SHA-256 values provide a later comparison anchor; they are not a public proof by themselves.

The screenshots were supplied during the live pilot and were not copied into Git. Contributors should retain their private originals if they want later re-verification against these hashes.

| Private artifact | SHA-256 | Public handling |
| --- | --- | --- |
| batch/environment-and-auth.raw.png | `5ae88c8067881a0861a2e17a6597f1345c6d0f6d6ee1d23965ae4558d34b7dd9` | Sanitized transcription published as `preflight.txt` |
| r1/status.raw.png | `fed8c312f7c9f5354cf41f16ea136a1b7f34a0050880fd4c5be62a0361740b75` | Withheld: account and private session fields |
| batch/effort-high.raw.png | `70deae13d03fe8909b7b96cc13e5761304126bee6f3e00faecb9c44b87daff82` | High effort transcribed in `harness.txt` |
| r1/response.raw.png | `d182ab2454d93a14c71bf09ab5178cb7c8d152127533e7795b69b6108d8db7f7` | Exact response and rounded latency published in sanitized records |
| r2/response.raw.png | `2089edb20741545deb05fda4516cc7daeeae81f8cc54beed22c2deedf7b28007` | Withheld: banner contains account and organization fields |
| r3/response.raw.png | `a183cc203bf3b3e3dc95338adf76e6e5783556dbf3470429de1797c91a12d7b4` | Withheld: banner contains account and organization fields |

The original transcript files are also private because their filenames and metadata contain session and local-environment identifiers. Each public event file contains only the final assistant record after grouping private transcript records by message ID and retaining the latest timestamp.
