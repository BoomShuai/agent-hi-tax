# Private evidence register

Private originals remain outside Git. SHA-256 links each reviewed original to its public copy.

| Private original | Private SHA-256 | Public file | Public SHA-256 | Treatment |
| --- | --- | --- | --- | --- |
| environment.png | `a208a772a6191571cae2f32ad51fa358ebd0cecae499d7be8337ce5b85818ca0` | `environment.redacted.png` | `d745cca3130f98719b4c4963c4a9bdf19dff5afe3fee4c037d7565fd326b8ebb` | Opaque rectangles over home-path prefix, username, and hostname |
| r1-start.png | `1ea7ebc11030b58f14296eec90f36d948f654875d1f3b212342b1e71dbbb2428` | `attempts/r1/start.png` | `1ea7ebc11030b58f14296eec90f36d948f654875d1f3b212342b1e71dbbb2428` | Unchanged copy |
| r1-response.png | `bc2fa1cbb849efa183f4cdf3d7f50ca2d133a6e95c70d65e02b1f5e1127ac556` | `attempts/r1/response.png` | `bc2fa1cbb849efa183f4cdf3d7f50ca2d133a6e95c70d65e02b1f5e1127ac556` | Unchanged copy |
| r2-start.png | `dac2ef09a5ab38e83ed2af3908fec16b888d01fc33f2027cf38763b30fb7a477` | `attempts/r2/start.png` | `dac2ef09a5ab38e83ed2af3908fec16b888d01fc33f2027cf38763b30fb7a477` | Unchanged copy |
| r2-response.png | `f491ece28dae67d847ec9644d7e7a3b84f165871534615ca734a4e397e23133b` | `attempts/r2/response.png` | `867bc8773bae7e4d88beaa20b091eda88e5ea39060eccaa23229ca65ba9e7ab6` | Opaque rectangle over injected Git identity |
| r3-start.png | `56c079a2bcd24320b881e0b0720ea4ab0efb72def0424ef4c1da87fafd67bd23` | `attempts/r3/start.png` | `56c079a2bcd24320b881e0b0720ea4ab0efb72def0424ef4c1da87fafd67bd23` | Unchanged copy |
| r3-response.png | `09dab7c85c323ba878b30ec32919539cabc8b16ca04a95645e2a3deab1e32a5a` | `attempts/r3/response.png` | `09dab7c85c323ba878b30ec32919539cabc8b16ca04a95645e2a3deab1e32a5a` | Unchanged copy |

Response-text originals:

| Attempt | Private exact text SHA-256 | Public text SHA-256 | Treatment |
| --- | --- | --- | --- |
| R1 | `f1d4ce86f04d8406f460c90c1f2f41ce0f285fbbe3718fd2895b7f8bd0d9d0eb` | `f1d4ce86f04d8406f460c90c1f2f41ce0f285fbbe3718fd2895b7f8bd0d9d0eb` | Unchanged |
| R2 | `b5ad655353ed140e386c680dc75558fe43a37ceb9f041793fbc1ed2c39c08857` | `50e921a786c3d73d7cd05a23fa93ff4d85b8ab09044981eae45b211dfc7f1ce8` | Git identity replaced with `[REDACTED_GIT_IDENTITY]` |
| R3 | `40cec0e7ec08c994f4c3114989bf7ea291103719deb37cb08cc41937c89e1a2c` | `40cec0e7ec08c994f4c3114989bf7ea291103719deb37cb08cc41937c89e1a2c` | Unchanged |

These hashes establish file identity between the maintained private evidence and published copies. They do not independently prove what the WorkBuddy service executed.
