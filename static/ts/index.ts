import { Loader } from "google-maps"

function marker_url(product_id: number): string {
  return `/marker/${product_id}`
}

const LOADER = new Loader(process.env.GOOGLE_API_KEY, { version: "weekly"})

let MAP: google.maps.Map
LOADER.load().then(() => {
  const MAP = new google.maps.Map(document.getElementById("map") as HTMLElement, {
    center: { lat: 60.1707368, lng: 24.9347073 },
    zoom: 10,
  })
})

interface Marker {
  icon: string,
  lat: number,
  lng: number,
  infobox: string,
  scale: number,
} 

let markerArray: Array<google.maps.Marker>

async function getMarkers(product_id: number): Promise<Array<Marker>> {
  const response = await fetch(`/marker/${product_id}`)
  if (response.ok) return response.json()
  throw new Error('Failed to fetch product markers')
}


void async function changeProduct(product_id: string) {
  const markers = await getMarkers(parseInt(product_id))
  markerArray.forEach((marker) => { 
    marker.setMap(null)
  })
  markerArray = []
  markers.forEach((marker) => {
    const newMarker = new google.maps.Marker({
      position: { lat: marker.lat, lng: marker.lng },
      map: MAP,
    })
    newMarker.setMap(MAP)
  })
}
