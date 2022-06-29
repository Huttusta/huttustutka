import './assets/css/style.css'
import { Loader } from 'google-maps'
import { 
  getStoreCoordinates, 
  getIcon,
  fetchMarkers,
  getStoreName,
} from './util'

const GOOGLE_API_KEY = "AIzaSyCrHBMGwEmJtbpZvNEsYfOUq6HVEopLdDQ"
const MAP_ID = "map"
const API_URL = "http://localhost:5000"

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

const storeMarkers = await fetchMarkers(`${API_URL}/amounts`)
storeMarkers.forEach((store) => {
  const storeCoords = getStoreCoordinates(store.id)
  if (!storeCoords) return

  const marker = new google.maps.Marker({
    map: map,
    position: storeCoords,
    icon: getIcon(store),
  })

  marker.addListener("click", () => {
    const amount = store.min === store.max ? store.min : `${store.min}-${store.max}`
    const infoWindow = new google.maps.InfoWindow({
      content: `${getStoreName(store.id)} ${amount}`
    })  
    infoWindow.open({
      anchor: marker,
      map,
      shouldFocus: false,
    })
  })
})
