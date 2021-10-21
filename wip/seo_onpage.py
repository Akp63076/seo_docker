from seoanalyzer import analyze
import json
output = analyze("https://collegedunia.com/", "https://collegedunia.com/sitemap-daily-index.xml")

print(output)

with open('do_re_mi.json', 'w') as json_file:
    json.dump(output, json_file)