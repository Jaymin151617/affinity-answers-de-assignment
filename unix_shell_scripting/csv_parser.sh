#!/bin/bash

#==============================================================================
# Description:
# Downloads and processes a CSV file from the provided URL. Validates the
# expected columns, extracts Company Name, Headquarters Location, and Founded,
# sorts the results by Founding Year, and displays them in a formatted table.
#
# Usage:
#   ./script.sh <CSV_URL>
#==============================================================================

# Check that exactly one URL argument was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <CSV_URL>"
    exit 1
fi

# Store the provided CSV URL
URL="$1"

# Download the CSV and process the required columns
curl -fsSL "$URL" | gawk -v FPAT='([^,]*)|(\"([^\"]|\"\")*\")' '
BEGIN {
    # Use tabs between output columns
    OFS = "\t"
}

NR == 1 {
    # Check that the CSV has the expected columns
    if ($2 != "Security" || $5 != "Headquarters Location" || $8 != "Founded") {
        print "Error: Unexpected CSV format." > "/dev/stderr"
        exit 1
    }

    # Print the output header after validation succeeds
    print "Company Name", "Location", "Founding Year"
}

NR > 1 {
    # Remove surrounding quotes from CSV fields
    gsub(/^"|"$/, "", $2)
    gsub(/^"|"$/, "", $5)
    gsub(/^"|"$/, "", $8)

    # Extract Company Name, Location, and Founding Year
    print $2, $5, $8
}
' | {
    # Keep the header at the top and sort the data
    read -r header
    echo "$header"

    # Sort the remaining rows by Founding Year in ascending order
    sort -t $'\t' -k3,3n
} | column -t -s $'\t'
