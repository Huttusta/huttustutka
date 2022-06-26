import './assets/css/style.css'
import { Loader } from 'google-maps'

const app = document.querySelector<HTMLDivElement>('#app')!
app.innerHTML = `
  <div id="map"></div>
`

const loader = new Loader(process.env.GOOGLE_API_KEY, { version: "weekly" })

let map: google.maps.Map
loader.load().then(() => {
  map = new google.maps.Map(document.getElementById("map") as HTMLElement, {
    center: { lat: 60.1707368, lng: 24.9347073 },
    zoom: 10,
  })
})
