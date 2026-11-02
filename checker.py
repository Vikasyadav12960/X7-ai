import re
from urllib.parse import urlparse

RISKY_TLDS = {".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".click", ".zip", ".work"}
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly"}
SCAM_WORDS = ["free", "recharge", "prize", "winner", "claim", "verify",
              "login", "update", "secure", "kyc", "otp", "internship", "offer"]

# brand name -> its real domains
BRANDS = {
    "paypal": ("paypal.com",),
    "google": ("google.com",),
    "amazon": ("amazon.com", "amazon.in"),
    "paytm": ("paytm.com",),
    "phonepe": ("phonepe.com",),
    "sbi": ("sbi.co.in",),
    "hdfc": ("hdfcbank.com",),
    "icici": ("icicibank.com",),
    "instagram": ("instagram.com",),
    "whatsapp": ("whatsapp.com",),
    "microsoft": ("microsoft.com",),
}


def check_url(raw_url):
    """Returns (score, verdict, reasons). Score goes from 0 to 100."""
    url = raw_url.strip()
    had_scheme = "://" in url
    parsed = urlparse(url if had_scheme else "http://" + url)
    host = (parsed.hostname or "").lower()

    score = 0
    reasons = []

    if not host:
        return 100, "dangerous", ["This does not look like a valid link."]

    # 1. IP address instead of a domain name
    if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host):
        score += 30
        reasons.append("Uses an IP address instead of a domain name.")

    # 2. '@' trick: http://google.com@evil.com really goes to evil.com
    if "@" in parsed.netloc:
        score += 30
        reasons.append("Contains '@', which can hide the real destination.")

    # 3. Punycode (lookalike characters)
    if "xn--" in host:
        score += 25
        reasons.append("Domain uses lookalike characters (punycode).")

    # 4. Brand impersonation
    for brand, real_domains in BRANDS.items():
        if brand in host:
            is_real = any(host == d or host.endswith("." + d) for d in real_domains)
            if not is_real:
                score += 35
                reasons.append(f"Mentions '{brand}' but is not the real {brand} website.")
                break

    # 5. Risky domain endings
    if any(host.endswith(tld) for tld in RISKY_TLDS):
        score += 15
        reasons.append("Uses a domain ending often seen in scam sites.")

    # 6. URL shorteners hide the real destination
    if host in SHORTENERS:
        score += 15
        reasons.append("Shortened link: the real destination is hidden.")

    # 7. Too many subdomains
    if host.count(".") >= 4:
        score += 15
        reasons.append("Has an unusually long chain of subdomains.")

    # 8. Many hyphens in the domain
    if host.count("-") >= 3:
        score += 10
        reasons.append("Domain contains many hyphens.")

    # 9. Very long URL
    if len(url) > 75:
        score += 10
        reasons.append("The link is unusually long.")

    # 10. Explicit plain http (only if the user typed it)
    if had_scheme and parsed.scheme == "http":
        score += 10
        reasons.append("Not using HTTPS (connection is not encrypted).")

    # 11. Scam keywords (capped so one rule can't dominate)
    hits = [w for w in SCAM_WORDS if w in url.lower()]
    if hits:
        score += min(10 * len(hits), 30)
        reasons.append("Contains suspicious words: " + ", ".join(hits) + ".")

    score = min(score, 100)
    if score >= 60:
        verdict = "dangerous"
    elif score >= 30:
        verdict = "suspicious"
    else:
        verdict = "safe"
        if not reasons:
            reasons.append("No red flags found by our rules.")

    return score, verdict, reasons