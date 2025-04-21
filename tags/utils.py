KEYWORDS = {
    'urgent': ['urgent', 'asap', 'immediately'],
    'meeting': ['meeting', 'call', 'sync'],
    'bug': ['bug', 'fix', 'issue', 'error'],
    'design': ['design', 'ui', 'ux', 'mockup'],
    'deploy': ['deploy', 'release', 'launch'],
}

def extract_tags_from_title(title):
    matched_tags = set()

    for tag, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in title.lower():
                matched_tags.add(tag)

    return list(matched_tags)
