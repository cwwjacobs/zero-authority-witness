"""
Zero Authority Witness — Raw Fetch (optional, stdlib urllib only)

Bounded, explicit, no-cookie, no-persistent-session fetch.
Only used when the Operator deliberately invokes it.
Records what it can for provenance and blind spots.

Hardening:
- Only http/https schemes are allowed (file://, ftp://, etc. are rejected).
- The target host is resolved and rejected if it maps to a loopback,
  link-local (incl. cloud metadata 169.254.169.254), private, multicast,
  reserved, or unspecified address (best-effort SSRF guard).
- Redirects are NOT followed; a redirecting response is surfaced by status.
"""

from __future__ import annotations

import ipaddress
import socket
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict

_ALLOWED_SCHEMES = {"http", "https"}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Disable redirect following so a safe-looking URL cannot be bounced to
    an internal/SSRF target after the pre-fetch validation has already run."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _validate_fetch_target(url: str) -> None:
    """Raise ValueError unless ``url`` is http/https and resolves only to
    globally-routable addresses. Best-effort SSRF guard; see blind spots for
    the residual DNS-rebinding limitation."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"scheme {parsed.scheme!r} not allowed (only http/https)")
    host = parsed.hostname
    if not host:
        raise ValueError("URL has no host")
    try:
        infos = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ValueError(f"could not resolve host {host!r}: {exc}")
    for info in infos:
        ip = ipaddress.ip_address(info[4][0].split("%")[0])
        if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped is not None:
            ip = ip.ipv4_mapped
        if (
            ip.is_loopback
            or ip.is_link_local
            or ip.is_private
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        ):
            raise ValueError(f"host {host!r} resolves to non-global address {ip}")


def raw_fetch(
    url: str,
    timeout: float = 10.0,
    max_bytes: int = 1_000_000,
) -> Dict[str, Any]:
    """
    Performs a minimal GET with no cookies, no auth, short timeout, and no
    redirect following. Returns a dict with status, headers (if available),
    body (truncated), and blind_spots. A blocked or failed fetch is recorded
    in the "error" field rather than raising.
    """
    result: Dict[str, Any] = {
        "url": url,
        "status": None,
        "headers": {},
        "body": None,
        "error": None,
        "blind_spots": [
            "Dynamic JavaScript not executed.",
            "Server-side state not visible.",
            "Authentication-gated content not retrieved.",
            "TOCTOU risk: content may have changed since fetch.",
            "No cookies or session state were sent or stored.",
            "Redirects are not followed; a redirecting response is recorded by status code, not resolved.",
            "SSRF guard validates the resolved address at check time; DNS rebinding between check and connection is not fully prevented.",
        ],
    }

    try:
        _validate_fetch_target(url)
    except ValueError as exc:
        result["error"] = f"blocked: {exc}"
        return result

    opener = urllib.request.build_opener(_NoRedirect)
    req = urllib.request.Request(
        url, headers={"User-Agent": "Zero-Authority-Witness/0.1 (stdlib; bounded)"}
    )
    try:
        with opener.open(req, timeout=timeout) as resp:
            result["status"] = resp.status
            # Headers
            for k, v in resp.getheaders():
                result["headers"][k] = v
            # Body (truncated)
            data = resp.read(max_bytes + 1)
            if len(data) > max_bytes:
                result["body"] = data[:max_bytes].decode("utf-8", errors="replace") + "... [truncated]"
                result["blind_spots"].append("Response body was truncated at max_bytes.")
            else:
                result["body"] = data.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        # A 3xx lands here because redirects are intentionally not followed.
        result["status"] = e.code
        result["error"] = str(e)
    except Exception as e:
        result["error"] = str(e)

    return result
