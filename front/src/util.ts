import ICONS from './assets/data/product_icons.json'

const ALKO_ICON = 'huttunen.png'
const TRESHOLDS = [5, 10, 30, 50]
const ICON_SCALING = [1, 2, 3, 4, 5]

export interface StoreCoordinates {
  id: string,
  name: string,
  address: string,
  latitude?: number,
  longitude?: number,
}

export interface StoreAmount {
  id: string,
  min: number,
  max: number,
}

export interface StoreIcon {
  id: string,
  icon: string,
}

export function getStoreCoordinates(
  storeId: string, 
  coordinates: Array<StoreCoordinates>
): google.maps.LatLng | undefined {
  const store = coordinates.find((store) => store.id === storeId)
  if (store?.latitude) return new google.maps.LatLng(store.latitude, store.longitude)
  return undefined
}

export function getIcon(store: StoreAmount): google.maps.Icon {
  const storeIcon: StoreIcon | undefined = ICONS.find((s) => s.id === store.id)   
  const iconName = storeIcon ? storeIcon.icon : ALKO_ICON
  let scaledSize: number = ICON_SCALING[ICON_SCALING.length - 1]
  for (let i = 0; i < TRESHOLDS.length; i++) {
    if (store.min <= TRESHOLDS[i]) {
      scaledSize = ICON_SCALING[i]
      break
    }
  }

  return new google.maps.Icon({
    url: iconName, 
    scaledSize,
  })
}
