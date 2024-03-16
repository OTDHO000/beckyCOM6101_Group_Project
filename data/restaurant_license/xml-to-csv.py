import os
import xml.etree.ElementTree as Xet
import pandas as pd

folder_path = 'restaurant-info-hk/xml'
output_folder = 'restaurant-info-hk/csv'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

cols = ["TYPE", "DIST", "LICNO", "SS", "ADR", "INFO", "EXPDATE"]

# Iterate through all XML files in the folder_path
for filename in os.listdir(folder_path):
    if filename.endswith(".xml"):
        xml_file = os.path.join(folder_path, filename)
        csv_file = os.path.join(output_folder, os.path.splitext(filename)[0][1:] + ".csv")
        rows = []
        xmlparse = Xet.parse(xml_file)
        # The data are stored in the <LPS> tag
        root = xmlparse.getroot().find("LPS")

        for i in root:
            
            TYPE = i.find("TYPE").text
            DIST = i.find("DIST").text
            LICNO = i.find("LICNO").text
            SS = i.find("SS").text
            ADR = i.find("ADR").text
            INFO = i.find("INFO").text
            EXPDATE = i.find("EXPDATE").text
            rows.append({"TYPE": TYPE, "DIST": DIST, "LICNO": LICNO, 
                         "SS": SS, "ADR": ADR, "INFO": INFO, "EXPDATE": EXPDATE})

        df = pd.DataFrame(rows, columns=cols)
        df.to_csv(csv_file, index=False)
        print(f"Converted {filename} to {os.path.splitext(filename)[0][1:] + '.csv'}")

print("XML to CSV conversion completed.")
