# Security Policy

## Supported Versions

Only the latest release receives security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you find a security vulnerability, **please do not open a public issue**.

Instead, report it privately via GitHub's [Security Advisories](https://github.com/godhoks/pdf2epub/security/advisories/new).

Please include:

- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

You can expect an initial response within 7 days.

## Scope

This project shells out to [Calibre](https://calibre-ebook.com/)'s `ebook-convert` for the actual PDF→EPUB conversion. Vulnerabilities in Calibre itself should be reported to the [Calibre project](https://github.com/kovidgoyal/calibre/security).
