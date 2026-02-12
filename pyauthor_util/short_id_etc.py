def short_id(quirkrec):
    cv_str = quirkrec["qr-cv"]
    chnu, vrnu = tuple(int(part) for part in cv_str.split(":"))
    cn02vn02 = f"{chnu:02d}{vrnu:02d}"
    wid = quirkrec.get("qr-word-id")
    wid_str = f"-{wid}" if wid else ""
    return cn02vn02 + wid_str
