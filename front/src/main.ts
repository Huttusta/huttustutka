import './assets/css/style.css'
import { Loader } from 'google-maps'
import { StoreCoordinates, StoreAmount, getStoreCoordinates, getIcon } from './util'

const GOOGLE_API_KEY = "AIzaSyCrHBMGwEmJtbpZvNEsYfOUq6HVEopLdDQ"
const MAP_ID = "map"
const API_URL = "localhost:5000"

const app = document.querySelector<HTMLDivElement>('#app')!
app.innerHTML = `
  <div id="${MAP_ID}"></div>
`

const loader = new Loader(GOOGLE_API_KEY, { version: "weekly" })

let map: google.maps.Map
loader.load().then(() => {
  map = new google.maps.Map(document.getElementById(MAP_ID) as HTMLElement, {
    center: { lat: 60.1707368, lng: 24.9347073 },
    zoom: 10,
  })
})

fetch(`${API_URL}/amounts/`).then(async (response) => {
  if (!response.ok) throw new Error('Failed to fetch amounts!')

  const coordinates: Array<StoreCoordinates> = await import("./assets/data/alko_coordinates.json")

  response.json().then((stores: Array<StoreAmount>) => {
    stores.forEach((store) => {
      const storeCoords = getStoreCoordinates(store.id, coordinates)
      if (!storeCoords) return
      new google.maps.Marker({
        map: map,
        position: storeCoords,
        icon: getIcon(store),
      })
    })
  })
})
