import re
import os
import pathlib


def proccess_raw_data(raw_file: str, out_file: str):

    with open(raw_file, 'r', encoding="Windows-1251") as r_file, open(out_file, "a", encoding="UTF-8") as out:
        text = r_file.read()
        
        
        year = re.search(r"date=\"(?P<year>[\d]{4})", text)['year']

        text = re.sub(r"[\t ]+({|})", "\t(", text) #all {} brackets inside are turned into ()
        pattern = re.compile(r"\d+=\n{\n\tname=[-\w\n\t\".= ()]+}", re.MULTILINE) # info inside {} brackets
        # 2688 - id of last province
        provinces = re.findall(pattern, text)[0:2689]
		
		
		#name of the province
        prov_pattern = re.compile(r"name=\"(?P<name>[-\w. ]+)\"")

        #Tag of the owner
        country_pattern = re.compile(r"owner=\"(?P<country>[A-Z]{3})\"")

        #Type of pop and it's info
        pop_pattern = re.compile(r"(?P<pop_type>aristocrats|craftsmen|bureaucrats|clerks|soldiers|artisans|labourers|farmers|capitalists|officers|clergymen|serfs|slaves)="
                                 r"\n\t\(\n\t\tid=\d+\n\t\tsize=(?P<pop_size>\d+)\n\t\t(?P<pop_culture>\w+)=(?P<pop_religion>\w+)")

        for province in provinces:
            prov_name = re.search(prov_pattern, province).group('name')
            country_name = re.search(country_pattern, province)
            country_name = country_name.group("country") if country_name is not None else "None"

            pops = re.findall(pop_pattern, province)
            for pop in pops:
                out.write(f"{year},{country_name},{prov_name},{pop[0]},{pop[1]},{pop[2]},{pop[3]}\n")



            
        

def main():
    path = pathlib.Path("input")

    files = os.listdir(path)

    for file in files:
            proccess_raw_data( path.joinpath(pathlib.Path(file)), "output.csv")

main()
