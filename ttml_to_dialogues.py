import codecs

INPUT_DIRECTORY = "/Users/arvindsuresh/Movies/"
OUTPUT_DIRECTORY = "/tmp/"

def write_to_file(fd, line):
    normalized_line = line.strip()
    if (normalized_line.endswith(('?', '!', '।')))
        normalized_line += '\n'
    else 
        normalized_line += ' '
    print(normalized_line)
    fd.write(normalized_line)

with codecs.open(INPUT_DIRECTORY + '[S01.E01] The Marvelous Mrs. Maisel - Pilot.HI.ttml', 'r', encoding='utf8') as en, \
  codecs.open(OUTPUT_DIRECTORY + 'output.txt', 'w') as cleaned_en:
    # (what a hack!) skip lines till we get to the body
    for header in en:
        if "body" in header:
            break
        else:
            print("skipping : " + header)

    for line in en:
        # remove metatags
        cleaned_line = line[102:-5]

        # remove line break
        cleaned_line = cleaned_line.replace('<br />', ' ')
        # remove span
        cleaned_line = cleaned_line.replace('<span>', ' ')
        cleaned_line = cleaned_line.replace('</span>', ' ')
        
        # hyphens indicate line has dialogue spoken by multiple speakers, break into multiple lines
        # make sure to remove empty strings (denoted by None in filter statement below)
        if (cleaned_line.startswith("-")):
            lines = list(filter(None, cleaned_line.split("-")))
            for individual_line in lines:
                write_to_file(cleaned_en, individual_line)
        else:
            write_to_file(cleaned_en, cleaned_line)

cleaned_en.close()
print("complete...")

