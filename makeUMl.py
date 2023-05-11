import plantuml

import plantuml

url = "http://www.plantuml.com/plantuml/png/"

with open('output.puml', 'r') as file:
    uml_code = file.read()

output_file = 'output.png'
plantuml.PlantUML(url).processes_file('output.puml')

print(f"PlantUML diagram generated and saved as {output_file}")