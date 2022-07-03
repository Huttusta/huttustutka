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
const DIV_SELECTOR_ID = "product-selector";
const SELECT_ID = "select-huttunen";
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

function addProductSelector(app: HTMLDivElement, defaultId: string): void {
  const div = document.createElement("div");
  div.id = DIV_SELECTOR_ID;

  const label = document.createElement("label");
  label.htmlFor = div.id;
  label.innerText = "Valitse janojuoma";
  div.appendChild(label);

  const select = document.createElement("select");
  select.id = SELECT_ID;
  div.appendChild(select);

  ALKO_PRODUCTS.forEach((product) => {
    const option = document.createElement("option");
    option.value = product.id;
    option.innerText = product.name;
    if (defaultId === product.id) option.selected = true
    select.appendChild(option);
  });

  app.appendChild(div);
}

function addLoadingElement(app: HTMLDivElement): void {
  const img = document.createElement("img");
  img.id = LOADING_ID
  img.src = LOADING_IMG_PATH
  img.alt = "Loading"
  img.setAttribute("width", "5%")

  app.appendChild(img);
}

export async function createMap(
  defaultId: string,
): Promise<google.maps.Map> {
  const app = document.querySelector<HTMLDivElement>(`#${APP_ID}`)!

  addMapElement(app, MAP_ID)
  addProductSelector(app, defaultId)
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

  COORDINATES.forEach((store) => {
    const fetchedStore = storeAmounts.find((s) => s.id === store.id)
    const marker = new google.maps.Marker({
      map: map,
      icon: getIcon(fetchedStore, productId),
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
  COORDINATES.forEach((store) => {
    const fetchedStore = storeAmounts.find((s) => s.id === store.id)
    const marker = markers[store.id]
    marker.setIcon(getIcon(fetchedStore, productId))
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

export function addProductSelectorOnChange(
  map: google.maps.Map,
  infoWindow: google.maps.InfoWindow,
  markers: MarkerStorage,
  url: string
): void {
  const select: HTMLSelectElement | null = <HTMLSelectElement>(
    document.getElementById(SELECT_ID)
  );

  select.onchange = async () => {
    infoWindow.close();
    await setMarkers(map, infoWindow, markers, url, select.value);
  };
}
