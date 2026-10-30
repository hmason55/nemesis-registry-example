# NEMESIS Registry Example

A text-only staging fixture: a NEMESIS manifest and README, with no APK,
executable scripts, services, or vehicle configuration. This is not a vehicle
application. These files and generated ZIPs may be redistributed for testing.

## Build and releases

Pushes to `main` run checks and publish a unique prerelease such as
`0.1.0-build.1`. Pull requests run checks without publishing. For an explicit
version, use **Actions → Publish example package → Run workflow** on `main`.
The manual default is `0.1.0`; use a new version after publication.

Each release includes `nemesis.registry.example-VERSION.zip` and `SHA256SUMS`.
Assets are uploaded to a draft before publication. Tags cannot be moved and
assets cannot be silently replaced. Failed draft uploads can resume on the same
commit; a published version must use a new version instead of being replaced.

Local build: `python build_package.py 0.1.0`.
Tests: `python -m unittest discover -s tests -v`.

## Connect to the staging registry

1. [Install NEMESIS Registry Staging](https://github.com/apps/nemesis-registry-staging/installations/new)
   on this repository. Codex access and the registry App are separate installations.
2. Sign in on the registry publisher page, register
   `hmason55/nemesis-registry-example`, and acknowledge redistribution permission.
3. Select a published release's installer ZIP, enter package ID
   `nemesis.registry.example`, and use its exact internal version, including
   `-build.N` for automatic releases. Do not select GitHub source archives.
4. Submit for trusted validation and administrator approval.

The first package submission is selected manually to establish its repository
relationship. Later release webhooks can propose new versions, but every version
still requires validation and approval. The registry validator downloads the
selected ZIP without executing this repository's build script.
