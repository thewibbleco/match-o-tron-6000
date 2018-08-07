import config, json, pprint

with open(config.MATCH_SOURCE_FILE,'r') as f:
    contents = f.read()

DATA = json.loads(contents)

while True:
    key_a = raw_input("Artist to match: ")
    if key_a == "x": break
    key_b = raw_input("Match to check: ")
    if key_b == "x": break

    if key_a and key_b:
        print DATA[key_a][key_b]
    elif key_a and not key_b:
        print DATA[key_a]
    else:
        print "Must enter at least the artist to match."
