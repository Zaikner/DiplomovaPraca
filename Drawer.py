import plantuml
class Drawer:
    def __init__(self,data):
        self.data = data
        print(self.data)

    def create_PlantUml(self,):
        print('Fragments found')
        print(self.data['fragments'])
        participated = []
        with open('output.puml', 'w') as file:
            file.write('@startuml\n')
            for num in range(1, len(self.data)):
                if self.data[num]['subjects'].replace(' ', '_') not in participated:
                    file.write('actor ' + self.data[num]['subjects'].replace(' ', '_') + '\n')
                    participated.append(self.data[num]['subjects'].replace(' ', '_'))

            for num in range(1,len(self.data)):
                if self.data[num]['subjects'].replace(' ','_') not in participated:
                    participated.append(self.data[num]['subjects'].replace(' ', '_'))
                if self.data[num]['objects'].replace(' ', '_') not in participated:
                    file.write('participant ' + self.data[num]['objects'].replace(' ', '_') + '\n')
                    participated.append(self.data[num]['relations'].replace(' ','_'))

                for fragment in self.data['fragments']:
                    if fragment.start_sentence == num:
                        file.write(fragment.type+'\n')
                        print('start'+str(fragment.start_sentence))
                        print('end'+str(fragment.end_sentence))
                    elif fragment.end_sentence == num:
                        file.write('end\n')

                file.write(self.data[num]['subjects'].replace(' ','_') + ' --> ' + self.data[num]['objects'].replace(' ','_')+ ': ' + self.data[num]['relations'].replace(' ','_')+'\n')
            file.write('@enduml\n')

        url = "http://www.plantuml.com/plantuml/png/"

        plantuml.PlantUML(url).processes_file('output.puml')

        # The file is automatically closed outside the 'with' block
        # for i in data:
