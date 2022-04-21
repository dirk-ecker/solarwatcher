<template>
  <v-app>
    <v-app-bar app>
      <div style="width: 50px;">
        <v-img :src="logoImage" width="50"/>
      </div>
      <v-app-bar-title>Solarwatcher</v-app-bar-title>
    </v-app-bar>

    <v-main>

      <v-container fluid>
        <v-card>
          <v-card-title>
            Messwerte
          </v-card-title>
          <v-text>
            <v-container dense fluid>
              <v-row no-gutters>
                Filter
                <v-col>
                  <v-checkbox />
                  <v-select/>
                </v-col>
                <v-col>
                  <v-checkbox />
                  <v-select/>
                </v-col>
                <v-col>
                  <v-checkbox />
                  <v-select/>
                </v-col>
              </v-row>
            </v-container>

            <v-table>
              <thead>
              <tr>
                <th class="text-left">
                  Zeitpunkt
                </th>
                <th class="text-left">
                  Beschreibung
                </th>
                <th class="text-left">
                  Leistung
                </th>
                <th class="text-left">
                  Einheit
                </th>
              </tr>
              </thead>
              <tbody>
              <tr
                  v-for="item in measurements"
                  :key="item.timestamp"
              >
                <td>{{ item.timestamp }}</td>
                <td>{{ item.description }}</td>
                <td>{{ item.power }}</td>
                <td>{{ item.unit }}</td>
              </tr>
              </tbody>
            </v-table>
          </v-text>
        </v-card>

      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import data from './assets/data.json'
import logoImage from './assets/logo.png'

const measurements = ref([])

measurements.value = data

</script>
