import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("netflix_titles.csv") # ez be olvassa nekünk a CSV fájlt.

#======================================================1. feladat==============================================================#
#top 5 forgatási helyszin#

orszagok = (
    df["country"] # ezzel kiválasztjuk melyik oszlopot szeretnénk feldolgozni   
    .dropna() # ez azért kell mert nem minden filmhez van megadva ország, így a NaN értékeket eldobjuk
    .str.split(", ") # ez csak azért kell, hogy a több országot tartalmazó cellákat szétválasszuk, így minden ország külön sorba kerül pl. "USA, canada"
    .explode() # listaban szereplő országokat külön sorba teszi
    .str.strip() # ha a cellákban van felesleges szóköz, azt eltávolítja
)

top10_otszag = orszagok.value_counts().head(10) # value_counts() megszámolja minden ország előfordulását, a head(10) pedig az első 10-et adja vissza.

print(top10_otszag) # ezzel meg kiirjuk a top 10 országot a konzolra


#=========================================================2.feladat===========================================================#
#top 5 filmek korhatár kategória#

ervenyes_korhatar = [
    "TV-MA",
    "TV-14",
    "TV-PG",
    "TV-G",
    "TV-Y",
    "TV-Y7",
    "TV-Y7-FV",
    "R",
    "PG-13",
    "PG",
    "G",
    "NC-17",
    "NR",
    "UR"
]


top5_korhatar = (
    df[df["rating"].isin(ervenyes_korhatar)]["rating"] # meg vizsgálja hogy a általam megadott elemek benne-e vannak a beolvasott adat sorba
    .value_counts() # meg számolja hogy hány olyan elemet talál az adtasora ami az általam megadott értékeknek megdfelel
    .head(5) # vissza adja a top 5-t
)

print(top5_korhatar)


#3. feladat#
#filmek hosszának átlaga és szórása#

filmek = df[df["type"] == "Movie"].copy()

filmek["perc"] = pd.to_numeric(
    filmek["duration"].str.extract(r"(^\d+)\s+min$")[0],
    errors = "coerce"                                           #ez beolvassa a filmek hosszát , majd átváltja percbe az időt.
)

jatekido = filmek["perc"].dropna().to_numpy() #droppna eltávolítja a hiányzó karatkereket, to_numpy pandas adatokat numpy tömbé alakítja.

atlag = np.mean(jatekido)  #kiszámítja az átlagot

szoras = np.std(jatekido) #kiszámolja a szórást.

print(f"Átlag jaátékidő: {atlag:.2f}perc")
print(f"Játékidő szórása: {szoras:.2f} perc")

#4.feladat filmek száma évenként#

filmek_evente = (
    filmek.groupby("release_year") # csoportosítja a filmeket az alapján hogy melyik évben jelentek meg
    .size() #számolja az egyes évekhez tartozó filmek számát
    .sort_index() # megejezi hogy az évek sorrendben legyenek a grafikonon

)

plt.figure(figsize=(12, 6)) # beállítja a grafikon méretét

plt.plot( #megjeleníti a grafikonon a filmek számát évenként
    filmek_evente.index, # az x tengelyen az évek szerepelnek
    filmek_evente.values, # az y tengelyen a filmek száma szerepel
    marker = "o", # a pontok formája kör
    markersize = 5, # a pontok mérete
)

plt.title("Netflix filmek száma megjelenítése év szerint") # a grafikon címe

plt.xlabel("megjelenés éve") # az x tengely felirata

plt.ylabel("filmek száma") # az y tengely felirata

plt.grid(True) # a grafikonon megjeleníti a rácsvonalakat

plt.tight_layout() # a grafikon elemeit úgy helyezi el hogy ne legyenek átfedések

plt.savefig("netflix_film_megjelenes_ev_szerint.png", dpi=300) # elmenti a grafikon képét

plt.show() # megjeleníti a grafikon képét



#5.feladat#
#filmek és sorozatok aránya#

tipusok = df["type"].value_counts() # megszámolja hogy hány film és hány sorozat van a beolvasott adatban

print(tipusok) # kiírja a konzolra a filmek és sorozatok számát

plt.figure(figsize=(8, 8)) # beállítja a grafikon méretét

plt.pie( # megjeleníti a kördiagramot
 tipusok.values, # a kördiagram szeleteinek mérete a filmek és sorozatok számától függ
 labels = tipusok.index, # a kördiagram szeleteinek felirata a filmek és sorozatok neve
 autopct = "%1.1f%%", # a kördiagram szeleteinek százalékos aránya
 startangle = 90, # a kördiagram kezdő szöge

)

plt.title("Netflix filmek és sorozatok aránya") # a grafikon címe

plt.tight_layout() # a grafikon elemeit úgy helyezi el hogy ne legyenek átfedések

plt.savefig("netflix_film_sorozat_aranya.png", dpi=300) # elmenti a grafikon képét

plt.show() # megjeleníti a grafikon képét