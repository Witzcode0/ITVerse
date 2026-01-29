import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_mobile(number):
    pattern = r'^\+[1-9]\d{1,3}\d{6,14}$'
    return bool(re.match(pattern, number))

def validate_password(password):
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")

    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")

    if not re.search(r"\d", password):
        errors.append("Password must contain at least one digit.")

    if not re.search(r"[@$!%*?&]", password):
        errors.append("Password must contain at least one special character (@$!%*?&).")

    if errors:
        return False, " ".join(errors)
    
    return True, "Password is valid"

def match_password(password, confirm_password):
    if not password or not confirm_password:
        return False, "Password and Confirm Password are required"

    if password != confirm_password:
        return False, "Password and Confirm Password do not match"

    return True, "Password matched successfully"