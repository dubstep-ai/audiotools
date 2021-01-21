import codecs
import os

INPUT_DIRECTORY = "/Users/arvindsuresh/projects/ai/datasets/subtitles/"
OUTPUT_DIRECTORY = "/tmp/"

def write_to_file(fd, line):
    # substitute multiple spaces with a single space, remove trailing/leading whitespaces
    normalized_line = ' '.join(line.strip().split())
    
    if (normalized_line.endswith(('?', '!', '।'))):
        normalized_line += '\n'
    else:
        normalized_line += ' '
    fd.write(normalized_line)

def extract_dialogues_from_ttml_file(filename):
    with codecs.open(INPUT_DIRECTORY + filename, 'r', encoding='utf8') as en, \
      codecs.open(OUTPUT_DIRECTORY + 'output.txt', 'a+', encoding='utf8') as cleaned_en:
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
     
            # remove whitespaces for good measure, since we're using startswith next
            cleaned_line = cleaned_line.strip()
     
            # hyphens indicate line has dialogue spoken by multiple speakers, break into multiple lines
            # make sure to remove empty strings (denoted by None in filter statement below)
            if (cleaned_line.startswith("-")):
                lines = list(filter(None, cleaned_line.split("-")))
                for individual_line in lines:
                    write_to_file(cleaned_en, individual_line)
            else:
                write_to_file(cleaned_en, cleaned_line)
    cleaned_en.close()

def filter_problematic_lines():
    sum_len = 0
    total_lines = 0
    with codecs.open(OUTPUT_DIRECTORY + 'output.txt', 'r', encoding='utf8') as d, \
      codecs.open(OUTPUT_DIRECTORY + 'filtered.txt', 'w', encoding='utf8') as f:
        for line in d:
            if (len(line) < 50) or (len(line) > 130) or \
              ("..." in line) or ("\"" in line) or \
              (any(char.isdigit() for char in line)) or \
              (any(x in line for x in [":", "(", "\'", "\.", "-", "[", "]"])) or \
              (u'\u200d' in line):
                print("skipping")
            else:
                f.write(line) 
    print("filtering complete.") 

# Step 1: many ttml files to one dialogue file
for f in os.listdir(INPUT_DIRECTORY):
    if not f.endswith('ttml'):
        continue
    print("processing file : " + f)
    extract_dialogues_from_ttml_file(f)

#Step 2:
filter_problematic_lines() 
