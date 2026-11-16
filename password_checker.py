
import re
from zxcvbn import zxcvbn

COMMON_PASSWORDS = {
    "password", "password123", "123456", "12345678",
    "qwerty", "admin", "letmein", "welcome",
    "iloveyou", "abc123"
}


def analyze_password(password):
    if not password:
        return {
            "score": 0,
            "strength": "Not Entered",
            "length": 0,
            "checks": {},
            "suggestions": ["Enter a password to begin analysis."]
        }

    length = len(password)

    checks = {
        "At least 8 characters": length >= 8,
        "At least 12 characters": length >= 12,
        "Contains uppercase letters": bool(re.search(r"[A-Z]", password)),
        "Contains lowercase letters": bool(re.search(r"[a-z]", password)),
        "Contains numbers": bool(re.search(r"\d", password)),
        "Contains special characters": bool(
            re.search(r"[^A-Za-z0-9]", password)
        )
    }

    result = zxcvbn(password)
    score = result["score"]

    if password.lower() in COMMON_PASSWORDS:
        score = 0

    if score == 0:
        strength = "Very Weak"
    elif score == 1:
        strength = "Weak"
    elif score == 2:
        strength = "Moderate"
    elif score == 3:
        strength = "Strong"
    else:
        strength = "Very Strong"

    suggestions = []

    if length < 12:
        suggestions.append("Use at least 12 characters.")

    if not checks["Contains uppercase letters"]:
        suggestions.append("Add uppercase letters.")

    if not checks["Contains lowercase letters"]:
        suggestions.append("Add lowercase letters.")

    if not checks["Contains numbers"]:
        suggestions.append("Include numbers.")

    if not checks["Contains special characters"]:
        suggestions.append("Include special characters.")

    if password.lower() in COMMON_PASSWORDS:
        suggestions.append("Avoid commonly used passwords.")

    if result.get("feedback", {}).get("warning"):
        suggestions.append(result["feedback"]["warning"])

    for suggestion in result.get("feedback", {}).get("suggestions", []):
        if suggestion not in suggestions:
            suggestions.append(suggestion)

    if not suggestions:
        suggestions.append("Your password has good estimated strength.")

    return {
        "score": score,
        "strength": strength,
        "length": length,
        "checks": checks,
        "suggestions": suggestions
    }
