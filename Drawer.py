import nltk
import plantuml
from nltk.corpus import wordnet as wn

class Drawer:
    def __init__(self,data,configuration):
        self.data = data
        self.configuration = configuration
        print(self.data)

    def create_PlantUml(self,):
        print('Fragments found')
        print(self.data['fragments'])
        participated = []
        actorsActivated = []
        with open('output.puml', 'w') as file:
            file.write('@startuml\n')
            # TODO: aby to nemusel byt rovnaky string
            # for num in range(1, len(self.data)):
            #     if self.data[num]['subjects'].replace(' ', '_') not in participated and self.data[num]['subjects'].replace(' ', '_')!= self.configuration.system:
            #         file.write('actor ' + self.data[num]['subjects'].replace(' ', '_') + '\n')
            #         participated.append(self.data[num]['subjects'].replace(' ', '_'))

            for num in range(1, len(self.data)):
                if len(self.data[num]['subjects'].replace(' ', '_')) > len(self.configuration.system)and not self.is_user(self.data[num]['subjects'].replace(' ', '_')) : \
                        # and len(self.data[num]['subjects'].replace(' ', '_')) != self.configuration.users[num].text \

                    self.configuration.system = self.data[num]['subjects'].replace(' ', '_')

            for num in range(1, len(self.data)):
                if not self.is_user(self.data[num]['subjects'].replace(' ', '_')): \
                        # and len(self.data[num]['subjects'].replace(' ', '_')) != self.configuration.users[num].text \

                    self.data[num]['subjects'] = self.configuration.system
            for user in self.configuration.users.values():
            #     if self.data[num]['subjects'].replace(' ', '_') != self.configuration.users[num].text:
            #         self.data[num]['subjects']= self.configuration.system

                file.write('actor ' + user.text.replace(' ', '_') + '\n')
                participated.append(user.text.replace(' ', '_'))
            file.write('participant ' + self.configuration.system.replace(' ', '_') + '\n')
            participated.append(self.configuration.system.replace(' ', '_'))
            file.write('activate ' + self.configuration.system.replace(' ', '_') + '\n')

            if self.configuration.pattern == 'mvc':
                for num in range(1, len(self.data)):
                    # if self.data[num]['objects'].replace(' ', '_') not in participated and (
                    #         self.data[num]['subjects'] == self.configuration.system):
                    #     file.write('participant ' + self.data[num]['objects'].replace(' ', '_') + '\n')
                    #     participated.append(self.data[num]['relations'].replace(' ', '_'))

                    for fragment in self.data['fragments']:
                        if fragment.start_sentence == num:
                            file.write(fragment.type + '\n')
                            print('start' + str(fragment.start_sentence))
                            print('end' + str(fragment.end_sentence))
                        elif fragment.end_sentence == num:
                            file.write('end\n')
                    #  tu sa dorabaju relacie
                    if not self.configuration.parameters:
                        print('nedostal sa')
                        file.write('participant ' + self.data[num]['objects'].replace(' ', '_') + 'View'.replace(' ',
                                                                                                                 '_') + '\n')
                        participated.append(self.data[num]['objects'].replace(' ', '_') + 'View')
                        file.write(
                            'participant ' + self.data[num]['objects'].replace(' ', '_') + 'Controller'.replace(' ',
                                                                                                                '_') + '\n')
                        participated.append(self.data[num]['objects'].replace(' ', '_') + 'View')
                        file.write('participant ' + self.data[num]['objects'].replace(' ', '_') + 'Model'.replace(' ',
                                                                                                                  '_') + '\n')
                        participated.append(self.data[num]['objects'].replace(' ', '_') + 'View')
                        if (self.data[num]['subjects'] == self.configuration.system):

                            # file.write(self.data[num]['subjects'].replace(' ','_') + ' -> ' + self.data[num]['objects'].replace(' ','_')+ ': ' + self.data[num]['relations'].replace(' ','_')+'()\n')
                            file.write(self.configuration.system.replace(' ', '_') + ' -> ' + self.data[num]['objects'].replace(' ', '_')+'view' + ': ' + self.data[num]['relations'].replace(' ','_') + '()\n')
                            file.write(self.data[num]['objects'].replace(' ', '_')+'view' + ' -> ' + self.data[num]['objects'].replace(' ', '_') + 'controller' + ': ' + 'handle_'+ self.data[num]['relations'].replace(' ','_')+ '()\n')
                            file.write(self.data[num]['objects'].replace(' ', '_') + 'controller' + ' -> ' + self.data[num]['objects'].replace(' ', '_') + 'model' + ': ' + 'get_data' + '()\n')
                            file.write(self.data[num]['objects'].replace(' ', '_') + 'model' + ' --> ' + self.data[num]['objects'].replace(' ', '_') + 'controller' + ': ' + 'return_data' + '()\n')
                            file.write(self.data[num]['objects'].replace(' ', '_') + 'controller' + ' --> ' + self.data[num]['objects'].replace(' ', '_') + 'view' + ': ' + 'update_view' + '()\n')
                            file.write(self.data[num]['objects'].replace(' ', '_') + 'view' + ' --> ' + self.configuration.system.replace(' ', '_') + ': ' +'show_view' + '()\n')


                            # file.write('activate ' + self.data[num]['objects'].replace(' ', '_') + '\n')
                            # file.write('deactivate ' + self.data[num]['objects'].replace(' ', '_') + '\n')



                        else:
                            # file.write(self.data[num]['subjects'].replace(' ','_') + ' -> ' + self.configuration.system+ ': ' + self.data[num]['relations'].replace(' ', '_') +'_'+ self.data[num]['objects']+ '()\n')
                            # file.write(
                            #     self.configuration.users[num].text.replace(' ', '_') + ' -> ' + self.configuration.system + ': ' +
                            #     self.data[num]['relations'].replace(' ', '_') + '_' + self.data[num][
                            #         'objects'] + '()\n')

                            # if self.data[num]['subjects'].replace(' ','_') not in actorsActivated:
                            if self.configuration.users[num].text.replace(' ', '_') not in actorsActivated:
                                actorsActivated.append(self.configuration.users[num].text.replace(' ', '_'))
                                # file.write('activate ' + self.configuration.users[num].text.replace(' ', '_') + '\n')

                            file.write(self.configuration.users[num].text.replace(' ', '_') + ' -> ' + self.data[num][
                                'objects'].replace(' ', '_') + 'View' + ': on_' + self.data[num]['relations'].replace(' ',
                                                                                                                   '_') + '()\n')
                            file.write(self.data[num]['objects'].replace(' ', '_') + 'View' + ' -> ' + self.data[num][
                                'objects'].replace(' ', '_') + 'Controller' + ': ' + 'Handle_' + self.data[num][
                                           'relations'].replace(' ', '_') + '()\n')
                            file.write(
                                self.data[num]['objects'].replace(' ', '_') + 'Controller' + ' -> ' + self.data[num][
                                    'objects'].replace(' ', '_') + 'Model' + ': ' + 'Get_Data' + '()\n')
                            file.write(self.data[num]['objects'].replace(' ', '_') + 'Model' + ' --> ' + self.data[num][
                                'objects'].replace(' ', '_') + 'Controller' + ': ' + 'Return_Data' + '()\n')
                            file.write(
                                self.data[num]['objects'].replace(' ', '_') + 'Controller' + ' --> ' + self.data[num][
                                    'objects'].replace(' ', '_') + 'View' + ': ' + 'Update_View' + '()\n')
                            file.write(self.data[num]['objects'].replace(' ',
                                                                         '_') + 'View' + ' --> ' + self.configuration.system.replace(
                                ' ', '_') + ': ' + 'Show_View' + '()\n')
                    else:
                        # TODO: pridat usera
                        secondary_relations = []
                        print('aspon sa dostal do tejto časti')
                        print(self.data[num])
                        for rel in self.data[num]['relations'].split():
                            if rel != self.data[num]['main_relation']:
                                secondary_relations.append(rel)
                        secondary_relations = ' '.join(secondary_relations)
                        if (self.data[num]['subjects'] == self.configuration.system):
                            file.write(self.data[num]['subjects'].replace(' ', '_') + ' -> ' + self.data[num][
                                'objects'].replace(' ', '_') + ': ' + self.data[num]['main_relation'].replace(' ',
                                                                                                              '_') + '(' + secondary_relations + ')\n')
                            file.write('activate ' + self.data[num]['objects'].replace(' ', '_') + '\n')
                            file.write('deactivate ' + self.data[num]['objects'].replace(' ', '_') + '\n')

                        else:
                            file.write(self.data[num]['subjects'].replace(' ',
                                                                          '_') + ' -> ' + self.configuration.system + ': ' +
                                       self.data[num]['main_relation'].replace(' ', '_') + '_' + self.data[num][
                                           'objects'] + '(' + secondary_relations + ')\n')
                            if self.data[num]['subjects'].replace(' ', '_') not in actorsActivated:
                                actorsActivated.append(self.data[num]['subjects'].replace(' ', '_'))
                                file.write('activate ' + self.data[num]['subjects'].replace(' ', '_') + '\n')
            else:
                for num in range(1,len(self.data)):
                    # if self.data[num]['subjects'].replace(' ','_') not in participated and self.data[num]['subjects'].replace(' ', '_')!= self.configuration.system:
                    #     participated.append(self.data[num]['subjects'].replace(' ', '_'))
                    # elif self.data[num]['subjects'].replace(' ', '_') not in participated and self.data[num][
                    #     'subjects'].replace(' ', '_') == self.configuration.system:
                    #     file.write('participant ' + self.data[num]['subjects'].replace(' ', '_') + '\n')
                    #     file.write('activate ' + self.data[num]['subjects'].replace(' ', '_') + '\n')
                    #     participated.append(self.data[num]['subjects'].replace(' ', '_'))

                    if self.data[num]['objects'].replace(' ', '_') not in participated and (self.data[num]['subjects'] == self.configuration.system):
                        file.write('participant ' + self.data[num]['objects'].replace(' ', '_') + '\n')
                        participated.append(self.data[num]['relations'].replace(' ','_'))

                    for fragment in self.data['fragments']:
                        print(fragment.type,fragment.fragment_number,fragment.start_sentence)
                        if fragment.type in ['LOOP','PAR']:
                            if fragment.start_sentence == num:
                                file.write(fragment.type+' '+fragment.text+ '\n')
                                print('start'+str(fragment.start_sentence))
                        elif fragment.type in ['OPT']:
                            if fragment.start_sentence == num:
                                file.write(fragment.type +' ' + fragment.text +'\n')
                                print('start' + str(fragment.start_sentence))
                        # elif fragment.end_sentence == num:
                        #     file.write('end\n')
                    #  tu sa dorabaju relacie
                    if not self.configuration.parameters:
                        print('nedostal sa')
                        if (self.data[num]['subjects'] == self.configuration.system):
                            # file.write(self.data[num]['subjects'].replace(' ','_') + ' -> ' + self.dat  a[num]['objects'].replace(' ','_')+ ': ' + self.data[num]['relations'].replace(' ','_')+'()\n')
                            file.write(self.configuration.system.replace(' ', '_') + ' -> ' + self.data[num]['objects'].replace( ' ', '_') + ': ' + self.data[num]['relations'].replace(' ', '_') + '()\n')
                            file.write('activate '+ self.data[num]['objects'].replace(' ','_')+'\n')
                            file.write('deactivate ' + self.data[num]['objects'].replace(' ', '_') + '\n')



                        else:
                            # file.write(self.data[num]['subjects'].replace(' ','_') + ' -> ' + self.configuration.system+ ': ' + self.data[num]['relations'].replace(' ', '_') +'_'+ self.data[num]['objects']+ '()\n')
                            if num in self.configuration.users.keys():
                                file.write(self.configuration.users[num].text.replace(' ','_') + ' -> ' + self.configuration.system+ ': ' + self.data[num]['relations'].replace(' ', '_') +'_'+ self.data[num]['objects']+ '()\n')

                                # if self.data[num]['subjects'].replace(' ','_') not in actorsActivated:
                                if self.configuration.users[num].text.replace(' ', '_') not in actorsActivated:
                                    actorsActivated.append(self.configuration.users[num].text.replace(' ','_'))
                                    file.write('activate '+self.configuration.users[num].text.replace(' ','_') +'\n')
                    else:
                        # TODO: pridat usera
                        secondary_relations = []
                        print('aspon sa dostal do tejto časti')
                        print(self.data[num])
                        for rel in self.data[num]['relations'].split():
                            if rel!= self.data[num]['main_relation']:
                                secondary_relations.append(rel)
                        secondary_relations = ' '.join(secondary_relations)
                        if (self.data[num]['subjects'] == self.configuration.system):
                            file.write(self.data[num]['subjects'].replace(' ', '_') + ' -> ' + self.data[num]['objects'].replace(' ', '_') + ': ' + self.data[num]['main_relation'].replace(' ', '_') + '('+secondary_relations+')\n')
                            file.write('activate ' + self.data[num]['objects'].replace(' ', '_') + '\n')
                            file.write('deactivate ' + self.data[num]['objects'].replace(' ', '_') + '\n')

                        else:
                            file.write(self.data[num]['subjects'].replace(' ', '_') + ' -> ' + self.configuration.system + ': ' + self.data[num]['main_relation'].replace(' ', '_') + '_' + self.data[num]['objects'] + '('+secondary_relations+')\n')
                            if self.data[num]['subjects'].replace(' ', '_') not in actorsActivated:
                                actorsActivated.append(self.data[num]['subjects'].replace(' ', '_'))
                                file.write('activate ' + self.data[num]['subjects'].replace(' ', '_') + '\n')
                    for fragment in self.data['fragments']:
                        if fragment.end_sentence == num:
                            file.write('end\n')



            file.write('@enduml\n')

        url = "http://www.plantuml.com/plantuml/png/"

        plantuml.PlantUML(url).processes_file('output.puml')
        self.configuration.system = ''
        # The file is automatically closed outside the 'with' block
        # for i in data:

    def is_user(self, word):
        word = nltk.WordNetLemmatizer().lemmatize(word.lower())

        synsets = wn.synsets(word)

        for synset in synsets:
            hypernyms = synset.hypernyms()
            for hypernym in hypernyms:
                if 'person' in hypernym.lexname():
                    return True
        return False
