import COORDINATES from "./assets/data/alko_coordinates_no_noutopiste.json"
import PRODUCT_NAMES from "./assets/data/alko_products_available.json"
//import PRODUCT_ICONS from "./assets/data/product_icons.json"

const IMG_PATH = "img/"
const ALKO_ICON = "alko_logo.png"
const SAD_FACE = "sadface.png"
const TRESHOLDS = [10, 20, 30, 50]
const MAX_ICON_PX = 50
const ICON_SCALING = [1, 1.5, 1.9, 2.3, 2.6]
const ALKO_CDN_URL = "https://images.alko.fi/images/cs_srgb,f_auto,t_medium/cdn/"

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

async function getIconImage(productId: string): Promise<HTMLImageElement> {
  const productImage = `${ALKO_CDN_URL}/${productId}/a`
  const img = new Image()
  img.src = productImage ? productImage : `${IMG_PATH}${ALKO_ICON}`
  await img.decode()
  return img
}

function scaleImage(img: HTMLImageElement): Array<number> {
  const imgScaler = MAX_ICON_PX / Math.max(img.width, img.height)
  img.width *= imgScaler
  img.height *= imgScaler
  return [img.width, img.height]
}

export async function getIcon(
  store: StoreAmount | undefined,
  productId: string
): Promise<google.maps.Icon> {
  if (!store) return { url: `${IMG_PATH}${SAD_FACE}` }

  let scale = ICON_SCALING[ICON_SCALING.length - 1]
  for (let i = 0; i < TRESHOLDS.length; i++) {
    if (store.min <= TRESHOLDS[i]) {
      scale = ICON_SCALING[i]
      break
    }
  }

  const iconImage = await getIconImage(productId)
  const imgSize = scaleImage(iconImage)

  return {
    url: iconImage.src,
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
