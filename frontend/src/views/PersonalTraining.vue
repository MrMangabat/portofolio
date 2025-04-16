<script setup>
import { personalTrainerStore } from "/src/stores/personalTrainerStore.js";
import { ref } from "vue";


// db 
const headers = ref([
  { title: "Navn", key: "navn" },
  { title: "Muskelgruppe", key: "muskelgruppe" },
  { title: "Muskel Bevægelse", key: "muskel_bevægelse" },
  { title: "Void MetCon", key: "voidMetCon" },
  { title: "Velegnet til", key: "goodFor" },
  { title: "Fordele", key: "advantages" },
  { title: "Ulemper", key: "disadvantages" },
  { title: "Skader", key: "injuries" }
]);

</script>

<template>
  <v-container id="MetCon-Info">
    <h1>Hvad er MetCon?</h1>
    <p>
      MetCon står for <strong>Metabolic Conditioning</strong>. Formålet er at forbedre kroppens evne til at producere og bruge energi. 
      Det sker gennem <strong>intervalbaseret træning med høj intensitet</strong>, der kombinerer vægtløftning, kondition, plyometri og kropsvægtsøvelser.
    </p>

    <br>
    <h2>Hvorfor MetCon?</h2>
    <ul>
      <li>Effektiv konditionstræning</li>
      <li>Tidsbesparende</li>
      <li>Stor variation</li>
      <li>Mulighed for at træne mange bevægelser</li>
      <li>Motiverende</li>
    </ul>

    <br>
    <h2>MetCon vs. CrossFit</h2>
    <p><strong>CrossFit:</strong> Sportsgren der kombinerer mange træningsformer med fokus på konkurrence.</p>
    <p><strong>MetCon:</strong> En metode til at forbedre kroppens energisystemer uden konkurrencefokus.</p>

    <br>
    <h2>Energisystemer i MetCon</h2>
    <v-row>
      <v-col cols="12" md="4">
        <br>
        <h3>Det akutte system</h3>
        <ul>
          <li>Primær energikilde: Kreatinfosfat</li>
          <li>Arbejdstid: 0-20 sek</li>
          <li>Arbejds/hvile forhold: 1:6 - 1:10+</li>
          <li>Eksempel: 20 sek. sprint / 180 sek. pause</li>
        </ul>
      </v-col>
      <v-col cols="12" md="4">
        <br>
        <h3>Det glykolytiske system</h3>
        <ul>
          <li>Primær energikilde: Glykolyse</li>
          <li>Arbejdstid: 20 sek - 2 min</li>
          <li>Arbejds/hvile forhold: 1:2 - 2:1</li>
          <li>Eksempel: 30 sek. arbejde / 30-60 sek. pause</li>
        </ul>
      </v-col>
      <v-col cols="12" md="4">
        <br>
        <h3>Det aerobe system</h3>
        <ul>
          <li>Primær energikilde: Kulhydrat & fedt</li>
          <li>Arbejdstid: 1-4 min</li>
          <li>Arbejds/hvile forhold: 2:1 - 6:1</li>
          <li>Eksempel: 3 min arbejde / 1 min pause</li>
        </ul>
      </v-col>
    </v-row>

    <br>
    <h2>Format & Skaleringsmuligheder</h2>
    <ul>
      <li>Intervaller med fast arbejde/pause tid</li>
      <li><strong>EMOM:</strong> Every Minute On the Minute</li>
      <li><strong>AMRAP:</strong> As Many Reps As Possible</li>
      <li><strong>RFT:</strong> Rounds For Time</li>
      <li>Mulighed for skalering: vægt, tempo, ROM, reps</li>
    </ul>

    <br>
    <h2>Øvelsestyper & Struktur</h2>
    <p>Gode MetCon øvelser: Kettlebell Swings, Thrusters, Wall Balls, Burpees, Battle Ropes, m.fl.</p>
    <p>Undgå: statiske øvelser, teknisk svære øvelser, hvor muskeludmattelse eller teknik begrænser.</p>
    <p><strong>Tip:</strong> Læg teknisk svære øvelser i starten, når deltageren er frisk.</p>

      <v-data-table
        :headers="headers"
        :items="personalTrainerStore.exercises"
        item-value="id"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Træningsøvelser</v-toolbar-title>
          </v-toolbar>
        </template>
      </v-data-table>

    <br>
    <h2>Instruktion</h2>
    
    <ul>
      <li><strong>Enkel øvelse: </strong>Vis - Forklar - Vis</li>
      <li><strong>Kompleks øvelse: </strong>Opdel i delelementer</li>
    </ul>
    
    <br>
    <h2>Fejlretning</h2>
    <li><strong>Load: </strong>Tilføj el. fjern vægt</li>
    <li><strong>Motorisk: </strong>Verbalt, visuelt el. taktilt</li>
    <li><strong>Mobilitet: </strong>Stiv krop, find ny øvelse</li>
    <li><strong>Fejlretning: </strong>Stop kun ved potentielt farlige fejl</li>

    <br>
    <h1>MetCon Intensitet</h1>
    <p>Intensitet i MetCon handler ikke kun om vægte eller puls – men om <strong>hvor meget arbejde</strong> du kan presse ind i en bestemt tidsramme. Det kaldes <strong>densitet</strong>.</p>

    <br>
    <h2>Hvordan måles intensitet ellers?</h2>
    
    <br>
    <h3>Intensitet i styrketræning</h3>
    <p>Intensiteten i styrketræning måles typisk på to måder:</p>
    <ul>
      <li><strong>%RM (Repetition Maximum):</strong> Procent af den maksimale vægt du kan løfte én gang (1RM). F.eks. 80% RM betyder, at du løfter 80% af din 1RM.</li>
      <li><strong>RIR (Reps In Reserve):</strong> Hvor mange gentagelser du har tilbage i tanken efter et sæt. F.eks. RIR 2 betyder, at du kunne have lavet 2 gentagelser mere.</li>
    </ul>

    <br>
    <h4>Anvendelse i programmering</h4>
    <p>%RM bruges til at styre belastning i styrketræning — typisk 70-85% RM for hypertrofi, 85-100% for styrke.</p>
    <p>RIR bruges til at styre træthed og sikre, at deltageren ikke træner til failure hele tiden.</p>

    <v-divider class="my-4"></v-divider>

    <br>
    <h3>Intensitet i konditionstræning</h3>
    <p>I konditionstræning måles intensiteten ud fra:</p>
    <ul>
      <li><strong>% af makspuls:</strong> Typisk 60-80% af max puls for udholdenhed og 80-95% for højintensiv træning.</li>
      <li><strong>Borg-skala:</strong> Subjektiv vurdering af anstrengelse fra 6-20 (original skala) eller 1-10 (moderne version).</li>
    </ul>

    <h4>Anvendelse i programmering</h4>
    <p>Vi bruger puls eller Borg-skala til at sikre, at deltageren arbejder med den ønskede intensitet. F.eks. Zone 2-træning (60-70% max puls) for udholdenhed eller Zone 5 (>90%) for højintensiv kapacitet.</p>

    <v-divider class="my-4"></v-divider>

    <br>
    <h3>Intensitet i MetCon = Densitet</h3>
    <p>I MetCon træning måler vi intensitet som <strong>densitet:</strong> hvor meget arbejde kan der udføres i en given tidsramme.</p>
    <p>Formel:</p>
    <v-card class="p-4 mb-4">
      <strong>Densitet = Total arbejde / Total tid</strong>
    </v-card>
    <p>Eksempel:</p>
    <ul>
      <li>5 min AMRAP</li>
      <li>10 swings, 5 burpees, 20m sled push</li>
      <li>Udfører du 5 runder, så vil arbejdet (antal reps + distance) blive tracket uge for uge</li>
    </ul>

    <br>
    <h4>Anvendelse i programmering</h4>
    <ul>
      <li>Progression = Øge antal reps, rounds eller forkorte pauser → højere densitet</li>
      <li>Kan også bruges til skalering af programmer (begynder → avanceret)</li>
      <li>Vi vil senere måle og tracke denne progression</li>
    </ul>

    <v-divider class="my-4"></v-divider>
    <h2>Hvordan måler vi progression?</h2>

    <p><strong>MetCon intensitet måles i densitet:</strong> Hvor meget arbejde der kan udføres på tid (reps, runder, belastning).</p>
    <p>Vi registrerer individuelle data, som vi kan visualisere for klienten over tid.</p>

    <br>
    <v-divider></v-divider>

    <h1>Anatomi & Progressionsdata</h1>
    <p>
      For at tracke progression på muskelgrupper, skal vi vide, hvilke muskler arbejder i hvilke øvelser.
    </p>

    <h2>Eksempel: Squat</h2>
    <ul>
      <li>Bevægelse: Fleksion & ekstension i hofte, knæ & ankel</li>
      <li>Primære muskler: Gluteus Maximus, Quadriceps, Hamstrings, Gastrocnemius, Soleus</li>
    </ul>

    <h2>Eksempel: Biceps Curl</h2>
    <ul>
      <li>Bevægelse: Fleksion i albue</li>
      <li>Primære muskler: Biceps Brachii, Brachialis, Brachioradialis</li>
    </ul>


  </v-container>
</template>

<style scoped>

</style>


