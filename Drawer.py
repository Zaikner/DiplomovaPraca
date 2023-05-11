import plantuml
class Drawer:
    def __init__(self,data):
        print('aspon zapol')
        self.data = data
        print(self.data)

    def create_PlantUml(self,):
        participated = []
        with open('output.puml', 'w') as file:
            file.write('@startuml \n')
            for num in range(1, len(self.data) + 1):
                if self.data[num]['subjects']['POS'].replace(' ', '_') not in participated:
                    file.write('actor ' + self.data[num]['subjects']['POS'].replace(' ', '_') + '\n')

            for num in range(1,len(self.data)+1):
                if self.data[num]['subjects']['POS'].replace(' ','_') not in participated:
                    participated.append(self.data[num]['subjects']['POS'].replace(' ', '_'))
                if self.data[num]['objects']['POS'].replace(' ', '_') not in participated:
                    file.write('participant ' + self.data[num]['objects']['POS'].replace(' ', '_') + '\n')
                    participated.append(self.data[num]['relations']['POS'].replace(' ','_'))
                file.write(self.data[num]['subjects']['POS'].replace(' ','_') + ' --> ' + self.data[num]['objects']['POS'].replace(' ','_')+ ': ' + self.data[num]['relations']['POS'].replace(' ','_')+'\n')
            file.write('@enduml \n')

        url = "http://www.plantuml.com/plantuml/png/"

        plantuml.PlantUML(url).processes_file('output.puml')

        # The file is automatically closed outside the 'with' block
        # for i in data:
