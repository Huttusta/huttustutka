import ICONS from "./assets/data/product_icons.json"
import COORDINATES from "./assets/data/alko_coordinates_no_noutopiste.json"
import PRODUCT_NAMES from "./assets/data/alko_products_available.json"

const IMG_PATH = "img/"
const ALKO_ICON = "alko_logo.png"
const SAD_FACE = "sadface.png"
const TRESHOLDS = [5, 10, 30, 50]
const MASTER_WIDTH_PX = 30
const ICON_SCALING = [1, 1.5, 2.0, 2.4, 2.8] 

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

export interface StoreAndProductNames {
  storeName: string,
  productName: string,
}

/* export function getStoreCoordinates(storeId: string): google.maps.LatLng | undefined { */
/*   const store = COORDINATES.find((store) => store.id === storeId) */
/*   if (store?.latitude) return new google.maps.LatLng(store.latitude, store.longitude) */
/*   return undefined */
/* } */

function scaleImage(imgPath: string): Array<number> {
  const img = new Image()
  img.src = imgPath
  const imgScaler = MASTER_WIDTH_PX / img.width
  img.width *= imgScaler
  img.height *= imgScaler
  return [img.width, img.height]
}

export function getIcon(
    store: StoreAmount | undefined, 
    productId: string
): google.maps.Icon {
  if (!store) return { url: `${IMG_PATH}${SAD_FACE}` }

  const storeIcon: StoreIcon | undefined = ICONS.find((p) => p.id === productId)   
  const iconName = storeIcon ? storeIcon.icon : ALKO_ICON
  const imgPath = `${IMG_PATH}/${iconName}`
  let scale = ICON_SCALING[ICON_SCALING.length - 1]
  for (let i = 0; i < TRESHOLDS.length; i++) {
    if (store.min <= TRESHOLDS[i]) {
      scale = ICON_SCALING[i]
      break
    }
  }

  const imgSize = scaleImage(imgPath)
  return {
    url: imgPath, 
    scaledSize: new google.maps.Size(
      imgSize[0] * scale, 
      imgSize[1] * scale, 
    ),
  }
}

export async function fetchAmounts(url: string): Promise<Array<StoreAmount>> {
  const response = await fetch(url)
  if (!response.ok) throw new Error("Failed to fetch amounts!")
  return await response.json()
}

export function getStoreName(storeId: string): string {
  const store = COORDINATES.find((s) => s.id === storeId)
  if (!store) throw new Error("Failed to find store!")
  return store.name
}

export function getProductName(productId: string): string {
  const product = PRODUCT_NAMES.find((p) => p.id === productId)
  if (!product) throw new Error("Failed to find product!")
  return product.name
}