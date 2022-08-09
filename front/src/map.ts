import ALKO_PRODUCTS from "./assets/data/alko_products_available.json"
import COORDINATES from "./assets/data/alko_coordinates_no_noutopiste.json"
import { Loader } from 'google-maps'
import {
  fetchAmounts,
  getIcon,
} from "./util";

const GOOGLE_API_KEY = import.meta.env.VITE_GOOGLE_API_KEY;
const MAP_ID = "map";
const APP_ID = "app";
const SEARCH_INPUT_ID = "input-search";
const SEARCH_TABLE_ID = "search-results";
const LOADING_ID = "img-loading";
const LOADING_IMG_PATH = "img/gambina.png"

export interface MarkerStorage {
  [key: string]: google.maps.Marker;
}

function addMapElement(app: HTMLDivElement, mapId: string): void {
  const el = document.createElement("div");
  el.id = mapId;
  app.appendChild(el);
}

function addProductSearch(app: HTMLDivElement): void {
  const input = document.createElement("input");
  input.id = SEARCH_INPUT_ID;
  input.innerText = "Valitse janojuoma";
  input.setAttribute("autofocus", "yes")
  input.setAttribute("placeholder", "Etsi janojuomaa")

  const table = document.createElement("table");
  table.id = SEARCH_TABLE_ID;

  app.appendChild(input);
  app.appendChild(table);
}

function addLoadingElement(app: HTMLDivElement): void {
  const img = document.createElement("img");
  img.id = LOADING_ID
  img.src = LOADING_IMG_PATH
  img.alt = "Loading"
  img.setAttribute("width", "5%")

  app.appendChild(img);
}

export async function createMap(): Promise<google.maps.Map> {
  const app = document.querySelector<HTMLDivElement>(`#${APP_ID}`)!

  addMapElement(app, MAP_ID)
  addProductSearch(app)
  addLoadingElement(app)

  const loader = new Loader(GOOGLE_API_KEY, { version: "weekly" });
  await loader.load();

  return new google.maps.Map(document.getElementById(MAP_ID) as HTMLElement, {
    center: { lat: 60.1707368, lng: 24.9347073 },
    zoom: 10,
  });
}

export function initInfoWindow(): google.maps.InfoWindow {
  return new google.maps.InfoWindow();
}

export function handleInfowindowClick(
  map: google.maps.Map,
  marker: google.maps.Marker,
  infoWindow: google.maps.InfoWindow,
  storeName: string,
  min: number | undefined,
  max: number | undefined,
): void {
  infoWindow.close();
  let content = `${storeName}`
  if (min) {
      const amount = min === max ? min : `${min}-${max}`;
      content += ` ${amount} kpl`
  } else {
      content += " Tuotetta ei saatavilla"
  }
  infoWindow.setContent(content);
  infoWindow.open(map, marker);
}

export async function initMarkers(
  map: google.maps.Map,
  infoWindow: google.maps.InfoWindow,
  url: string,
  productId: string,
): Promise<MarkerStorage> {
  let newMarkers: MarkerStorage = {}
  const storeAmounts = await fetchAmounts(`${url}/${productId}/`)

  COORDINATES.forEach(async (store) => {
    const fetchedStore = storeAmounts.find((s) => s.id === store.id)
    const marker = new google.maps.Marker({
      map: map,
      icon: await getIcon(fetchedStore, productId),
    })

    if (store.latitude) marker.setPosition(new google.maps.LatLng(
      store.latitude,
      store.longitude,
    ))

    newMarkers[store.id] = marker
    marker.addListener("click", () => {
      handleInfowindowClick(
        map,
        marker,
        infoWindow,
        store.name,
        fetchedStore?.min,
        fetchedStore?.max,
      )
    })
  })

  return newMarkers;
}

async function setMarkers(
  map: google.maps.Map,
  infoWindow: google.maps.InfoWindow,
  markers: MarkerStorage,
  url: string,
  productId: string,
): Promise<void> {
  const loadingElement = <HTMLDivElement>(document.getElementById(LOADING_ID))
  loadingElement.style.display = "block"

  const storeAmounts = await fetchAmounts(`${url}/${productId}/`)
  COORDINATES.forEach(async (store) => {
    const fetchedStore = storeAmounts.find((s) => s.id === store.id)
    const marker = markers[store.id]
    marker.setIcon(await getIcon(fetchedStore, productId))
    marker.addListener("click", () => {
      handleInfowindowClick(
        map,
        marker,
        infoWindow,
        store.name,
        fetchedStore?.min,
        fetchedStore?.max,
      )
    });
  });

  loadingElement.style.display = "none"
}

export function setProductChangeHandler(
  map: google.maps.Map,
  markers: MarkerStorage,
  infoWindow: google.maps.InfoWindow,
  url: string
): void {
  const input = <HTMLInputElement>(document.getElementById(SEARCH_INPUT_ID));
  const table = <HTMLTableElement>(document.getElementById(SEARCH_TABLE_ID));

  input.addEventListener("input", function() {
    table.innerHTML = ""
    const searchString: string = input.value.toLowerCase();

    if (!searchString) return

    const products = ALKO_PRODUCTS.filter(
      (p) => p.name.toLowerCase().includes(searchString)
    ).sort(
      (a, b) => {
        return a.name.toLowerCase().indexOf(searchString) - b.name.toLowerCase().indexOf(searchString)
      }
    )

    if (!products.length) {
      const row = document.createElement("tr")
      row.innerText = "Ei tuloksia"
      table.appendChild(row)
      return
    }

    products.forEach((product) => {
      const row = document.createElement("tr")
      row.innerText = product.name
      row.setAttribute("data-value", product.id)
      row.classList.add("search-product-row")
      row.addEventListener("click", async () => {
        input.value = product.name
        infoWindow.close();
        table.innerHTML = ""
        await setMarkers(
          map,
          infoWindow,
          markers,
          url,
          <string>(row.getAttribute("data-value")),
        )
      })
      table.appendChild(row)
    })
  })
}
