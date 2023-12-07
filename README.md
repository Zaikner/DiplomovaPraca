**Generovanie UML modelu z prípadov použitia**<br />
**Diplomová práca**<br />
**Autor: Bc. Filip Zaikner**<br />
**Školiteľ: Ing. Lukaš Radoský**<br />
<br /><br />
**Anotácia:**<br />
Prípady použitia predstavujú skvelý nástroj pre komunikáciu medzi
zákazníkom, analytikom, a v konečnom dôsledku aj architektom či
programátorom. Umožňujú porozumieť procesom, ktoré bude daný informačný
systém či softvér podporovať. Než sú prípady použitia pretavené do finálneho
produktu v podobe zdrojového kódu, prechádzajú mnohými fázami, najmä
návrhom a implementáciou, často vo viacerých iteráciách. Vývoj softvéru
by bol značne rýchlejší a lacnejší, ak by bolo možné z prípadov použitia
automatizovane odvodiť štrukturálne alebo behaviorálne modely, ktoré vizuálne
reprezentujeme napríklad diagramom tried či diagramom sekvencií.
Analyzujte existujúce prístupy pre konverziu prípadov použitia na modely
bližšie zdrojovému kódu. Navrhnite a implementujte metódu pre konverziu
prípadov použitia na niektorý z týchto modelov. Umožnite vizualizáciu
vytvorených modelov. Svoju metódu a jej implementáciu overte na testovacej
množine dát.<br /><br />
**Cieľ práce:**<br />
Vytvorte prototyp využívajúci novú alebo zdokonalenú existujúcu metódu
pre konverziu prípadov použitia na UML model. Vytvorený prototyp bude
poskytovať vizualizáciu vytvorených modelov vo forme diagramov. Overte
svoje riešenie pomocou množiny testovacích dát.<br />

**Denník:**<br />
28.2.23 - prezentácia podobných existujúcich riešení, článkov a návrh evaluácie<br />
14.3.23- základna prvá pipeline tokenizacia + lemma + OIE<br />
28.3.23- úprava podla arch štýlu Chain of Responsibility, získanie use casov na evaluáciu. Návrh parametrizácie. Možnosť osekania času pre processing.<br />
14.4.23 - Dependency parsing + Part of speech, krokovanie<br />
27.4.23 - Projektový slovník, Vykreslovanie UML, Prezentácia<br />
9.5.23 - Kostra latexu<br />
x.07.23 - x.08.23 - Refaktoring<br />
x.09.23 - Prvé stránky textu, optimalizácia pipeline<br />
x.10.23 - Pridanie nového nlp engine, a pridanie všetkych existujúcich konfigurácií aj pre tento engine
x.11.23 - datasety, evaluacia, evaluačny script, písanie
x.12.23 - Preskúmať možnosť parametrizácie správ + písanie

**Future work:**<br />
x.1.24 - Loop/Alt.. fragmenty, vylepšovanie vysledkov<br />
x.2.24 - Algoritmus na nájdenie najlepšie konfiguracie<br />
x.3.24 - Alternativny tok ?(podľa progressu)<br />
x.4.24 - Písanie textu práce<br />
**Prezentácia:** V repozitári.<br />
**PDF:** V repozitári.<br />
**Kostra latexu:** V repozitári.<br /><br />

**Progress - jún.2023:**<br />

Pipeline je rozdelená na 3 časti. Každá časť spracováva Use Case inout metódou NLP.<br />
Ukážková veta: System displays a list of discount offers.<br />
<br />
Časť 1: Open Information Exctraction časť, ktorá dokáže rozdeliť vetu na predmet, prísudok a podmet. Kde podmet symbolizuje odosielateľa, predmet príjmateľa a prísudok správu.<br /> 
Výsledok :   System -->displays -->list <br /> <br />
Časť 2: Dependency parsing čast, ktorá rozdeľuje podľa vetných členov. Rovnako sa využíva podmet, predmet, prísudok ale na rozdiel od OIE aj iné vetné členy.<br /> 
Výsledok :   System-->displays-->list of discount offers. <br /> <br />
Časť 3: Part of speech reprezentuje najintuitívnejší spôsob. Veta sa rozdelí podľa slovných druhov. Ako prijmateľa a odosielateľa zvolíme podstatné mená, ako správu sloveso a využijeme aj iné rozvíjacie slovné druhy.<br /> 
Výsledok :  System-->displays-->list of discount offers. <br /> <br /> 

Ukážkový prípad použitia: <br /> <br /> 

1. System displays a list of discount offers. <br /> 
2. Customer chooses a specific discount offer. <br /> 
3. System displays the discount offer details. <br /> 
4. Customer accepts offer. <br /> 
5. System checks number of available discount offers. <br /> 
6. System inserts discount offer to basket. <br /> <br /> 

Výsledok Part of speech časti Pipeliny : <br />
![POS pipeline - 06.2023](pipeline.png)<br /><br /><br />

**Progress - december.2023:**<br />
Ako sme videli pri pipeline z júna, nie všetky správy boli identifikované správne. Na vine bol NLP engine a model, ktorý nesprávne identifikoval gramatické kategórie slova. 

Výsledok Part of speech časti Pipeliny : <br />
![POS pipeline - 12.2023](pipeline.png)<br /><br /><br />

**Literatúra:**<br />
Deva Kumar Deeptimahanti a Muhammad Ali Babar. „An automated tool for generating UML models from natural language requirements“. In: 2009 IEEE/ACM
International Conference on Automated Software Engineering. IEEE. 2009, s. 680–
682.<br /><br />
Abdelsalam M. Maatuk a Esra A. Abdelnabi. „Generating uml use case and activity diagrams using nlp techniques and heuristics rules“. In: International Conference on Data Science, E-learning and Information Systems 2021. 2021, s. 271–
277.<br /><br />
Jitendra Singh Thakur a Atul Gupta. „Automatic generation of sequence diagram
from use case specification“. In: Proceedings of the 7th India Software Engineering
Conference. 2014, s. 1–6.<br /><br />
Song Yang a Houari Sahraoui. „Towards automatically extracting UML class diagrams from natural language specifications“. In: Proceedings of the 25th International Conference on Model Driven Engineering Languages and Systems: Companion Proceedings. 2022, s. 396–403.<br /><br />
Tao Yue, Lionel C Briand a Yvan Labiche. „An Automated Approach to Transform
Use Cases into Activity Diagrams.“ In: ECMFA 10 (2010), s. 337–353.<br />

