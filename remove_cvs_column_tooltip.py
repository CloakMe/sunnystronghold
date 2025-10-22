input_file = "Issues_Vector21-periodicreview-oct25.csv"
output_file = "Issues_Vector21-periodicreview-oct25o.csv"

with open(input_file, "r", encoding="utf-8") as fin, open(output_file, "w", encoding="utf-8") as fout:
    for line in fin:
        first_comma = line.find("\",\"")
        if first_comma != -1:
            second_comma = line.find("\",\"", first_comma + 1)
            if second_comma != -1:
                # Remove text between first and second comma (including second comma)
                new_line = line[:first_comma+1] + line[second_comma+1:]
                fout.write(new_line)
                continue
        # If not enough commas to operate, write line as is
        fout.write(line)
