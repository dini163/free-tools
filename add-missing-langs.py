#!/usr/bin/env python3
import re

# Read the i18n.js file
with open('js/i18n.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the missing languages with English placeholders
missing_langs = {
    'es': 'Spanish',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ko': 'Korean'
}

# For each missing language, add it to the TRANSLATIONS object
for lang_code, lang_name in missing_langs.items():
    # Check if the language already exists
    if f'"{lang_code}":' in content:
        print(f'✅ {lang_name} ({lang_code}) already exists, skipping...')
        continue
    
    print(f'📝 Adding {lang_name} ({lang_code}) translations...')
    
    # Create a minimal translation object with English placeholders
    # We'll copy the English translations as a base
    en_match = re.search(r'    "en": \{', content)
    if not en_match:
        print(f'❌ Could not find English translations, skipping {lang_code}')
        continue
    
    # Find the end of the English translations (next "xx": \{ or end of TRANSLATIONS)
    en_start = en_match.start()
    next_lang = re.search(r'    "[a-z]{2}(-[A-Z]{2})?": \{', content[en_start + 10:])
    
    if next_lang:
        en_end = en_start + 10 + next_lang.start()
        en_content = content[en_start:en_end]
    else:
        # English is the last language, find the end of TRANSLATIONS
        trans_end = content.find('\n};', en_start)
        if trans_end == -1:
            print(f'❌ Could not find end of TRANSLATIONS, skipping {lang_code}')
            continue
        en_content = content[en_start:trans_end]
    
    # Now create the new language object by replacing the language code
    new_content = en_content.replace('"en":', f'"{lang_code}":')
    
    # Add the new language before the closing of TRANSLATIONS
    # Find the place to insert (before the last `    }\n};`)
    insert_pos = content.rfind('    }\n};')
    if insert_pos == -1:
        print(f'❌ Could not find insertion point, skipping {lang_code}')
        continue
    
    # Insert the new language
    content = content[:insert_pos] + new_content + '\n\n' + content[insert_pos:]
    print(f'✅ Added {lang_name} ({lang_code}) translations')

# Write the updated content back
with open('js/i18n.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('\n🎉 Successfully updated i18n.js with missing languages!')
