# Fraud-Detector-V2
Version 2 of the fraud detector

# Motivationen bakom koden

1. Från "Facit" till "Intelligens"
I den första versionen injicerade jag fusk med stenhårda if-satser. Det var som att ge en elev svaren på provet i förväg – de lär sig inget, de bara memorerar. I V2 har jag skapat "brus" och överlappande mönster. Nu måste modellen faktiskt använda sin matematiska "hjärna" för att skilja på en person med otur och en person med uppsåt.

2. "No Black Boxes"
jag har rensat bort onödig kod och tvingat systemet att vara transparent. Genom att använda predict_proba i vår ML-pipeline ser jag nu exakt hur osäker eller säker AI:n är. jag döljer inte modellens misstag; jag redovisar dem så att människor kan fatta bättre beslut.

3. Business ROI (Affärsnytta)
Varje minut en utredare lägger på ett ärligt ärende är förlorade pengar för If.

Precision 95%: jag minimerar risken att anklaga hederliga kunder av misstag.

Recall 73%: jag fångar de flesta fuskare automatiskt, vilket sparar hundratals timmar av manuell granskning.

Resultat: jag har skapat en prioriteringsmaskin som riktar strålkastaren där den behövs mest.

Skapat med ❤️ av Lily - The Data translator